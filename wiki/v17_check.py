"""Regression checks for the October 30 V17 release."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "wiki" / "dist"


def page(route: str) -> str:
    return (OUT / route.strip("/") / "index.html").read_text(encoding="utf-8")


home = page("")
assert "2026-10-30" in home
assert "Halloween, mobile aim & safer saves" in home

mobile = page("mobile")
assert "Settings → Accessibility" in mobile
assert "Anchored or Floating joystick?" in mobile
assert "Manual Aim is not available" not in mobile
assert "Mobile Manual Aim was removed" not in mobile

save = page("save-recovery")
download = page("download")
updates = page("updates")
assert "25-second cloud rule" in save
assert "automatic-save schedule" in save
assert "65 seconds" not in save
assert "at least 25 seconds" in download
assert "2026-11-03 00:00 Europe/Madrid" in updates
assert "2026-11-03 07:00" in updates
assert "official planned window" in updates

for route in ("how-to-play", "starters", "builds"):
    assert "A practical 0–7 minute route" in page(route)
assert "When is this tier list updated?" in page("tier-list")
assert "issues/373" in page("co-op") and "issues/377" in page("co-op")
assert "Which four Orbs should a beginner carry?" in page("orbs")

locale_markers = {
    "es": ("cuatro días", "Anclado", "25 segundos"),
    "it": ("quattro giorni", "Ancorato", "25 secondi"),
    "zh-hant": ("四天視窗", "錨定", "25 秒"),
}
for locale, markers in locale_markers.items():
    combined = page(f"{locale}/updates") + page(f"{locale}/mobile") + page(f"{locale}/save-recovery")
    assert all(marker in combined for marker in markers)
    assert 'id="first-seven-minutes"' in page(f"{locale}/how-to-play")
    assert 'id="tier-update-method"' in page(f"{locale}/tier-list")
    assert 'id="leaderboard-group-report"' in page(f"{locale}/co-op")
    assert 'id="beginner-orb-loadout"' in page(f"{locale}/orbs")

assert 'id="identity-check"' in page("zh-hant/survivor-vs-burst")
assert 'id="first-seven-minutes"' in page("es/starter-tier-list")

manifest = json.loads((ROOT / "wiki" / "data" / "v17-source-manifest.json").read_text(encoding="utf-8"))
assert manifest["policy"]["networkDependencyDuringBuild"] is False
assert manifest["policy"]["onMissingUpstream"] == "keep-last-validated-snapshot"
assert manifest["upstream"]["currentMainChangelogPath"]["status"] == "missing"
assert manifest["upstream"]["cloudSave"]["normalMinimumGapMs"] == 25000
assert manifest["upstream"]["halloween"]["endUtcExclusive"] == "2026-11-02T23:00:00Z"

start = datetime(2026, 10, 29, 23, 0, tzinfo=timezone.utc)
end = datetime(2026, 11, 2, 23, 0, tzinfo=timezone.utc)
status = lambda at: "upcoming" if at < start else "official-planned-window" if at < end else "ended"
assert status(datetime(2026, 10, 29, 22, 59, 59, tzinfo=timezone.utc)) == "upcoming"
assert status(start) == "official-planned-window"
assert status(datetime(2026, 11, 2, 22, 59, 59, tzinfo=timezone.utc)) == "official-planned-window"
assert status(end) == "ended"

game = json.loads((ROOT / "wiki" / "data" / "game.json").read_text(encoding="utf-8"))
assert game["rules"]["cloudSave"]["minUploadGapMs"] == 25000
assert game["rules"]["cloudSave"]["hiddenScheduledRuleGapMs"] == 21000

sitemap = ET.parse(OUT / "sitemap.xml")
ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
urls = sitemap.findall(f"{ns}url")
assert len(urls) == 108
lastmods = {u.findtext(f"{ns}loc"): u.findtext(f"{ns}lastmod") for u in urls}
changed = ("", "mobile/", "save-recovery/", "download/", "updates/", "how-to-play/", "starters/", "builds/", "tier-list/", "co-op/", "orbs/", "survivor-vs-burst/")
for prefix in ("", "es/", "it/", "zh-hant/"):
    for route in changed:
        assert lastmods[f"https://pokemonsurvivorwiki.com/{prefix}{route}"] == "2026-10-30"
assert lastmods["https://pokemonsurvivorwiki.com/pokedex/"] != "2026-10-30"

print("PASS V17: current mobile/save/event facts, localized answer depth, source fallback and 108-URL sitemap valid.")
