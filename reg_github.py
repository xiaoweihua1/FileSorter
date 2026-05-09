import asyncio
from playwright.async_api import async_playwright

async def main():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            executable_path=edge_path,
            channel="msedge",
        )
        page = await browser.new_page()
        
        await page.goto("https://github.com/signup", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(3000)
        
        # 填邮箱
        await page.locator("#email").fill("3263173839@qq.com")
        await page.wait_for_timeout(500)
        
        # 点Continue
        btns = page.locator("button[type='submit']")
        count = await btns.count()
        for i in range(count):
            text = await btns.nth(i).inner_text()
            if "Continue" in text and "Google" not in text and "Apple" not in text:
                await btns.nth(i).click()
                break
        
        await page.wait_for_timeout(3000)
        
        # 填密码
        await page.locator("#password").fill("awei031212")
        # 填用户名
        await page.locator("#login").fill("weihua-file")
        
        print("🎉 表单已填好！邮箱/密码/用户名全部就绪")
        print("浏览器已打开，您直接操作就行，我不会关它了")
        print("验证码到了告诉我，我帮您填")
        
        # 浏览器保持打开，不关
        while True:
            await asyncio.sleep(10)

asyncio.run(main())
