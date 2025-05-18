from playwright.sync_api import sync_playwright


def get_cf_cookies():
    for i in range(5):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)…"
            )
            page = context.new_page()
            page.goto("https://pump.fun/")
            cookies = {c["name"]: c["value"] for c in context.cookies()}
            browser.close()
            if "__cf_bm" not in cookies or "cf_clearance" not in cookies:
                continue
            return cookies
    raise RuntimeError("Failed to get cookies after 3 attempts.")
