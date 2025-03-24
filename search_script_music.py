# search_script_music.py 
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

    # 録画ディレクトリの設定（環境変数から取得するか、デフォルト値を使用）
    recording_dir = os.environ.get("RECORDING_PATH", "./tmp/record_videos")
    os.makedirs(recording_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成
    
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
        # 録画オプションを指定してコンテキストを作成
        context = await browser.new_context(
            record_video_dir=recording_dir,
            record_video_size={"width": 1280, "height": 720}  # 録画解像度
        )
        page = await context.new_page()

        # Beatport検索とTop10の連続再生
        await page.goto("https://musicsite/")
        await page.get_by_role("button", name="I Accept").click()
        await page.get_by_test_id("header-search-input").click()
        await page.get_by_test_id("header-search-input").fill(query)
        await page.goto("https://musicsite/genre/minimal")
        await page.locator(".XXXX-XXXX-XXXX > .XXXXX-XXXXX-XXXX").first.click()

        await page.wait_for_timeout(10000)

        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_text_search(None))
