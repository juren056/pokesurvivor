"""Touch-emulated Chromium capture, explicitly not real-phone certification."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from capture_media import RAW, login, partner, shot


with sync_playwright() as p:
    browser=p.chromium.launch()
    ctx=browser.new_context(viewport={'width':844,'height':390},has_touch=True,is_mobile=True,
                            device_scale_factor=1,locale='en-US',record_video_dir=str(RAW/'touch'),
                            record_video_size={'width':844,'height':390})
    page=ctx.new_page();page.set_default_timeout(12000)
    login(page);partner(page)
    page.locator('#scr-menu [data-go=settings]').click()
    page.locator('#set-tabs [data-t=ctl]').click();page.wait_for_timeout(500)
    shot(page,'mobile-touch-settings','Touch settings in Chromium mobile emulation (844 × 390), not a physical-phone test.',['mobile'])
    page.locator('#set-close').click();page.locator('#scr-menu [data-go=play]').click();page.wait_for_timeout(3000)
    shot(page,'mobile-landscape','Landscape game layout in touch-enabled Chromium emulation.',['mobile'])
    cdp=ctx.new_cdp_session(page)
    for i in range(4):
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':200,'y':220}]})
        cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':270 if i%2==0 else 130,'y':220}]})
        page.wait_for_timeout(1200)
        if i==0:shot(page,'mobile-joystick','Dragging on the play area reveals the virtual joystick in this emulated session.',['mobile'])
        cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    page.wait_for_timeout(700)
    # Touch the visible pause control; its rendered canvas hit region is defined by touch.js.
    page.keyboard.press('Escape');page.wait_for_timeout(300)
    shot(page,'mobile-paused','Paused solo run in the landscape emulation.',['mobile'])
    page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(700)
    shot(page,'mobile-rotate','The game asks a touch device in portrait orientation to rotate. Emulated browser capture.',['mobile'])
    page.set_viewport_size({'width':844,'height':390});page.wait_for_timeout(500)
    video=page.video;ctx.close();video.save_as(str(RAW/'mobile-touch.webm'));browser.close()
