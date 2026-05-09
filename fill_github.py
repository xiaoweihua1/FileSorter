import asyncio
from playwright.async_api import async_playwright

async def main():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            executable_path=edge_path,
        )
        page = await browser.new_page()
        
        await page.goto("https://github.com/signup")
        await page.wait_for_timeout(2000)
        
        # 填写邮箱
        email_input = page.locator('input[id="email"]')
        if await email_input.count() > 0:
            await email_input.fill('3263173839@qq.com')
            print("✅ 邮箱已填写")
        
        await page.wait_for_timeout(1000)
        
        # 点击 Continue
        continue_btn = page.locator('button:has-text("Continue")')
        if await continue_btn.count() > 0:
            await continue_btn.click()
            print("✅ 已点击Continue")
            await page.wait_for_timeout(2000)
        
        # 填密码
        password_input = page.locator('input[id="password"]')
        if await password_input.count() > 0:
            await password_input.fill('awei031212')
            print("✅ 密码已填写")
        
        await page.wait_for_timeout(500)
        
        # 填用户名
        username_input = page.locator('input[id="login"]')
        if await username_input.count() > 0:
            await username_input.fill('weihua')
            print("✅ 用户名已填写")
        
        await page.wait_for_timeout(500)
        
        await page.screenshot(path=r"C:\Users\AWEI\Desktop\github_filled.png")
        print("\n✅ 表单已填写完毕，截图保存在桌面 github_filled.png")
        print("请查看浏览器页面，可能需要完成验证码或点击 Continue")
        
        input("按回车键关闭浏览器...")
        await browser.close()

asyncio.run(main())
