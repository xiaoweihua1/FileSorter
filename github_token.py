import asyncio, time, json
from playwright.async_api import async_playwright

async def main():
    # 连接到已经在运行的Edge
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        
        # 获取所有页面
        pages = browser.contexts[0].pages if browser.contexts else []
        
        if not pages:
            # 如果没有页面，新开一个
            page = await browser.new_page()
        else:
            page = pages[0]
        
        # 看看当前在哪个页面
        current_url = page.url
        print(f"当前页面: {current_url}")
        
        # 截图
        await page.screenshot(path=r"C:\Users\AWEI\Desktop\edge_status.png")
        
        # 尝试打开token页面
        await page.goto("https://github.com/settings/tokens/new", timeout=30000)
        await page.wait_for_timeout(3000)
        
        current_url2 = page.url
        print(f"跳转后: {current_url2}")
        
        await page.screenshot(path=r"C:\Users\AWEI\Desktop\github_token.png")
        
        # 看看有没有登录
        page_text = await page.inner_text("body")
        if "Sign in" in page_text and "Password" in page_text:
            print("❌ 未登录，需要先登录")
            # 填登录
            login = page.locator("#login_field")
            if await login.count() > 0:
                await login.fill("xiaoweihua1")
                await page.locator("#password").fill("awei031212")
                await page.locator("input[type='submit']").click()
                await page.wait_for_timeout(5000)
                print("已提交登录")
        elif "token" in page_text.lower() or "New personal access token" in page_text:
            print("✅ 已登录！在token页面")
            # 填token名称
            note = page.locator("input[id='token_name']")
            if await note.count() > 0:
                await note.fill("FileSorter")
                # 勾选repo
                repo_check = page.locator("input[value='repo']")
                if await repo_check.count() > 0:
                    await repo_check.click()
                    print("✅ 已勾选repo权限")
                # 生成token
                gen_btn = page.locator("button:has-text('Generate token')")
                if await gen_btn.count() > 0:
                    await gen_btn.click()
                    await page.wait_for_timeout(3000)
                    # 获取token
                    token_input = page.locator("input[class*='form-control']")
                    print("token页面已提交")
        
        await page.screenshot(path=r"C:\Users\AWEI\Desktop\github_result.png")
        print("截图已保存")
        
        # 保持打开
        while True:
            await asyncio.sleep(60)

asyncio.run(main())
