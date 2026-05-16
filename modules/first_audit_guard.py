"""Guard premium First Audit assets from public marketplace queues.

This is intentionally audit-first: it creates a machine-readable blocklist and
checks public queue files for accidental leaks. It does not publish, delete, or
mutate marketplace rows.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "Database"
REVIEW_DIR = ROOT / "Review_Packets" / "First_Audit_001"
MANIFEST = DATABASE / "First_Audit_001_Asset_Manifest.csv"
BLOCKLIST = DATABASE / "First_Audit_001_Blocklist.csv"
AUDIT_CSV = DATABASE / "First_Audit_001_Guard_Audit.csv"
AUDIT_MD = REVIEW_DIR / "FIRST_AUDIT_GUARD_REPORT.md"

PUBLIC_QUEUE_HINTS = (
    "etsy",
    "ebay",
    "digital",
    "listing",
    "upload",
    "launch",
    "metadata",
)

PRIVATE_ALLOW_HINTS = (
    "first_audit",
    "shock_and_awe",
    "private",
)


@dataclass(frozen=True)
class FirstAuditAsset:
    audit_id: str
    sku: str
    concept: str
    production_file: str
    source_file: str
    action: str

    @property
    def markers(self) -> set[str]:
        values = {self.audit_id, self.sku}
        for raw_path in (self.production_file, self.source_file):
            if raw_path:
                p = Path(raw_path)
                values.add(str(p).replace("\\", "/"))
                # Source files are SKU-specific, but production files are often
                # generic names such as Production_Design.png. Matching generic
                # basenames would turn every public queue into a false positive.
                if p.name.lower().startswith(self.sku.lower()):
                    values.add(p.name)
        return {v.lower() for v in values if v}


def et_now() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_manifest() -> list[FirstAuditAsset]:
    if not MANIFEST.exists():
        raise FileNotFoundError(f"Missing First Audit manifest: {MANIFEST}")
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        return [
            FirstAuditAsset(
                audit_id=(row.get("Audit_ID") or "").strip(),
                sku=(row.get("SKU") or "").strip(),
                concept=(row.get("Concept") or "").strip(),
                production_file=(row.get("Production_File") or "").strip(),
                source_file=(row.get("Source_File") or "").strip(),
                action=(row.get("Etsy_Archive_Action") or "KEEP_OUT_OF_ETSY_ARCHIVE").strip(),
            )
            for row in reader
            if (row.get("SKU") or "").strip()
        ]


def write_blocklist(assets: list[FirstAuditAsset]) -> None:
    BLOCKLIST.parent.mkdir(parents=True, exist_ok=True)
    with BLOCKLIST.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "Audit_ID",
                "SKU",
                "Concept",
                "Production_File",
                "Source_File",
                "Required_Action",
                "Reason",
            ],
        )
        writer.writeheader()
        for asset in assets:
            writer.writerow(
                {
                    "Audit_ID": asset.audit_id,
                    "SKU": asset.sku,
                    "Concept": asset.concept,
                    "Production_File": asset.production_file,
                    "Source_File": asset.source_file,
                    "Required_Action": "KEEP_OUT_OF_PUBLIC_MARKETPLACE_ARCHIVE",
                    "Reason": "Top studio asset reserved for The First Audit: 001.",
                }
            )


def public_queue_files() -> list[Path]:
    candidates: list[Path] = []
    for path in DATABASE.glob("*.csv"):
        name = path.name.lower()
        if any(hint in name for hint in PRIVATE_ALLOW_HINTS):
            continue
        if any(hint in name for hint in PUBLIC_QUEUE_HINTS):
            candidates.append(path)
    return sorted(candidates)


def audit_file(path: Path, assets: list[FirstAuditAsset]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    try:
        with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames:
                return findings
            for idx, row in enumerate(reader, start=2):
                row_blob = " | ".join(str(v or "") for v in row.values()).lower().replace("\\", "/")
                for asset in assets:
                    matched = sorted(marker for marker in asset.markers if marker and marker in row_blob)
                    if matched:
                        findings.append(
                            {
                                "Queue_File": str(path.relative_to(ROOT)),
                                "Row_Number": str(idx),
                                "SKU": asset.sku,
                                "Audit_ID": asset.audit_id,
                                "Matched_Marker": matched[0],
                                "Action": "HOLD_AND_REMOVE_FROM_PUBLIC_QUEUE",
                                "Note": "First Audit studio asset appeared in a public queue candidate.",
                            }
                        )
    except UnicodeDecodeError as exc:
        findings.append(
            {
                "Queue_File": str(path.relative_to(ROOT)),
                "Row_Number": "",
                "SKU": "",
                "Audit_ID": "",
                "Matched_Marker": "",
                "Action": "REVIEW_FILE_ENCODING",
                "Note": str(exc),
            }
        )
    return findings


def write_audit(findings: list[dict[str, str]], scanned: list[Path], assets: list[FirstAuditAsset]) -> None:
    AUDIT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = ["Queue_File", "Row_Number", "SKU", "Audit_ID", "Matched_Marker", "Action", "Note"]
    with AUDIT_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for finding in findings:
            writer.writerow(finding)

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    status = "FAIL - leaks found" if findings else "PASS - no public queue leaks found"
    lines = [
        "# First Audit Guard Report",
        "",
        f"Generated: {et_now()}",
        f"Status: {status}",
        f"Protected assets: {len(assets)}",
        f"Public queue files scanned: {len(scanned)}",
        f"Findings: {len(findings)}",
        "",
        "Rule: THE FIRST AUDIT: 001 assets are private Studio inventory. They must not be placed into Etsy Archive, eBay, low-price digital bundles, or generic Printify public queues.",
        "",
        "Outputs:",
        f"- {BLOCKLIST.relative_to(ROOT)}",
        f"- {AUDIT_CSV.relative_to(ROOT)}",
        "",
    ]
    if findings:
        lines.extend(["## Findings", ""])
        for finding in findings[:50]:
            lines.append(
                f"- {finding['Queue_File']} row {finding['Row_Number']}: {finding['SKU']} -> {finding['Action']}"
            )
        if len(findings) > 50:
            lines.append(f"- ... {len(findings) - 50} more findings in CSV.")
    else:
        lines.extend(
            [
                "## Result",
                "",
                "No protected First Audit SKU or source/production filename was found in the public queue candidates scanned.",
            ]
        )
    AUDIT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> int:
    assets = read_manifest()
    write_blocklist(assets)
    scanned = public_queue_files()
    findings: list[dict[str, str]] = []
    for path in scanned:
        findings.extend(audit_file(path, assets))
    write_audit(findings, scanned, assets)
    print(f"First Audit guard: assets={len(assets)} scanned={len(scanned)} findings={len(findings)}")
    print(f"blocklist={BLOCKLIST}")
    print(f"audit={AUDIT_CSV}")
    print(f"report={AUDIT_MD}")
    return 2 if findings else 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-findings", action="store_true", help="Return success even if public leaks are found.")
    args = parser.parse_args()
    code = run()
    if args.allow_findings:
        code = 0
    raise SystemExit(code)


if __name__ == "__main__":
    main()
