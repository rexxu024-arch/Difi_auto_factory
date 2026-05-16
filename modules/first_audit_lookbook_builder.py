from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont, JpegImagePlugin  # noqa: F401


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "Review_Packets"
DATABASE = ROOT / "Database"
OUT_DIR = REVIEW / "First_Audit_001"
NY_TZ = ZoneInfo("America/New_York")


KEEP_SKUS = {
    "OC-NYC-ARCHIVE-011": ("THE FIRST AUDIT: 001-01", "Entrance", 48, "Archival Studio Print"),
    "OC-NYC-ARCHIVE-012": ("THE FIRST AUDIT: 001-02", "Anchor", 295, "Optical Acrylic Monument"),
    "OC-NYC-EPIC-001": ("THE FIRST AUDIT: 001-03", "Core", 128, "Optical Acrylic Relic"),
    "OC-NYC-EPIC-004": ("THE FIRST AUDIT: 001-04", "Core", 128, "Optical Acrylic Relic"),
    "OC-NYC-CYBER-005": ("THE FIRST AUDIT: 001-05", "Core", 128, "Optical Acrylic Relic"),
    "OC-NYC-ASSASSIN-008": ("THE FIRST AUDIT: 001-06", "Anchor", 295, "Masterwork Acrylic Relic"),
    "OC-NYC-ASSASSIN-010": ("THE FIRST AUDIT: 001-07", "Anchor", 295, "Masterwork Acrylic Relic"),
    "OC-NYC-MUSEUM-020": ("THE FIRST AUDIT: 001-08", "Core", 128, "Optical Acrylic Relic"),
    "OC-NYC-AMERICANA-016": ("THE FIRST AUDIT: 001-09", "Entrance", 48, "Archival Studio Print"),
}

EXCLUDE_SKUS = {
    "OC-NYC-ARCHIVE-014",
    "OC-NYC-ASSASSIN-009",
    "OC-NYC-CYBERPOP-023",
}


@dataclass
class AuditAsset:
    sku: str
    audit_id: str
    tier: str
    price: int
    studio_medium: str
    concept: str
    product_vector: str
    blueprint_id: str
    provider_id: str
    variant_id: str
    base_cost: str
    shipping: str
    source_file: Path
    production_file: Path
    printify_product_id: str
    decision_note: str


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def index_by_sku(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {r.get("Final_SKU") or r.get("SKU") or "": r for r in rows if (r.get("Final_SKU") or r.get("SKU"))}


def resolve_path(value: str) -> Path:
    p = Path(value.replace("\\", "/"))
    if not p.is_absolute():
        p = ROOT / p
    return p


def collect_assets() -> list[AuditAsset]:
    zone2 = index_by_sku(read_csv(DATABASE / "Shock_And_Awe_V5_Printify_Private_Drafts.csv"))
    zones13 = index_by_sku(read_csv(DATABASE / "Shock_And_Awe_V5_Zones1_3_Printify_Private_Drafts.csv"))
    decisions = index_by_sku(read_csv(REVIEW / "SHOCK_AWE_GEMINI_DECISIONS.csv"))
    rows = {**zone2, **zones13}
    assets: list[AuditAsset] = []
    for sku, (audit_id, tier, price, studio_medium) in KEEP_SKUS.items():
        row = rows.get(sku)
        if not row:
            continue
        production = resolve_path(row.get("Production_Design_File") or row.get("Selected_File") or "")
        source = resolve_path(row.get("Selected_File") or row.get("Production_Design_File") or "")
        if not production.exists() and source.exists():
            production = source
        if not production.exists():
            continue
        decision = decisions.get(sku, {})
        concept = row.get("Concept_Name") or decision.get("Concept") or sku
        assets.append(
            AuditAsset(
                sku=sku,
                audit_id=audit_id,
                tier=tier,
                price=price,
                studio_medium=studio_medium,
                concept=concept,
                product_vector=row.get("Product_Vector", ""),
                blueprint_id=row.get("Blueprint_ID", ""),
                provider_id=row.get("Provider_ID", ""),
                variant_id=row.get("Variant_ID", ""),
                base_cost=row.get("Base_Cost_USD", ""),
                shipping=row.get("Shipping_USD", ""),
                source_file=source,
                production_file=production,
                printify_product_id=row.get("Printify_Product_ID", ""),
                decision_note=(decision.get("Required_Action") or row.get("QA_Note") or "Selected for First Audit review."),
            )
        )
    return assets


def write_manifest(assets: list[AuditAsset]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = DATABASE / "First_Audit_001_Asset_Manifest.csv"
    fields = [
        "Audit_ID",
        "SKU",
        "Concept",
        "Tier",
        "Studio_Medium",
        "Price_USD",
        "Printify_Vector",
        "Blueprint_ID",
        "Provider_ID",
        "Variant_ID",
        "Base_Cost_USD",
        "Shipping_USD",
        "Printify_Product_ID",
        "Production_File",
        "Source_File",
        "Decision_Note",
        "Etsy_Archive_Action",
        "Studio_Action",
    ]
    with manifest.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for a in assets:
            w.writerow(
                {
                    "Audit_ID": a.audit_id,
                    "SKU": a.sku,
                    "Concept": a.concept,
                    "Tier": a.tier,
                    "Studio_Medium": a.studio_medium,
                    "Price_USD": a.price,
                    "Printify_Vector": a.product_vector,
                    "Blueprint_ID": a.blueprint_id,
                    "Provider_ID": a.provider_id,
                    "Variant_ID": a.variant_id,
                    "Base_Cost_USD": a.base_cost,
                    "Shipping_USD": a.shipping,
                    "Printify_Product_ID": a.printify_product_id,
                    "Production_File": str(a.production_file),
                    "Source_File": str(a.source_file),
                    "Decision_Note": a.decision_note,
                    "Etsy_Archive_Action": "KEEP_OUT_OF_ETSY_ARCHIVE",
                    "Studio_Action": "FIRST_AUDIT_SHORTLIST",
                }
            )


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size=size)
    return ImageFont.load_default()


def fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, fnt: ImageFont.ImageFont) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def cover_page() -> Image.Image:
    page = Image.new("RGB", (1600, 2200), "#0d0d0d")
    d = ImageDraw.Draw(page)
    d.rectangle((80, 80, 1520, 2120), outline="#b8a15e", width=3)
    d.text((140, 260), "OPENCLAW DESIGN STUDIO", fill="#c9c1b0", font=font(38))
    d.text((140, 430), "THE FIRST AUDIT: 001", fill="#f3eee3", font=font(92))
    d.text((140, 560), "New York / Optical Relics / Archival Studio Prints", fill="#b8a15e", font=font(42))
    body = (
        "A cold gallery draft for private review. The archive is stripped of marketplace noise: "
        "no discount language, no low-end carrier objects, no public-platform SEO posture. "
        "Only the pieces capable of carrying a physical price ladder remain."
    )
    y = 820
    for line in fit_text(d, body, 1180, font(38)):
        d.text((140, y), line, fill="#d8d1c3", font=font(38))
        y += 58
    d.text((140, 1680), "PRICE FIRMWARE", fill="#b8a15e", font=font(34))
    d.text((140, 1760), "$48  /  Entrance Studio Print", fill="#f3eee3", font=font(44))
    d.text((140, 1840), "$128 /  Core Optical Acrylic Relic", fill="#f3eee3", font=font(44))
    d.text((140, 1920), "$295 /  Anchor Masterwork Acrylic", fill="#f3eee3", font=font(44))
    d.text((140, 2050), datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M ET"), fill="#777066", font=font(28))
    return page


def asset_page(asset: AuditAsset) -> Image.Image:
    page = Image.new("RGB", (1600, 2200), "#111111")
    d = ImageDraw.Draw(page)
    img = Image.open(asset.production_file).convert("RGB")
    img.thumbnail((980, 1320), Image.Resampling.LANCZOS)
    x = 80 + (980 - img.width) // 2
    y = 170 + (1320 - img.height) // 2
    d.rectangle((70, 160, 1070, 1500), fill="#171717", outline="#2b2b2b", width=2)
    page.paste(img, (x, y))
    d.text((1120, 180), asset.audit_id, fill="#b8a15e", font=font(38))
    d.text((1120, 260), asset.concept.upper(), fill="#f2eee4", font=font(42))
    d.text((1120, 390), f"${asset.price}", fill="#f2eee4", font=font(76))
    d.text((1120, 500), asset.studio_medium, fill="#c9c1b0", font=font(32))
    details = [
        f"SKU: {asset.sku}",
        f"Tier: {asset.tier}",
        f"Printify: {asset.product_vector}",
        f"Blueprint: {asset.blueprint_id} / {asset.provider_id} / {asset.variant_id}",
        f"Cost+ship: ${asset.base_cost} + ${asset.shipping}",
    ]
    yy = 660
    for item in details:
        for line in fit_text(d, item, 390, font(28)):
            d.text((1120, yy), line, fill="#c9c1b0", font=font(28))
            yy += 42
        yy += 16
    d.line((1120, 1040, 1510, 1040), fill="#3b3322", width=2)
    note = asset.decision_note or "Selected for First Audit review."
    yy = 1100
    d.text((1120, yy), "AUDIT NOTE", fill="#b8a15e", font=font(28))
    yy += 54
    for line in fit_text(d, note, 390, font(27))[:8]:
        d.text((1120, yy), line, fill="#d8d1c3", font=font(27))
        yy += 42
    d.text((80, 1620), "STUDIO POSITIONING", fill="#b8a15e", font=font(30))
    copy = (
        "Reserved for studio presentation. Not eligible for Etsy archive placement. "
        "The buyer-facing offer is a physical object, an atmosphere, and a status signal."
    )
    yy = 1685
    for line in fit_text(d, copy, 1360, font(32)):
        d.text((80, yy), line, fill="#d8d1c3", font=font(32))
        yy += 50
    d.text((80, 2070), str(asset.production_file), fill="#5c5c5c", font=font(22))
    return page


def write_pdf(assets: list[AuditAsset]) -> None:
    pages = [cover_page()] + [asset_page(a) for a in assets]
    pdf = OUT_DIR / "THE_FIRST_AUDIT_001_LOOKBOOK.pdf"
    jpgs: list[Image.Image] = []
    for p in pages:
        jpgs.append(p.convert("RGB"))
    jpgs[0].save(pdf, save_all=True, append_images=jpgs[1:], resolution=160.0)
    # Save contact preview as well.
    preview = OUT_DIR / "THE_FIRST_AUDIT_001_CONTACT_SHEET.jpg"
    thumbs = []
    for a in assets:
        img = Image.open(a.production_file).convert("RGB")
        img.thumbnail((300, 420), Image.Resampling.LANCZOS)
        tile = Image.new("RGB", (340, 510), "#111111")
        tile.paste(img, ((340 - img.width) // 2, 20))
        dd = ImageDraw.Draw(tile)
        dd.text((18, 450), a.audit_id[-5:], fill="#b8a15e", font=font(20))
        dd.text((18, 475), f"${a.price} {a.tier}", fill="#f2eee4", font=font(20))
        thumbs.append(tile)
    cols = 3
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 340, rows * 510), "#0d0d0d")
    for i, t in enumerate(thumbs):
        sheet.paste(t, ((i % cols) * 340, (i // cols) * 510))
    sheet.save(preview, quality=92)


def write_markdown(assets: list[AuditAsset]) -> None:
    md = OUT_DIR / "THE_FIRST_AUDIT_001_LOOKBOOK.md"
    lines = [
        "# THE FIRST AUDIT: 001",
        "",
        f"Generated: {datetime.now(NY_TZ).strftime('%Y-%m-%d %H:%M ET')}",
        "",
        "Studio rule: Etsy is a digital resource archive. The First Audit is a private physical-asset series.",
        "",
        "Pricing firmware: $48 entrance print, $128 core optical acrylic, $295 anchor masterwork.",
        "",
        "## Shortlist",
        "",
    ]
    for a in assets:
        lines += [
            f"### {a.audit_id} - {a.concept}",
            f"- SKU: `{a.sku}`",
            f"- Tier / Price: {a.tier} / `${a.price}`",
            f"- Medium: {a.studio_medium}",
            f"- Printify vector: {a.product_vector} (`{a.blueprint_id}/{a.provider_id}/{a.variant_id}`)",
            f"- Cost + ship: `${a.base_cost}` + `${a.shipping}`",
            f"- Product draft: `{a.printify_product_id}`",
            f"- Production file: `{a.production_file}`",
            f"- Audit note: {a.decision_note}",
            "- Etsy archive: exclude",
            "",
        ]
    md.write_text("\n".join(lines), encoding="utf-8")


def write_strategy_files(assets: list[AuditAsset]) -> None:
    state_path = DATABASE / "First_Audit_001_State.json"
    state = {
        "protocol": "V13.0_HIGH_ATELIER_FIRST_AUDIT",
        "updated_at_et": datetime.now(NY_TZ).isoformat(timespec="seconds"),
        "studio_brand": "OpenClaw Design Studio",
        "series": "THE FIRST AUDIT: 001",
        "etsy_archive_candidate_names": ["Digital Relic Archive", "Apothecary Resource Vault"],
        "etsy_archive_role": "low-price digital resource warehouse only",
        "studio_role": "New York atelier for physical acrylic relics and archival studio prints",
        "banned_studio_carriers": ["mug", "notebook", "phone case"],
        "allowed_studio_carriers": ["optical acrylic block", "archival studio print", "premium framed poster"],
        "price_firmware_usd": {"entrance": 48, "core": 128, "anchor": 295},
        "first_audit_count": len(assets),
        "lookbook_pdf": str(OUT_DIR / "THE_FIRST_AUDIT_001_LOOKBOOK.pdf"),
        "manifest_csv": str(DATABASE / "First_Audit_001_Asset_Manifest.csv"),
    }
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    assets = collect_assets()
    write_manifest(assets)
    write_markdown(assets)
    write_pdf(assets)
    write_strategy_files(assets)
    print(f"[FIRST_AUDIT] assets={len(assets)}")
    print(f"[FIRST_AUDIT] manifest={DATABASE / 'First_Audit_001_Asset_Manifest.csv'}")
    print(f"[FIRST_AUDIT] pdf={OUT_DIR / 'THE_FIRST_AUDIT_001_LOOKBOOK.pdf'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
