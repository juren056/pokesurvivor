"""Focused browser checks for the October 23 V11 release."""
import os

from playwright.sync_api import sync_playwright


BASE = os.environ.get("POKESURVIVOR_TEST_BASE", "http://127.0.0.1:8765")
EXPECTED = {
    "": {
        "coins": "Coins missing or not syncing between phone and PC?",
        "result": "no single trusted copy is confirmed",
        "lag": "Still connected but lagging?",
        "lag_result": "still connected",
        "mobile": "Why is Manual Aim unavailable with a controller on mobile?",
    },
    "es": {
        "coins": "¿Faltan monedas o no se sincronizan entre el móvil y el PC?",
        "result": "no hay una copia fiable confirmada",
        "lag": "¿Sigue habiendo lag después de la reconexión?",
        "lag_result": "Sigues conectado",
        "mobile": "¿Por qué no aparece Apuntar a mano con mando en móvil?",
    },
    "it": {
        "coins": "Monete mancanti o non sincronizzate tra telefono e PC?",
        "result": "non è confermata una copia affidabile",
        "lag": "Lag anche dopo la correzione?",
        "lag_result": "Sei ancora connesso",
        "mobile": "Perché Mira manuale non appare con un controller su mobile?",
    },
    "zh-hant": {
        "coins": "手機與電腦金幣不同步，或突然顯示 0？",
        "result": "無法確認唯一可信副本",
        "lag": "重連修正後仍然卡頓？",
        "lag_result": "目前仍有連線",
        "mobile": "為什麼手機接手把後仍沒有手動瞄準？",
    },
}


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))

    for locale, copy in EXPECTED.items():
        prefix = f"/{locale}" if locale else ""

        page.goto(f"{BASE}{prefix}/save-recovery/", wait_until="load")
        assert copy["coins"] in page.locator("main").inner_text()
        page.locator("#save-symptom").select_option("coins_differ")
        page.locator("#save-copy").select_option("unknown")
        page.locator("[data-diagnostic-run]").click()
        assert copy["result"] in page.locator("#save-result").inner_text()
        assert page.locator("#save-report").input_value().strip()
        assert page.evaluate(
            "document.documentElement.scrollWidth <= document.documentElement.clientWidth"
        )

        page.goto(f"{BASE}{prefix}/co-op/", wait_until="load")
        assert copy["lag"] in page.locator("main").inner_text()
        page.locator("#coop-stage").select_option("lag")
        page.locator("[data-coop-run]").click()
        assert copy["lag_result"] in page.locator("#coop-result").inner_text()

        page.goto(f"{BASE}{prefix}/mobile/", wait_until="load")
        assert copy["mobile"] in page.locator("main").inner_text()
        assert page.evaluate(
            "document.documentElement.scrollWidth <= document.documentElement.clientWidth"
        )

    assert not errors, errors
    browser.close()

print("PASS: V11 save, co-op and mobile additions work in four locales at 390px.")
