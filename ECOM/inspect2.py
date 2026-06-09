# -*- coding: utf-8 -*-
"""Inspect address section and other missing elements"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

PRODUCT_URL = "https://staging.tongdaiwifi.vn/thiet-bi-thong-minh/access-point-ac1200t-test"

def go_checkout(page):
    page.goto(PRODUCT_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(2000)
    try:
        for kw in ["Chọn khu vực"]:
            popup = page.locator(f"text={kw}").first
            if popup.is_visible(timeout=1200):
                el = page.locator("text=Hồ Chí Minh").first
                if el.count() > 0: el.click()
                page.wait_for_timeout(500)
                el = page.locator("text=Bến Thành").first
                if el.count() > 0: el.click()
                page.wait_for_timeout(500)
                page.locator("button:has-text('Xác nhận')").first.click()
                page.wait_for_timeout(800)
                break
    except: pass
    page.locator("button:has-text('Mua ngay')").first.click()
    page.wait_for_url("**/checkout/**", timeout=15000)
    page.wait_for_timeout(2000)
    return page.url

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False, slow_mo=100)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    url = go_checkout(page)
    print(f"URL: {url}\n")

    # Fill personal info first
    page.locator("input[placeholder='Nhập họ tên']").first.fill("Chúc ngủ ngon nha")
    page.locator("input[placeholder*='điện thoại'], input[type='tel']").first.fill("0901234567")
    page.wait_for_timeout(500)

    # Scroll down gradually
    for scroll_y in [300, 600, 900, 1200, 1500, 2000]:
        page.evaluate(f"window.scrollTo(0, {scroll_y})")
        page.wait_for_timeout(500)

    print("=== ALL ACCORDION SECTIONS ===")
    accordions = page.locator("[data-slot='accordion-item'], [data-orientation='vertical']").all()
    for i, acc in enumerate(accordions[:20]):
        try:
            txt = acc.inner_text()[:100].replace('\n', ' ')
            state = acc.get_attribute("data-state") or ""
            print(f"  [{i}] state={state} text='{txt[:80]}'")
        except: pass

    print("\n=== SCROLLED PAGE - ALL VISIBLE TEXT SECTIONS ===")
    page.evaluate("window.scrollTo(0, 1000)")
    page.wait_for_timeout(500)
    all_text = page.evaluate("() => document.body.innerText")
    print(all_text[:3000])

    print("\n=== LOOK FOR ĐỊA CHỈ SECTION ===")
    for kw in ["Địa chỉ lắp đặt", "Địa chỉ", "Tỉnh", "Phường", "Nhà riêng", "Chung cư"]:
        els = page.get_by_text(kw).all()
        for el in els[:3]:
            try:
                if el.is_visible(timeout=300):
                    cls = el.get_attribute("class") or ""
                    tag = el.evaluate("el => el.tagName")
                    print(f"  '{kw}' → tag={tag} class='{cls[:60]}'")
            except: pass

    print("\n=== LOOK FOR ĐIỀU KHOẢN LINK (scroll all the way) ===")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1000)
    for sel in ["a[href*='policy']", "a[href*='term']", "a.text-brand-blue-primary",
                "a:has-text('điều khoản')"]:
        try:
            el = page.locator(sel).first
            if el.count() > 0:
                txt = el.inner_text()[:50]
                href = el.get_attribute("href") or ""
                vis = el.is_visible(timeout=500)
                print(f"  [{sel}] text='{txt}' href='{href}' visible={vis}")
        except: pass

    print("\n=== PHONE FIELD CLEAR BUTTON ===")
    phone = page.locator("input[type='tel'], input[placeholder*='điện thoại']").first
    if phone.count() > 0:
        phone.scroll_into_view_if_needed()
        phone.fill("0901234")
        page.wait_for_timeout(500)
        # Look for clear button near phone
        parent_html = page.evaluate("""(el) => {
            let p = el.parentElement;
            for(let i=0;i<4;i++){ if(p) p = p.parentElement; }
            return p ? p.innerHTML.substring(0,500) : '';
        }""", phone.element_handle())
        print(f"  Phone parent HTML: {parent_html[:300]}")
        clear_btns = page.locator("button[aria-label='Clear']").all()
        print(f"  Clear buttons: {len(clear_btns)}")
        for i, btn in enumerate(clear_btns[:5]):
            try:
                vis = btn.is_visible(timeout=300)
                print(f"  Clear[{i}] visible={vis} bbox={btn.bounding_box()}")
            except: pass

    input("\nPress Enter to close...")
    browser.close()
