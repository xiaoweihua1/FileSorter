
import asyncio, subprocess, os, re, ssl, json, urllib.request
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="msedge")
        page = await browser.new_page()
        
        # 登录
        await page.goto("https://github.com/login")
        await page.locator("#login_field").fill("xiaoweihua1")
        await page.locator("#password").fill("awei031212")
        await page.locator("input[type='submit']").click()
        await page.wait_for_timeout(3000)
        
        # 创建token - 注意这里一定要用新名字
        await page.goto("https://github.com/settings/tokens/new")
        await page.wait_for_timeout(2000)
        
        note_input = page.locator("#token_name")
        await note_input.fill("FileSorter_new_token")
        
        # 勾repo
        await page.locator("label:has-text('repo')").first.click()
        await page.wait_for_timeout(300)
        
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(800)
        
        await page.locator("button:has-text('Generate token')").first.click()
        await page.wait_for_timeout(5000)
        
        # 用多种方式提取token
        html = await page.content()
        token = None
        
        # 方式1: 正则
        m = re.search(r'ghp_\w{36,}', html)
        if m: token = m.group(0)
        
        # 方式2: 查找input框
        if not token:
            inp = page.locator("input[readonly]")
            if await inp.count() > 0:
                v = await inp.get_attribute("value")
                if v: token = v
        
        if token:
            print(f"OK:{token}")
            with open(r"C:\Users\AWEI\Desktop\_token.txt","w") as f:
                f.write(token)
        else:
            print("NOTOK")
            await page.screenshot(path=r"C:\Users\AWEI\Desktop\_fail.png")
        
        await browser.close()

asyncio.run(main())
