"""Regression checks for the October 24 evening V13 review."""
from pathlib import Path
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "wiki" / "dist"


def page(route: str) -> str:
    return (OUT / route.strip("/") / "index.html").read_text(encoding="utf-8")


home = page("")
assert "2026-10-30" in home

shop = page("kecleon-shop")
assert "Kecleon Shop or Daily Missions Not Resetting?" in shop
assert "not evidence of a failed purchase" in shop
assert "purchase problem" not in shop

coop = page("co-op")
assert "Connected but Stuttering: Multiplayer Lag Reports" in coop
assert "issues/325" in coop and "issues/306" in coop

save = page("save-recovery")
assert "Why Does the Same Account Show Different Progress in Another Browser?" in save
assert 'id="save-source-browser"' in save and 'id="save-target-browser"' in save
assert "issues/327" in save

updates = page("updates")
assert "Three dates used on this page" in updates
assert "is a site-review date" in updates
assert "Source review updated October 23" not in updates

for locale in ("es", "it", "zh-hant"):
    orb = page(f"{locale}/orbs")
    assert "Select up to four different Orb types" not in orb
    assert 'data-orb-planner' in orb
    localized_shop = page(f"{locale}/kecleon-shop")
    localized_coop = page(f"{locale}/co-op")
    localized_save = page(f"{locale}/save-recovery")
    assert "issues/320" in localized_shop
    assert "issues/325" in localized_coop
    assert "issues/327" in localized_save

# Fixed shiny examples requested by the execution plan.
for rate, pulls, expected in (
    (0.01, 10, 9.5617924991),
    (0.02, 10, 18.2927193112),
    (0.01, 100, 63.3967658727),
    (0.02, 100, 86.7380444105),
):
    actual = (1 - math.pow(1 - rate, pulls)) * 100
    assert abs(actual - expected) < 1e-9

sitemap = ET.parse(OUT / "sitemap.xml")
urls = sitemap.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
assert len(urls) == 108
locs = [u.findtext("{http://www.sitemaps.org/schemas/sitemap/0.9}loc") for u in urls]
assert len(locs) == len(set(locs))
assert all("?" not in loc and "#" not in loc for loc in locs)
assert "https://pokemonsurvivorwiki.com/orbs/" in locs

print("PASS V13: evidence corrections, four-language diagnostics, fixed probability examples, 108-URL sitemap and October 24 review date valid.")
