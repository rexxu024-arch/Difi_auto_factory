"""Build Project Mirror vision/LLM distillation job scaffolds.

The job file is intentionally conservative: it queues only source candidates
for human/QA acceptance first. Actual vision calls should run only after a
local reference image path is present and the source is marked ACCEPTED_SOURCE.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
REVIEW_DIR = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"
INDEX_CSV = DATABASE_DIR / "Aesthetic_DNA_Pool_Index.csv"
JOBS_CSV = DATABASE_DIR / "Project_Mirror_Distillation_Jobs.csv"
PROMPT_MD = REVIEW_DIR / "PROJECT_MIRROR_VISION_DISTILLER_PROMPT.md"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"

JOB_HEADERS = [
    "Job_ID",
    "Niche",
    "Sample_ID",
    "Source_URL",
    "Local_File",
    "Status",
    "Vision_Model",
    "Distillation_Prompt_Profile",
    "Output_DNA_ID",
    "Notes",
]


def now_et() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def build_jobs() -> list[dict[str, str]]:
    rows = read_rows(INDEX_CSV)
    jobs = []
    for row in rows:
        if row.get("Status") not in {"SOURCE_CANDIDATE_REVIEW", "ACCEPTED_SOURCE"}:
            continue
        has_file = bool(row.get("Local_File"))
        status = "READY_FOR_VISION" if row.get("Status") == "ACCEPTED_SOURCE" and has_file else "WAITING_ACCEPTED_IMAGE"
        jobs.append(
            {
                "Job_ID": f"PM-DISTILL-{len(jobs) + 1:03d}",
                "Niche": row.get("Niche", ""),
                "Sample_ID": row.get("Sample_ID", ""),
                "Source_URL": row.get("Source_URL", ""),
                "Local_File": row.get("Local_File", ""),
                "Status": status,
                "Vision_Model": "defer: gpt/gemini vision after accepted local image",
                "Distillation_Prompt_Profile": "material-light-composition-buyer-intent",
                "Output_DNA_ID": "",
                "Notes": row.get("Notes", ""),
            }
        )
    return jobs


def write_jobs(jobs: list[dict[str, str]]) -> None:
    with JOBS_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=JOB_HEADERS)
        writer.writeheader()
        writer.writerows(jobs)


def write_prompt() -> None:
    text = """# Project Mirror Vision Distiller Prompt

Role: You are OpenClaw's aesthetic DNA distiller. Analyze the image only as a reference for material, light, composition, and buyer intent. Do not copy the image, do not describe it as provenance, and do not produce marketplace claims.

Return strict JSON:

{
  "physical_material_parameters": {
    "roughness": "",
    "translucency": "",
    "metal_behavior": "",
    "texture_frequency": "",
    "surface_wear": "",
    "refractive_depth": ""
  },
  "light_distribution_matrix": {
    "key_light_angle": "",
    "color_temperature": "",
    "fill_ratio": "",
    "shadow_decay": "",
    "specular_highlight_placement": ""
  },
  "composition_rules": [],
  "purchase_intent_word_cluster": [],
  "negative_prompt_cluster": [],
  "mentor_hub_dna": {
    "category": "",
    "layout": "",
    "title": "",
    "gold_prompt_dna": "",
    "material_keywords": ""
  },
  "mj_prompt_reference_derived": "",
  "qa_risks": []
}
"""
    PROMPT_MD.parent.mkdir(parents=True, exist_ok=True)
    PROMPT_MD.write_text(text, encoding="utf-8")


def append_progress(jobs: list[dict[str, str]]) -> None:
    counts: dict[str, int] = {}
    for job in jobs:
        counts[job["Status"]] = counts.get(job["Status"], 0) + 1
    msg = (
        f"\n## {now_et().strftime('%Y-%m-%d %H:%M ET')} - Project Mirror Distiller Scaffold\n"
        f"- Built `{JOBS_CSV.name}` with {len(jobs)} jobs: {counts}.\n"
        f"- Wrote strict JSON vision prompt `{PROMPT_MD}`.\n"
        "- Actual vision calls remain blocked until accepted local reference images exist.\n"
    )
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(msg)


def main() -> int:
    jobs = build_jobs()
    write_jobs(jobs)
    write_prompt()
    append_progress(jobs)
    print({"jobs": len(jobs), "ready_for_vision": sum(1 for j in jobs if j["Status"] == "READY_FOR_VISION")})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
