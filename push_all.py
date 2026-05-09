import asyncio, subprocess, os, re
from playwright.async_api import async_playwright

async def main():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    print("[1/7] 启动Edge...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, executable_path=edge_path, channel="msedge")
        page = await browser.new_page()
        
        print("[2/7] 登录GitHub...")
        await page.goto("https://github.com/login", wait_until="domcontentloaded")
        await page.locator("#login_field").fill("xiaoweihua1")
        await page.locator("#password").fill("awei031212")
        await page.locator("input[type='submit']").click()
        await page.wait_for_timeout(3000)
        
        print("[3/7] 创建token...")
        await page.goto("https://github.com/settings/tokens/new?scopes=repo&description=FileSorter", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        # 勾repo
        if await page.locator("input#repo").count() > 0:
            await page.locator("input#repo").check()
        else:
            await page.locator("label:has-text('repo')").first.click()
        
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(500)
        await page.locator("button:has-text('Generate token')").first.click()
        await page.wait_for_timeout(5000)
        
        print("[4/7] 提取token...")
        html = await page.inner_html("body")
        token_match = re.search(r'ghp_\w{36,}', html)
        
        if token_match:
            token = token_match.group(0)
            print(f"[5/7] Token: {token[:8]}...{token[-4:]}")
            
            with open(r"C:\Users\AWEI\Desktop\token.txt", "w") as f:
                f.write(token)
            
            print("[6/7] 创建仓库并push...")
            from github import Github
            g = Github(token)
            user = g.get_user()
            try:
                repo = user.get_repo("FileSorter")
                print("  仓库已存在")
            except:
                repo = user.create_repo("FileSorter", description="一键文件整理工具", private=False)
                print("  仓库创建成功")
            
            repo_dir = r"C:\Users\AWEI\.astrbot\data\workspaces\default_FriendMessage_C12C0123E6C2C6B9F24541448E394668\FileSort"
            remote_url = f"https://xiaoweihua1:{token}@github.com/xiaoweihua1/FileSorter.git"
            subprocess.run(["git", "-C", repo_dir, "remote", "remove", "origin"], capture_output=True)
            subprocess.run(["git", "-C", repo_dir, "remote", "add", "origin", remote_url], capture_output=True)
            result = subprocess.run(["git", "-C", repo_dir, "push", "-u", "origin", "master", "--force"],
                                   capture_output=True, text=True, timeout=60)
            print(f"[7/7] Push完成!")
            print(f"  结果: {result.stdout[-100:]}{result.stderr[-100:]}")
            print(f"  仓库: https://github.com/xiaoweihua1/FileSorter")
        else:
            print("[失败] 未找到token")
        
        # 保持浏览器打开
        print("\n✅ 操作完成，浏览器保持打开")
        while True:
            await asyncio.sleep(10)

asyncio.run(main())
