# -*- coding: utf-8 -*-
"""Inspect full popover HTML and test province selection"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

PRODUCT_URL = "https://staging.tongdaiwifi.vn/thiet-bi-thong-minh/access-point-ac1200t-test"

def go_checkout(page):
    page.goto(PRODUCT_URL, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3000)
    try:
        if page.locator("text=Chọn khu vực").first.is_visible(timeout=1200):
            page.locator("text=Hồ Chí Minh").first.click(); page.wait_for_timeout(500)
            page.locator("text=Bến Thành").first.click(); page.wait_for_timeout(500)
            page.locator("button:has-text('Xác nhận')").first.click(); page.wait_for_timeout(800)
    except: pass
    page.locator("button:has-text('Mua ngay'), a:has-text('Mua ngay')").first.click()
    page.wait_for_url("**/checkout/**", timeout=20000)
    page.wait_for_timeout(2000)
    return page.url

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False, slow_mo=100)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    go_checkout(page)
    page.locator("input[placeholder='Nhập họ tên']").first.fill("Test User")
    page.locator("input[placeholder*='điện thoại'], input[placeholder*='Điện thoại']").first.fill("0901234567")
    page.wait_for_timeout(500)
    page.evaluate("window.scrollTo(0,400)"); page.wait_for_timeout(500)

    print("=== CLICKING PROVINCE BUTTON ===")
    btn = page.locator("button[aria-haspopup]:has-text('Chọn tỉnh thành phố')").first
    if btn.count() > 0:
        btn.click(); page.wait_for_timeout(1000)
        print("  Clicked!")
    else:
        print("  NOT FOUND - trying button[aria-expanded='false']")
        btn2 = page.locator("button[aria-expanded='false']:has-text('Chọn')").first
        if btn2.count() > 0:
            btn2.click(); page.wait_for_timeout(1000); print("  Clicked btn2!")

    print("\n=== FULL POPOVER HTML ===")
    html = page.evaluate("""() => {
        const p = document.querySelector('[data-radix-popper-content-wrapper]');
        return p ? p.innerHTML.substring(0, 5000) : 'NONE';
    }""")
    print(html)

    print("\n=== OPTION ELEMENTS IN POPOVER ===")
    popover = page.locator("[data-radix-popper-content-wrapper]").first
    if popover.count() > 0:
        for sel in ["button", "li", "div[class*='item']", "span", "[role='option']",
                    "p", "[tabindex]", "a"]:
            els = popover.locator(sel).all()
            vis = [e for e in els if e.is_visible(timeout=100)]
            if vis:
                first_txt = vis[0].inner_text()[:50].strip().replace('\n', ' ')
                print(f"  [{sel}] total={len(els)} visible={len(vis)} first='{first_txt}'")

    print("\n=== TYPE 'Hồ' AND CHECK ===")
    search_in = page.locator("[data-radix-popper-content-wrapper] input").first
    if search_in.count() > 0:
        print(f"  Found search input! placeholder={search_in.get_attribute('placeholder')}")
        search_in.fill("Hồ"); page.wait_for_timeout(800)
        # Check options again
        popover = page.locator("[data-radix-popper-content-wrapper]").first
        for sel in ["button", "li", "div[class*='item']", "[tabindex='0']", "[tabindex='-1']"]:
            els = popover.locator(sel).all()
            vis = [e for e in els if e.is_visible(timeout=100)]
            if vis:
                first_txt = vis[0].inner_text()[:50].strip().replace('\n', ' ')
                print(f"  After filter [{sel}] visible={len(vis)} first='{first_txt}'")

        print("\n=== CLICK FIRST VISIBLE ITEM AFTER SEARCH ===")
        # Try to click Hồ Chí Minh
        for sel in ["button:has-text('Hồ Chí Minh')", "li:has-text('Hồ Chí Minh')",
                    "span:has-text('Hồ Chí Minh')", "*:has-text('Hồ Chí Minh')"]:
            el = popover.locator(sel).first
            if el.count() > 0 and el.is_visible(timeout=500):
                tag = el.evaluate("e => e.tagName")
                print(f"  Found {tag}:has-text('Hồ Chí Minh') — clicking")
                el.click(); page.wait_for_timeout(500)
                print(f"  After click page text near TP: {page.evaluate(chr(40)+'() => document.body.innerText.substring(document.body.innerText.indexOf(\"Tỉnh\"),document.body.innerText.indexOf(\"Tỉnh\")+200)'+chr(41))}")
                break

    print("\n=== CHECK PHUONG XA AFTER TP SELECTED ===")
    page.wait_for_timeout(1000)
    body = page.evaluate("() => document.body.innerText")
    if "Phường" in body or "phường" in body:
        idx = body.find("Phường")
        if idx < 0: idx = body.find("phường")
        print(body[max(0,idx-100):idx+200])
    else:
        print("  Phường/Xã NOT found in page text!")

    print("\n=== ALL button[aria-haspopup] AFTER TP SELECTED ===")
    for btn in page.locator("button[aria-haspopup]").all():
        if btn.is_visible(timeout=200):
            txt = btn.inner_text()[:50].strip().replace('\n',' ')
            print(f"  aria-haspopup: '{txt}'")

    print("Done!")
    browser.close()
