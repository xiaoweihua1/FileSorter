import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    async with async_playwright() as p:
        # 用Edge打开GitHub注册
        browser = await p.chromium.launch(
            headless=False,
            executable_path=edge_path,
            args=["--start-maximized"]
        )
        page = await browser.new_page()
        
        await page.goto("https://github.com/signup")
        await page.wait_for_timeout(3000)
        
        # 截图确认
        await page.screenshot(path=r"C:\Users\AWEI\Desktop\github_signup.png")
        print("✅ GitHub注册页面已打开，截图保存在桌面 github_signup.png")
        print("请查看截图，在浏览器中继续完成注册")
        
        # 等待用户完成注册
        input("按回车键关闭浏览器...")
        await browser.close()

asyncio.run(main())
