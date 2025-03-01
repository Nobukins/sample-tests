def login(page,password):
    page.goto("https://example.com/login")
    page.fill("#username", "testuser")
    page.fill("#password", password)
    page.click("#login-button")
login(page)