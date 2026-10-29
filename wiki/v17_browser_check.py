"""Responsive browser checks for V17 current guidance and localized surfaces."""
import os
from playwright.sync_api import sync_playwright

BASE = os.environ.get("V17_BASE", "http://127.0.0.1:4173")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width, height in ((1280, 900), (430, 932), (390, 844), (375, 812)):
        page = browser.new_page(viewport={"width": width, "height": height})
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        for route, marker in (
            ("/mobile/", "Anchored or Floating joystick?"),
            ("/es/updates/", "cuatro días"),
            ("/it/save-recovery/", "25 secondi"),
            ("/zh-hant/orbs/", "新手該帶哪四種寶珠"),
        ):
            page.goto(BASE + route, wait_until="networkidle")
            assert marker in page.locator("main").inner_text()
            assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
        assert not errors, "Browser errors: " + " | ".join(errors)
        page.close()
    browser.close()

print("PASS V17 browser: current guidance renders without console errors or horizontal overflow at 1280/430/390/375.")
