"""Create an eBay seller-profile update packet from the selected brand shell."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
ETSY_PACKET = DATABASE_DIR / "Etsy_shop_update_packet.md"
OUT_MD = DATABASE_DIR / "eBay_Profile_Update_Packet.md"


def now_text() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")


def extract_asset(label: str, text: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip().startswith(label):
            for follow in lines[index + 1 : index + 4]:
                value = follow.strip()
                if value and not value.startswith("#"):
                    return value
    return ""


def build() -> str:
    packet = ETSY_PACKET.read_text(encoding="utf-8") if ETSY_PACKET.exists() else ""
    icon = extract_asset("Shop Icon:", packet)
    banner = extract_asset("Big Banner:", packet)
    return "\n".join(
        [
            "# eBay Profile Update Packet",
            "",
            f"Generated: {now_text()} America/New_York",
            "",
            "## Purpose",
            "",
            "Improve buyer trust and visual consistency for the current eBay shop while traffic experiments continue.",
            "",
            "## Brand Direction",
            "",
            "Quiet Relic Studio: premium small-batch art objects for zen study corners, dark academia rooms, jade-inspired decor, acrylic desk objects, matte wall art, and collectible sticker sheets.",
            "",
            "## Assets To Use",
            "",
            f"- Seller profile image / logo: `{icon}`",
            f"- Optional banner/reference visual: `{banner}`",
            "",
            "## Seller Bio Draft",
            "",
            "Quiet Relic Studio creates small-batch wall art, acrylic desk objects, and sticker sheets inspired by jade textures, scholar rooms, quiet ritual objects, kintsugi repair, and wabi-sabi detail. Each item is produced on demand through trusted production partners and curated as part of a focused visual collection.",
            "",
            "## Buyer-Facing Note",
            "",
            "The main image on each listing shows the actual product customers receive. Additional gallery images may show concept, detail, or collection-reference views and are not extra products or selectable variations unless the listing explicitly says so.",
            "",
            "## Suggested Shop Categories",
            "",
            "- Scholar Wall Art",
            "- Acrylic Desk Objects",
            "- Sticker Sheets",
            "- Zen Study Decor",
            "- Dark Academia Gifts",
            "",
            "## Apply Rule",
            "",
            "- This packet is safe to apply manually or through browser automation when eBay Seller Hub is stable.",
            "- Do not change payment settings, shipping/payment policies, active listing prices, or order settings from this packet.",
            "",
        ]
    )


def main() -> None:
    OUT_MD.write_text(build(), encoding="utf-8")
    print(f"[EBAY-PROFILE-PACKET] {OUT_MD}")


if __name__ == "__main__":
    main()
