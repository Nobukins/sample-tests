# search_script.py
import pytest
import sys
import os
from playwright.async_api import async_playwright, Page, expect
import asyncio

# pytest_asyncioを必須としてチェック
try:
    import pytest_asyncio
except ImportError:
    print("pytest_asyncioがインストールされていません。以下のコマンドでインストールしてください：")
    print("pip install pytest-asyncio")
    sys.exit(1)

# プラグイン設定
pytest_plugins = ["pytest_asyncio"]

# コマンドラインオプションの設定
def pytest_addoption(parser):
    parser.addoption("--query", action="store", default=None, help="検索するキーワード")
    parser.addoption("--slowmo", action="store", type=int, default=0, help="スローモーションの遅延（ミリ秒）")
    parser.addoption("--bykilt-slowmo", action="store", type=int, default=0, help="Bykiltが使用するスローモーション設定")
    parser.addoption("--headless", action="store_true", default=False, help="ヘッドレスモードで実行")

# ブラウザフィクスチャを追加
@pytest.fixture(scope="function")
async def browser_fixture(request):
    # スローモーション設定の取得（bykilt-slowmoが優先）
    slowmo = request.config.getoption("--bykilt-slowmo", default=0)
    if slowmo == 0:
        slowmo = request.config.getoption("--slowmo", default=0)
    
    # デフォルト値を設定
    headless = request.config.getoption("--headless", default=False)
    
    # PlaywrightとBrowserを初期化
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=headless,
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
    
    # テスト後のクリーンアップ
    yield browser
    
    await browser.close()
    await playwright.stop()

@pytest.mark.asyncio
async def test_text_search(request, browser_fixture) -> None:
    """Yahoo検索のテスト"""
    # ブラウザフィクスチャを使用
    browser = browser_fixture
    
    # 検索クエリの取得
    query = request.config.getoption("--query")
    if not query:
        pytest.skip("検索クエリが提供されていません。--queryで検索語を指定してください。")
    
    # コンテキストとページの作成
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        # Yahoo検索の実行
        print(f"「{query}」をYahooで検索します...")
        await page.goto("https://www.yahoo.co.jp/")
        await page.get_by_role("searchbox", name="検索したいキーワードを入力してください").click()
        await page.get_by_role("searchbox", name="検索したいキーワードを入力してください").fill(query)
        await page.get_by_role("button", name="検索").click()
        
        # 検索結果が表示されるまで待機
        await page.wait_for_timeout(3000)
        print("検索が完了しました")
        
    finally:
        # 常にコンテキストを閉じる
        await context.close()

if __name__ == "__main__":
    # コマンドラインから直接実行された場合の処理
    import sys
    sys.argv = [sys.argv[0]] + ["--query", "テスト検索"]
    pytest.main(["-xvs", __file__])