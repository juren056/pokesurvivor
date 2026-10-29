"""Regression checks for the October 25 V14 release."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "wiki" / "dist"


def page(route: str) -> str:
    return (OUT / route.strip("/") / "index.html").read_text(encoding="utf-8")


home = page("")
assert "2026-10-30" in home
assert "Halloween, mobile aim & safer saves" in home

english_orbs = page("orbs")
assert english_orbs.count("<caption class=\"sr-only\">All six Mystery Dungeon Orbs</caption>") == 1
assert "25 percentage points" in english_orbs
assert "1.4 for 10 seconds" in english_orbs

locale_expectations = {
    "es": ("Efecto verificado", "25 puntos porcentuales", "Multiplica la velocidad"),
    "it": ("Effetto verificato", "25 punti percentuali", "Moltiplica la velocità"),
    "zh-hant": ("已核對效果", "25 個百分點", "移動速度乘以 1.4"),
}
for locale, expected in locale_expectations.items():
    orb = page(f"{locale}/orbs")
    assert expected[0] in orb
    assert all(text in orb for text in expected)
    assert "Sleep for 4 seconds" not in orb
    assert orb.count('data-orb-planner') == 1

for route, issue, anchor in (
    ("save-recovery", "issues/331", "login-preserve-progress"),
    ("co-op", "issues/333", "friend-username-not-found"),
    ("gacha-calculator", "issues/334", "ticket-units"),
    ("arceus-judgment", "issues/332", "leaderboard-run-missing"),
):
    html = page(route)
    assert issue in html and f'id="{anchor}"' in html
    for locale in locale_expectations:
        localized = page(f"{locale}/{route}")
        assert issue in localized and f'id="{anchor}"' in localized

updates = page("updates")
assert "October 25 player-report review" in updates
assert "not a new official game release" in updates

sitemap = ET.parse(OUT / "sitemap.xml")
ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
urls = sitemap.findall(f"{ns}url")
assert len(urls) == 108
loc_to_lastmod = {u.findtext(f"{ns}loc"): u.findtext(f"{ns}lastmod") for u in urls}
for route in ("", "orbs/", "save-recovery/", "co-op/", "gacha-calculator/", "arceus-judgment/", "updates/"):
    assert loc_to_lastmod[f"https://pokemonsurvivorwiki.com/{route}"] >= "2026-10-25"

print("PASS V14: localized Orb effects, four scoped reports, October 25 dates and 108-URL sitemap valid.")
