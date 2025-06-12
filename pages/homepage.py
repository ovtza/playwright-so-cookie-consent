from playwright.sync_api import Page, expect
import pytest

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.customize_button = page.get_by_role("button", name="Dostosuj", exact=True)
        self.analytics_switch = page.get_by_role("switch", name="Cookies analityczne")
        self.accept_selected_button = page.get_by_role("button", name="Zaakceptuj zaznaczone", exact=True)

    def go_to(self):
        self.page.goto("https://www.ing.pl", wait_until="load")

        if self.page.locator("text=Request unsuccessful.").is_visible():
            pytest.skip("Access was blocked (possibly due to CAPTCHA or bot detection). Test skipped.")

    def open_cookie_settings(self):
        self.customize_button.click()
        expect(self.analytics_switch).to_be_visible()

    def enable_analytics_cookie(self):
        if 'aria-checked="false"' in self.analytics_switch.inner_html():
            self.analytics_switch.locator("span").first.click()

    def accept_selected(self):
        self.accept_selected_button.click()
