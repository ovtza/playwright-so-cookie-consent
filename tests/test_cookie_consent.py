import os
import pytest
from playwright.sync_api import sync_playwright
from pages.homepage import HomePage

expected_cookies = [
    "cookiePolicyGDPR",
    "cookiePolicyGDPR__details",
    "cookiePolicyINCPS"
]

@pytest.fixture(scope="function")
def homepage():
    browser_name = os.getenv("BROWSER", "chromium")
    headed = os.getenv("HEADED", "").lower() == "true"

    with sync_playwright() as p:
        if browser_name == "edge":
            browser = p.chromium.launch(channel="msedge", headless=not headed)
        else:
            browser = getattr(p, browser_name).launch(headless=not headed)

        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        home = HomePage(page)

        try:
            yield home, context, browser
        finally:
            context.tracing.stop(path=f"trace-{browser_name}.zip")
            context.close()
            browser.close()

def test_cookie_consent_flow(homepage):
    home, context, _ = homepage

    home.go_to()
    initial_cookies = context.cookies()
    initial_names = [cookie["name"] for cookie in initial_cookies]

    for expected in expected_cookies:
        assert expected not in initial_names, f"Cookie '{expected}' should not exist before consent!"

    home.open_cookie_settings()
    home.enable_analytics_cookie()
    home.accept_selected()

    final_cookies = context.cookies()
    final_names = [cookie["name"] for cookie in final_cookies]

    for expected in expected_cookies:
        assert expected in final_names, f"Expected cookie '{expected}' not found after consent!"
