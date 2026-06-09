# -*- coding: utf-8 -*-
"""Inspect checkout page structure to find correct selectors"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

PRODUCT_URL = "https://staging.tongdaiwifi.vn/thiet-bi-thong-minh/access-point-ac1200t-test"

def go_checkout(page):
    page.goto(PRODUCT_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(2000)
    # Handle location popup
    try:
        for kw in ["Chọn khu vực", "Chọn tỉnh"]:
            popup = page.locator(f"text={kw}").first
            if popup.is_visible(timeout=1500):
                for hcm in ["Hồ Chí Minh", "TP. Hồ Chí Minh"]:
                    el = page.locator(f"text={hcm}").first
                    if el.count() > 0 and el.is_visible(timeout=1500): el.click(); break
                page.wait_for_timeout(500)
                el = page.locator("text=Bến Thành").first
                if el.count() > 0: el.click()
                page.wait_for_timeout(500)
                for btn in ["button:has-text('Xác nhận')", "button:has-text('OK')"]:
                    b = page.locator(btn).first
                    if b.count() > 0: b.click(); break
                page.wait_for_timeout(1000)
                break
    except: pass
    page.locator("button:has-text('Mua ngay'), a:has-text('Mua ngay')").first.click()
    page.wait_for_url("**/checkout/**", timeout=15000)
    page.wait_for_timeout(2000)
    return page.url

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False, slow_mo=100)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    url = go_checkout(page)
    print(f"Checkout URL: {url}\n")

    # 1. Find back button
    print("=== BACK BUTTON / NAVIGATION ===")
    for sel in ["[class*='back']", "button[aria-label*='back']", ".back", "svg[class*='arrow']",
                "[class*='arrow-left']", "[class*='return']"]:
        el = page.locator(sel)
        n = el.count()
        if n > 0:
            for i in range(min(n, 3)):
                try:
                    txt = el.nth(i).get_attribute("class") or ""
                    print(f"  [{sel}][{i}] class='{txt[:100]}' visible={el.nth(i).is_visible()}")
                except: pass

    # 2. Find payment section
    print("\n=== PAYMENT / PTTT SECTION ===")
    for kw in ["Phương thức", "thanh toán", "payment", "PTTT"]:
        els = page.locator(f"*:has-text('{kw}')").all()
        if els:
            for el in els[:3]:
                try:
                    tag = el.evaluate("el => el.tagName")
                    cls = el.get_attribute("class") or ""
                    txt = el.inner_text()[:50]
                    print(f"  tag={tag} class='{cls[:60]}' text='{txt}'")
                except: pass

    # 3. Find điều khoản link
    print("\n=== ĐIỀU KHOẢN LINK ===")
    for sel in ["a", "span[role='link']", "[class*='term']", "[class*='policy']"]:
        els = page.locator(sel).all()
        for el in els[:10]:
            try:
                txt = el.inner_text().strip()
                if any(k in txt.lower() for k in ["điều khoản", "điều kiện", "terms", "policy"]):
                    href = el.get_attribute("href") or ""
                    cls = el.get_attribute("class") or ""
                    print(f"  sel={sel} text='{txt}' href='{href}' class='{cls[:60]}'")
            except: pass

    # 4. Find product summary / tên gói in right panel
    print("\n=== PRODUCT SUMMARY (right panel) ===")
    for sel in ["[class*='summary']", "[class*='order-summary']", "[class*='cart']",
                "[class*='bill']", "[class*='product']", "aside", "[class*='right']"]:
        el = page.locator(sel).first
        if el.count() > 0 and el.is_visible(timeout=500):
            try:
                txt = el.inner_text()[:200]
                cls = el.get_attribute("class") or ""
                print(f"  [{sel}] class='{cls[:60]}' text='{txt[:100]}'")
            except: pass

    # 5. Find address / province dropdown
    print("\n=== ĐỊA CHỈ / PROVINCE DROPDOWN ===")
    page.wait_for_timeout(1000)
    for sel in ["select", "[role='combobox']", "[class*='select']", "[class*='province']",
                "[class*='dropdown']", "input[placeholder*='tỉnh'], input[placeholder*='Tỉnh']",
                "input[placeholder*='Thành phố']", "[class*='ant-select']"]:
        try:
            els = page.locator(sel).all()
            for el in els[:5]:
                if el.is_visible(timeout=500):
                    tag = el.evaluate("el => el.tagName")
                    cls = el.get_attribute("class") or ""
                    ph = el.get_attribute("placeholder") or ""
                    txt = el.inner_text()[:50] if tag != "INPUT" else el.input_value()[:50]
                    print(f"  [{sel}] tag={tag} class='{cls[:60]}' ph='{ph}' text='{txt}'")
        except: pass

    # 6. Find radio buttons for address type
    print("\n=== ADDRESS TYPE RADIO (Nhà riêng / Chung cư) ===")
    for sel in ["input[type='radio']", "[role='radio']", "[class*='radio']"]:
        els = page.locator(sel).all()
        for el in els[:10]:
            try:
                label = el.evaluate("el => el.labels ? el.labels[0]?.textContent : ''") or ""
                val = el.get_attribute("value") or ""
                cls = el.get_attribute("class") or ""
                print(f"  [{sel}] value='{val}' label='{label}' class='{cls[:60]}'")
            except: pass

    # 7. Find Ghi chú field
    print("\n=== GHI CHÚ / NOTE FIELD ===")
    for sel in ["textarea", "input[placeholder*='Ghi']", "input[placeholder*='ghi']",
                "[placeholder*='chú']", "[placeholder*='ọi']"]:
        els = page.locator(sel).all()
        for el in els[:5]:
            try:
                ph = el.get_attribute("placeholder") or ""
                cls = el.get_attribute("class") or ""
                print(f"  [{sel}] ph='{ph}' class='{cls[:60]}' visible={el.is_visible()}")
            except: pass

    # 8. Find Họ tên clear button / X button
    print("\n=== HỌ TÊN FIELD + CLEAR BUTTON ===")
    name_field = page.locator("input[placeholder*='Họ'], input[placeholder*='họ'], input[placeholder*='tên'], input[placeholder*='Tên']").first
    if name_field.count() > 0:
        name_field.fill("test")
        page.wait_for_timeout(500)
        print(f"  Name field found: ph='{name_field.get_attribute('placeholder')}' class='{name_field.get_attribute('class') or ''}' ")
        # Look for nearby clear/X buttons
        for sel in ["button", "span[class*='clear']", "[class*='icon']", "[class*='close']", "svg"]:
            els = page.locator(sel).all()
            for el in els[:20]:
                try:
                    cls = el.get_attribute("class") or ""
                    aria = el.get_attribute("aria-label") or ""
                    if any(k in cls.lower() for k in ["clear", "close", "delete", "x", "remove"]) or \
                       any(k in aria.lower() for k in ["clear", "close", "delete"]):
                        print(f"  Possible X: {sel} class='{cls[:60]}' aria='{aria}' visible={el.is_visible()}")
                except: pass

    # 9. Get page source snippet of form area
    print("\n=== FORM AREA HTML SNIPPET ===")
    form_html = page.evaluate("""() => {
        const form = document.querySelector('form, [class*="form"], main');
        return form ? form.innerHTML.substring(0, 3000) : 'no form found';
    }""")
    print(form_html[:3000])

    input("\nPress Enter to close browser...")
    browser.close()
