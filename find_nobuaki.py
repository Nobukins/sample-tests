import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://nogtips.wordpress.com/")
    page.get_by_role("link", name="Slide04").click()
    page.locator("body").click()
    page.goto("https://nogtips.wordpress.com/")
    page.get_by_role("link", name="Slide05").click()
