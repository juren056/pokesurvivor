"""Browser checks for V14 localized Orb tables and responsive controls."""
import os
from playwright.sync_api import sync_playwright

BASE = os.environ.get("V14_BASE", "http://127.0.0.1:4173")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width, height in ((1280, 900), (390, 844)):
        page = browser.new_page(viewport={"width": width, "height": height})
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        for locale, marker in (("es", "25 puntos porcentuales"), ("it", "25 punti percentuali"), ("zh-hant", "25 個百分點")):
            page.goto(f"{BASE}/{locale}/orbs/", wait_until="networkidle")
            assert page.locator("table caption").count() == 1
            assert page.locator("tbody tr").count() == 6
            assert marker in page.locator("table").inner_text()
            assert page.locator('[data-orb-planner]').count() == 1
            checks = page.locator('[data-orb-planner] input[type="checkbox"]')
            for i in range(4): checks.nth(i).check()
            checks.nth(4).click()
            assert sum(checks.nth(i).is_checked() for i in range(6)) == 4
            assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
        assert not errors, "Browser errors: " + " | ".join(errors)
        page.close()
    browser.close()

print("PASS V14 browser: 24 localized effects, single DOM table, four-slot limit and responsive widths valid.")
