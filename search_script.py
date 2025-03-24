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
async def test_text_search(request) -> None:
    query = request.config.getoption("--query")
    slowmo = request.config.getoption("--slowmo")
    if not query:
        pytest.skip("No query provided. Use --query to specify a search term.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, 
            slow_mo=slowmo, 
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-zygote',
                '--single-process'
            ]
        )  
        context = await browser.new_context()
        page = await context.new_page()

        # Yahoo検索処理
        await page.goto("https://www.yahoo.co.jp/")
        await page.get_by_role("searchbox", name="検索したいキーワードを入力してください").click()
        await page.get_by_role("searchbox", name="検索したいキーワードを入力してください").fill(query)
        await page.get_by_role("button", name="検索").click()
        await page.locator("#contents").click()

        await page.wait_for_timeout(3000)

        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_text_search(None))