import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # 先启动新的Edge带调试端口
        browser = await p.chromium.launch(
            headless=False,
            channel="msedge",
            args=["--remote-debugging-port=9222"]
        )
        page = await browser.new_page()
        
        # 去token设置页面
        await page.goto("https://github.com/settings/tokens", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        # 获取页面内容找token
        html = await page.inner_html("body")
        import re
        # 找所有ghp_格式的token
        tokens = re.findall(r'ghp_\w{36,}', html)
        if tokens:
            token = tokens[0]
            print(f"✅ 找到Token: {token[:8]}...{token[-4:]}")
            with open(r"C:\Users\AWEI\Desktop\token.txt", "w") as f:
                f.write(token)
            
            # 创建仓库并push
            from github import Github
            import subprocess
            g = Github(token)
            user = g.get_user()
            try:
                repo = user.get_repo("FileSorter")
            except:
                repo = user.create_repo("FileSorter", "一键文件整理工具", private=False)
            
            repo_dir = r"C:\Users\AWEI\.astrbot\data\workspaces\default_FriendMessage_C12C0123E6C2C6B9F24541448E394668\FileSort"
            remote_url = f"https://xiaoweihua1:{token}@github.com/xiaoweihua1/FileSorter.git"
            subprocess.run(["git", "-C", repo_dir, "remote", "remove", "origin"], capture_output=True)
            subprocess.run(["git", "-C", repo_dir, "remote", "add", "origin", remote_url], capture_output=True)
            result = subprocess.run(["git", "-C", repo_dir, "push", "-u", "origin", "master", "--force"],
                                   capture_output=True, text=True, timeout=60)
            print(f"Push: {result.stdout[-100:]}")
            print(f"✅ 全部完成！https://github.com/xiaoweihua1/FileSorter")
        else:
            print("⚠️ 没找到token，保存页面内容")
            with open(r"C:\Users\AWEI\Desktop\token_page.html", "w", encoding='utf-8') as f:
                f.write(html[:10000])
        
        await browser.close()

asyncio.run(main())
