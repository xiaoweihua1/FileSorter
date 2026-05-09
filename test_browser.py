import asyncio, sys
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="msedge",
        )
        page = await browser.new_page()
        await page.goto("https://www.baidu.com", timeout=30000)
        await page.screenshot(path=r"C:\Users\AWEI\Desktop\test_baidu.png")
        print("✅ 浏览器能正常工作！")
        await page.wait_for_timeout(10000)
        await browser.close()

asyncio.run(test())
