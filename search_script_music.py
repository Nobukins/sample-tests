# search_script.py 
import pytest
from playwright.async_api import async_playwright, Page, expect
import asyncio
import os

pytest_plugins = ["pytest_asyncio"]  # Add this line to enable async test support

def pytest_addoption(parser):
    parser.addoption("--query", action="store", default=None, help="Search query to use")
    parser.addoption("--slowmo", action="store", type=int, default=0, help="Slow motion delay in milliseconds")

@pytest.mark.asyncio  # This mark will now be recognized
async def test_beatport_search(request) -> None:
    query = request.config.getoption("--query")
    slowmo = request.config.getoption("--slowmo")
    if not query:
        pytest.skip("No query provided. Use --query to specify a search term.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=slowmo)
        context = await browser.new_context()
        page = await context.new_page()

        # Beatport検索とTop10の連続再生
        await page.goto("https://www.beatport.com/")
        await page.get_by_role("button", name="I Accept").click()
        await page.get_by_test_id("header-search-input").click()
        await page.get_by_test_id("header-search-input").fill(query)
        await page.goto("https://www.beatport.com/genre/minimal-deep-tech/14")
        await page.locator(".CollectionControls-style__Controls-sc-3a6a5b4a-0 > .Play-style__Control-sc-bdba3bac-0").first.click()

        await page.wait_for_timeout(10000)

        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_beatport_search(None))