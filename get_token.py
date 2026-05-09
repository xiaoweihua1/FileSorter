import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        
        print(f"URL: {page.url}")
        
        if "login" in page.url:
            print("登录中...")
            await page.locator("#login_field").fill("xiaoweihua1")
            await page.locator("#password").fill("awei031212")
            await page.locator("input[type='submit']").click()
            await page.wait_for_timeout(3000)
        
        await page.goto("https://github.com/settings/tokens/new", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)
        
        await page.locator("#token_name").fill("FileSorter_push")
        await page.locator("input#repo").first.check()
        await page.wait_for_timeout(500)
        await page.locator("button:has-text('Generate token')").first.click()
        await page.wait_for_timeout(3000)
        
        await page.screenshot(path=r"C:\Users\AWEI\Desktop\token_done.png")
        
        # 获取token
        try:
            token_input = page.locator("input[readonly]")
            if await token_input.count() > 0:
                token = await token_input.get_attribute("value")
                if token:
                    with open(r"C:\Users\AWEI\Desktop\token.txt", "w") as f:
                        f.write(token)
                    print(f"✅ Token: {token[:8]}...{token[-4:]}")
        except:
            pass
        
        print("✅ 完成，查看桌面 token_done.png 和 token.txt")
        await browser.close()

asyncio.run(main())
