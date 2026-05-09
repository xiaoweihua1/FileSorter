import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="msedge")
        page = await browser.new_page()
        
        # 登录GitHub
        await page.goto("https://github.com/login")
        await page.locator("#login_field").fill("xiaoweihua1")
        await page.locator("#password").fill("awei031212")
        await page.locator("input[type='submit']").click()
        await page.wait_for_timeout(3000)
        
        # 打开token创建页面
        await page.goto("https://github.com/settings/tokens/new")
        print("已打开token页面，浏览器保持打开")
        
        # 保持浏览器打开，不关
        while True:
            await asyncio.sleep(10)

asyncio.run(main())
