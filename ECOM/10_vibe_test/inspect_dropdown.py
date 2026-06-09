# -*- coding: utf-8 -*-
"""Inspect dropdown structure after clicking province combobox"""
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
    page.locator("input[placeholder='Nhập họ tên']").first.fill("Chúc ngủ ngon nha")
    page.locator("input[type='tel'], input[placeholder*='điện thoại']").first.fill("0901234567")
    page.wait_for_timeout(500)
    page.evaluate("window.scrollTo(0,400)"); page.wait_for_timeout(500)

    print("=== COMBOBOX ELEMENTS BEFORE CLICK ===")
    for sel in ["[role='combobox']", "button[aria-haspopup]", "button[aria-expanded]", "[aria-autocomplete]"]:
        els = page.locator(sel).all()
        for i, el in enumerate(els[:5]):
            try:
                txt = el.inner_text()[:60].strip().replace('\n', ' ')
                cls = (el.get_attribute("class") or "")[:60]
                tag = el.evaluate("e => e.tagName")
                aria = el.get_attribute("aria-expanded") or ""
                role = el.get_attribute("role") or ""
                vis = el.is_visible(timeout=200)
                print(f"  [{sel}][{i}] tag={tag} role={role} aria-exp={aria} vis={vis} text='{txt[:40]}' cls='{cls[:40]}'")
            except: pass

    print("\n=== CLICK PROVINCE COMBOBOX ===")
    # Try [role='combobox'] first
    combos = page.locator("[role='combobox']").all()
    print(f"  Found {len(combos)} combobox elements")
    clicked = False
    for i, el in enumerate(combos[:10]):
        try:
            if el.is_visible(timeout=300):
                txt = el.inner_text()[:60].strip().replace('\n', ' ')
                print(f"  Combobox[{i}] visible text='{txt[:50]}'")
                if "tỉnh" in txt.lower() or "thành phố" in txt.lower() or "Chọn" in txt:
                    print(f"  → Clicking this one")
                    el.click(); page.wait_for_timeout(1000); clicked = True; break
        except: pass

    if not clicked:
        # Try p.line-clamp-1 parent
        p_el = page.locator("p.line-clamp-1").first
        if p_el.count() > 0:
            print(f"  → Clicking p.line-clamp-1 parent")
            parent = p_el.locator("xpath=..")
            parent.click(); page.wait_for_timeout(1000); clicked = True

    print("\n=== AFTER CLICK - OPTIONS ELEMENTS ===")
    for sel in ["[role='option']", "[role='listbox']", "[cmdk-item]", "[cmdk-list]",
                "[data-radix-popper-content-wrapper]", "[data-state='open'][role='listbox']",
                "li[role='option']", "[role='presentation'] li", "[aria-selected]",
                "ul li", "[data-value]"]:
        try:
            els = page.locator(sel).all()
            count = len(els)
            if count > 0:
                first_txt = els[0].inner_text()[:40].strip().replace('\n', ' ') if els else ""
                print(f"  [{sel}] count={count} first='{first_txt}'")
        except: pass

    print("\n=== FULL HTML OF OPEN DROPDOWN ===")
    try:
        # Find popover/portal content
        html = page.evaluate("""() => {
            const portal = document.querySelector('[data-radix-popper-content-wrapper]') ||
                           document.querySelector('[role="listbox"]') ||
                           document.querySelector('[cmdk-root]');
            return portal ? portal.innerHTML.substring(0, 2000) : 'NO PORTAL FOUND';
        }""")
        print(html[:2000])
    except Exception as e:
        print(f"  Error: {e}")

    print("\n=== BODY innerText (search area) ===")
    try:
        txt = page.evaluate("() => document.body.innerText")
        # Find relevant section
        idx = txt.find("Tỉnh")
        if idx >= 0: print(txt[max(0,idx-200):idx+500])
    except: pass

    input("\nPress Enter to close...")
    browser.close()
