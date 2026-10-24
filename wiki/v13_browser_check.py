"""Headless interaction checks for V13 tools and localized output."""
import os
from playwright.sync_api import sync_playwright

BASE = os.environ.get("V13_BASE", "http://127.0.0.1:4173")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: errors.append(str(exc)))

    page.goto(BASE + "/arceus-judgment/", wait_until="networkidle")
    assert page.locator("#plate-type option").count() == 17
    assert page.locator('#plate-type option[value="normal"]').count() == 0
    assert "Arceus" in page.locator("#plate-result").inner_text()

    page.goto(BASE + "/gacha-calculator/", wait_until="networkidle")
    assert "9.56%" in page.locator("#gacha-result").inner_text()
    page.select_option("#gacha-pulls", "100")
    assert "63.40%" in page.locator("#gacha-result").inner_text()

    page.goto(BASE + "/orbs/", wait_until="networkidle")
    checks = page.locator('[data-orb-planner] input[type="checkbox"]')
    assert checks.count() == 6
    for i in range(4): checks.nth(i).check()
    checks.nth(4).click()
    assert sum(checks.nth(i).is_checked() for i in range(6)) == 4
    assert "4/4" in page.locator("#orb-result").inner_text()

    for locale in ("es", "it", "zh-hant"):
        page.goto(f"{BASE}/{locale}/orbs/", wait_until="networkidle")
        orb_text = page.locator("[data-orb-planner]").inner_text()
        assert "Select up to four" not in orb_text
        page.locator('[data-orb-planner] input[type="checkbox"]').first.check()
        result = page.locator("#orb-result").inner_text()
        assert "slots selected" not in result and "Up to three uses" not in result

        page.goto(f"{BASE}/{locale}/gacha-calculator/", wait_until="networkidle")
        gacha = page.locator("#gacha-result").inner_text()
        assert "At least one rarity" not in gacha and "Hard pity" not in gacha

        page.goto(f"{BASE}/{locale}/arceus-judgment/", wait_until="networkidle")
        plate = page.locator("#plate-result").inner_text()
        assert "super effective" not in plate and "neutral" not in plate

    page.goto(BASE + "/save-recovery/", wait_until="networkidle")
    page.select_option("#save-source-browser", "opera")
    page.select_option("#save-target-browser", "firefox")
    page.click("[data-diagnostic-run]")
    report = page.locator("#save-report").input_value()
    assert "Source browser category: Opera" in report
    assert "Target browser category: Firefox" in report

    page.goto(BASE + "/builds/?p=4&m=ember", wait_until="networkidle")
    assert page.locator("#build-starter").input_value() == "4"
    assert page.locator("#build-result").inner_text().strip()

    assert not errors, "Browser errors: " + " | ".join(errors)
    browser.close()

print("PASS V13 browser: Plate, gacha, Orbs, localization, save report, legacy build link and mobile viewport valid.")
