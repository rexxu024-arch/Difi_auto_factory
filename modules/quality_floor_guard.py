from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageFilter, ImageStat


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
REPORT_PATH = DATABASE_DIR / "Quality_Floor_Guard.csv"
SUMMARY_PATH = DATABASE_DIR / "Quality_Floor_Guard_State.json"
QUARANTINE_ROOT = DATABASE_DIR / "Quality_Floor_Quarantine"
NY = ZoneInfo("America/New_York")

TEXT_EXTS = {".txt", ".md", ".csv", ".json", ".html", ".htm"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

SECRET_RE = re.compile(
    r"(\bapi[_-]?key\s*[:=]|\btoken\s*[:=]|\bsecret\s*[:=]|\bpassword\s*[:=]|authorization\s*[:=]\s*bearer|bearer\s+[a-z0-9._-]{16,})",
    re.I,
)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
LOGIN_ERROR_PHRASE = "an error has occurred, please try again"
HTML_ERROR_PHRASE = "service unavailable - zero size object"


@dataclass
class QualityResult:
    timestamp: str
    path: str
    profile: str
    verdict: str
    failed_count: int
    passed_count: int
    failed_rules: str
    action: str
    quarantine_path: str = ""


def _now():
    return datetime.now(NY).isoformat(timespec="seconds")


def _sha256(path: Path, limit_mb=100):
    if not path.is_file() or path.stat().st_size > limit_mb * 1024 * 1024:
        return ""
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _text_sample(path: Path, max_chars=250_000):
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except Exception:
        return ""


def _image_metrics(path: Path):
    with Image.open(path) as image:
        image = image.convert("RGB")
        gray = image.convert("L")
        small = gray.resize((512, 512), Image.Resampling.LANCZOS)
        stat = ImageStat.Stat(small)
        pixels = list(small.getdata())
        total = len(pixels)
        black_clip = sum(1 for px in pixels if px <= 3) / total
        white_clip = sum(1 for px in pixels if px >= 252) / total
        edges = small.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        return {
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "mean_luma": stat.mean[0],
            "stddev_luma": stat.stddev[0],
            "black_clip_pct": black_clip * 100,
            "white_clip_pct": white_clip * 100,
            "edge_energy": edge_stat.mean[0],
            "aspect": image.width / max(1, image.height),
        }


def _rule(name, ok, reason=""):
    return {"name": name, "ok": bool(ok), "reason": reason}


def _is_login_error_capture(text: str, suffix: str) -> bool:
    lower = text.lower()
    if LOGIN_ERROR_PHRASE not in lower:
        return False

    # Reports and recovery notes often quote marketplace errors as history. Those
    # should remain reviewable; this guard is meant to catch raw captured pages.
    documentation_markers = [
        "historical blocker",
        "resolved later",
        "current state supersedes",
        "returned the red",
        "login block",
    ]
    if suffix in {".md", ".txt"} and any(marker in lower for marker in documentation_markers):
        return False

    login_page_markers = [
        "sign in to continue",
        "continue with google",
        "continue with facebook",
        "continue with apple",
        "email address",
        "forgot your password",
    ]
    marker_hits = sum(1 for marker in login_page_markers if marker in lower)
    return suffix in {".html", ".htm"} or marker_hits >= 3


def _is_html_error_capture(text: str, suffix: str) -> bool:
    lower = text.lower()
    if HTML_ERROR_PHRASE not in lower:
        return False
    documentation_markers = [
        "user reported",
        "web check",
        "diagnosis",
        "likely local",
        "reference #",
        "cdn-edge issue",
    ]
    if suffix in {".md", ".txt"} and any(marker in lower for marker in documentation_markers):
        return False
    error_page_markers = ["the server is temporarily unable", "errors.edgesuite.net", "<html", "<body"]
    marker_hits = sum(1 for marker in error_page_markers if marker in lower)
    return suffix in {".html", ".htm"} or marker_hits >= 2


def evaluate_path(path: Path, profile="basic"):
    path = Path(path)
    rules = []
    rel_ok = True
    try:
        path.resolve().relative_to(PROJECT_ROOT.resolve())
    except Exception:
        rel_ok = False
    rules.extend(
        [
            _rule("01_path_inside_project", rel_ok, "path is outside project root"),
            _rule("02_exists", path.exists(), "missing path"),
            _rule("03_not_browser_profile", "openclaw_edge_profile" not in str(path).lower(), "browser profile data"),
            _rule("04_not_env_file", path.name.lower() != ".env", "env files are never outputs"),
            _rule("05_not_git_internal", ".git" not in path.parts, "git internals are not outputs"),
        ]
    )
    if not path.exists():
        return rules
    stat = path.stat()
    suffix = path.suffix.lower()
    rules.extend(
        [
            _rule("06_non_empty", stat.st_size > 0, "empty file"),
            _rule("07_reasonable_size", stat.st_size < 250 * 1024 * 1024, "file too large for grunt output"),
            _rule("08_filename_no_temp_suffix", not path.name.endswith((".tmp", ".partial", ".crdownload")), "temporary file"),
            _rule("09_filename_no_backup_prefix", not path.name.startswith("~$"), "office lock/temp file"),
            _rule("10_supported_or_known_extension", suffix in TEXT_EXTS | IMAGE_EXTS | {".xlsx", ".zip", ".log"} or path.is_dir(), "unknown extension"),
        ]
    )

    sha = _sha256(path)
    rules.append(_rule("11_hash_readable", bool(sha) or path.is_dir() or stat.st_size > 100 * 1024 * 1024, "cannot hash file"))

    text = _text_sample(path) if suffix in TEXT_EXTS or path.name.endswith(".log") else ""
    if text:
        lines = text.splitlines()
        rules.extend(
            [
                _rule("12_utf8_readable", "\ufffd" not in text[:5000], "replacement chars in text"),
                _rule("13_no_secret_markers", not SECRET_RE.search(text), "possible secret marker"),
                _rule("14_no_binary_control_chars", not CONTROL_RE.search(text), "control chars"),
                _rule("15_line_count_nonzero", len(lines) > 0, "no text lines"),
                _rule("16_no_single_line_giant_blob", max((len(line) for line in lines), default=0) < 80_000, "giant line"),
                _rule("17_not_html_error_page", not _is_html_error_capture(text, suffix), "captured error page"),
                _rule("18_not_login_error_page", not _is_login_error_capture(text, suffix), "captured login error page"),
                _rule("19_not_traceback_only", not text.lstrip().startswith("Traceback (most recent call last):"), "raw traceback artifact"),
                _rule("20_has_content_words", len(re.findall(r"[A-Za-z0-9]{3,}", text)) >= 3, "too little useful text"),
            ]
        )
        if suffix == ".json":
            try:
                json.loads(text)
                json_ok = True
            except Exception:
                json_ok = False
            rules.append(_rule("21_json_parses", json_ok, "invalid json"))
        else:
            rules.append(_rule("21_json_parses_or_not_json", True))
        if suffix == ".csv":
            try:
                with path.open("r", encoding="utf-8-sig", newline="") as handle:
                    reader = csv.reader(handle)
                    header = next(reader, [])
                    first = next(reader, [])
                csv_ok = bool(header)
                row_ok = not first or len(first) == len(header)
            except Exception:
                csv_ok = False
                row_ok = False
            rules.extend(
                [
                    _rule("22_csv_has_header", csv_ok, "csv missing header"),
                    _rule("23_csv_first_row_shape", row_ok, "csv row/header length mismatch"),
                ]
            )
        else:
            rules.extend([_rule("22_csv_has_header_or_not_csv", True), _rule("23_csv_shape_or_not_csv", True)])
    else:
        rules.extend([_rule(f"{i:02d}_text_rule_not_applicable", True) for i in range(12, 24)])

    if suffix in IMAGE_EXTS:
        try:
            m = _image_metrics(path)
            min_side = min(m["width"], m["height"])
            max_side = max(m["width"], m["height"])
            rules.extend(
                [
                    _rule("24_image_opens", True),
                    _rule("25_image_min_side_512", min_side >= 512, "image too small"),
                    _rule("26_image_max_side_reasonable", max_side <= 12000, "image dimension too large"),
                    _rule("27_image_not_blank_low_contrast", m["stddev_luma"] >= 18, "low contrast"),
                    _rule("28_image_not_shadow_clipped", m["black_clip_pct"] <= 25, "too much black clipping"),
                    _rule("29_image_not_highlight_clipped", m["white_clip_pct"] <= 35, "too much white clipping"),
                    _rule("30_image_has_edges", m["edge_energy"] >= 4, "soft/blank image"),
                    _rule("31_image_aspect_valid", 0.25 <= m["aspect"] <= 4.5, "odd aspect ratio"),
                    _rule("32_image_luma_not_extreme_dark", m["mean_luma"] >= 12, "too dark"),
                    _rule("33_image_luma_not_extreme_bright", m["mean_luma"] <= 245, "too bright"),
                    _rule("34_image_mode_rgb", m["mode"] == "RGB", "unexpected mode"),
                    _rule("35_image_profile_specific_resolution", min_side >= (1000 if profile in {"product", "image"} else 512), "profile min resolution"),
                ]
            )
        except Exception as exc:
            rules.extend([_rule("24_image_opens", False, str(exc))])
            rules.extend([_rule(f"{i:02d}_image_rule_unavailable", False, "image failed to open") for i in range(25, 36)])
    else:
        rules.extend([_rule(f"{i:02d}_image_rule_not_applicable", True) for i in range(24, 36)])

    rel = str(path.relative_to(PROJECT_ROOT)) if rel_ok else str(path)
    lower_rel = rel.lower()
    rules.extend(
        [
            _rule("36_not_in_pycache", "__pycache__" not in lower_rel, "pycache artifact"),
            _rule("37_not_raw_screenshot_root", not (path.name.lower().startswith("screen_") and path.parent == PROJECT_ROOT), "root screenshot artifact"),
            _rule("38_not_old_excel_lock", not path.name.startswith("~$"), "excel lock"),
            _rule("39_no_secret_filename", not any(x in path.name.lower() for x in ["secret", "token", "password", "credential"]), "secret-like filename"),
            _rule("40_parent_writable", path.parent.exists(), "parent missing"),
            _rule("41_not_deep_temp", ".tmp" not in lower_rel and "rwtemp" not in lower_rel, "temp folder artifact"),
            _rule("42_not_node_modules", "node_modules" not in path.parts, "dependency artifact"),
            _rule("43_not_venv", ".venv" not in path.parts, "venv artifact"),
            _rule("44_not_browser_cache", "cache" not in lower_rel or "review_packets" in lower_rel, "cache artifact"),
            _rule("45_not_empty_directory", not path.is_dir() or any(path.iterdir()), "empty directory"),
            _rule("46_timestamp_reasonable", stat.st_mtime > 1_600_000_000, "bad modified timestamp"),
            _rule("47_path_length_reasonable", len(str(path)) < 240, "path too long"),
            _rule("48_not_personal_temp_source", "xwechat_files" not in lower_rel, "personal temp source"),
            _rule("49_no_forbidden_marketplace_action", "buyer_message" not in lower_rel and "order_refund" not in lower_rel, "forbidden action artifact"),
            _rule("50_reviewable_or_quarantinable", True),
        ]
    )
    return rules


def quarantine(path: Path, reason: str, execute=False):
    target = QUARANTINE_ROOT / datetime.now(NY).strftime("%Y%m%d_%H%M%S") / path.name
    if not execute:
        return str(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    if path.is_dir():
        shutil.move(str(path), str(target))
    else:
        shutil.move(str(path), str(target))
    manifest = target.parent / "manifest.jsonl"
    with manifest.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"source": str(path), "target": str(target), "reason": reason}, ensure_ascii=False) + "\n")
    return str(target)


def discover(paths, limit=0):
    found = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        if path.is_file():
            found.append(path)
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and child.suffix.lower() in TEXT_EXTS | IMAGE_EXTS | {".log"}:
                    found.append(child)
                    if limit and len(found) >= limit:
                        return found
        if limit and len(found) >= limit:
            return found
    return found


def audit(paths, profile="basic", limit=0, execute_quarantine=False, fresh=False):
    DATABASE_DIR.mkdir(exist_ok=True)
    items = discover(paths, limit=limit)
    rows = []
    for path in items:
        rules = evaluate_path(path, profile=profile)
        failed = [rule for rule in rules if not rule["ok"]]
        passed = [rule for rule in rules if rule["ok"]]
        verdict = "PASS" if not failed else "QUARANTINE"
        failed_rules = ";".join(f"{rule['name']}:{rule['reason']}" for rule in failed)
        action = "ALLOW_REVIEW_QUEUE" if verdict == "PASS" else "ISOLATE_FROM_REVIEW_QUEUE"
        qpath = ""
        if failed:
            qpath = quarantine(path, failed_rules, execute=execute_quarantine)
            action = "MOVED_TO_QUARANTINE" if execute_quarantine else "QUARANTINE_RECOMMENDED"
        rows.append(
            QualityResult(
                timestamp=_now(),
                path=str(path),
                profile=profile,
                verdict=verdict,
                failed_count=len(failed),
                passed_count=len(passed),
                failed_rules=failed_rules,
                action=action,
                quarantine_path=qpath,
            )
        )
        print(f"[QUALITY-FLOOR] {path.name} {verdict} failed={len(failed)}")

    mode = "w" if fresh else "a"
    exists = REPORT_PATH.exists() and not fresh
    with REPORT_PATH.open(mode, encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(QualityResult.__dataclass_fields__.keys()))
        if not exists:
            writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    summary = {
        "generated_at": _now(),
        "count": len(rows),
        "pass": sum(1 for row in rows if row.verdict == "PASS"),
        "quarantine": sum(1 for row in rows if row.verdict != "PASS"),
        "execute_quarantine": execute_quarantine,
        "report": str(REPORT_PATH),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return rows


def main():
    parser = argparse.ArgumentParser(description="50-rule quality floor guard for Grunt Engine outputs.")
    parser.add_argument("--paths", nargs="+", default=["Database"])
    parser.add_argument("--profile", default="basic")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--execute-quarantine", action="store_true")
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args()
    rows = audit(args.paths, profile=args.profile, limit=args.limit, execute_quarantine=args.execute_quarantine, fresh=args.fresh)
    if any(row.verdict != "PASS" for row in rows):
        raise SystemExit(3)


if __name__ == "__main__":
    main()
