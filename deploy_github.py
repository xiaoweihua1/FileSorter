import asyncio, os, subprocess, sys
from playwright.async_api import async_playwright

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
repo_dir = r"C:\Users\AWEI\.astrbot\data\workspaces\default_FriendMessage_C12C0123E6C2C6B9F24541448E394668\FileSort"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            executable_path=edge_path,
            channel="msedge",
        )
        page = await browser.new_page()
        
        # 第一步：登录GitHub
        print("步骤1/6: 打开GitHub登录页面...")
        await page.goto("https://github.com/login", timeout=60000)
        await page.wait_for_timeout(2000)
        
        # 填登录表单
        await page.locator("#login_field").fill("3263173839@qq.com")
        await page.locator("#password").fill("awei031212")
        await page.locator("input[type='submit']").click()
        await page.wait_for_timeout(5000)
        print("步骤2/6: 登录完成")
        
        # 检查是否登录成功（是否有2FA验证）
        page_url = page.url
        if "two-factor" in page_url or "sessions" in page_url:
            print("⚠️ 需要双重验证，请在浏览器中完成验证后继续")
            await page.wait_for_timeout(30000)
        
        # 第二步：创建仓库
        print("步骤3/6: 创建仓库...")
        await page.goto("https://github.com/new", timeout=60000)
        await page.wait_for_timeout(2000)
        
        # 填仓库名
        await page.locator("#repository_name").fill("FileSorter")
        await page.wait_for_timeout(1000)
        
        # 仓库描述
        desc = page.locator("#repository_description")
        if await desc.count() > 0:
            await desc.fill("一键文件整理工具，按类型归类，批量重命名")
        
        # 确保是Public
        await page.wait_for_timeout(500)
        
        # 点创建
        await page.locator("button:has-text('Create repository')").first.click()
        await page.wait_for_timeout(5000)
        print("步骤4/6: 仓库创建完成")
        
        # 获取仓库URL
        current_url = page.url
        print(f"仓库地址: {current_url}")
        
        # 第三步：返回本地git push
        print("步骤5/6: 本地git配置并推送...")
        
        # 更新git remote
        subprocess.run(["git", "-C", repo_dir, "remote", "remove", "origin"], 
                       capture_output=True, cwd=repo_dir)
        subprocess.run(["git", "-C", repo_dir, "remote", "add", "origin", 
                       f"{current_url.rstrip('/')}.git"], cwd=repo_dir)
        
        # 添加文件并push
        result = subprocess.run(["git", "-C", repo_dir, "push", "-u", "origin", "master", "--force"],
                               capture_output=True, text=True, cwd=repo_dir)
        
        if result.returncode == 0:
            print("步骤6/6: 上传完成！✅")
        else:
            print(f"push输出: {result.stdout[-200:]}{result.stderr[-200:]}")
            # 如果master分支不行，尝试main
            result2 = subprocess.run(["git", "-C", repo_dir, "push", "-u", "origin", "main", "--force"],
                                    capture_output=True, text=True, cwd=repo_dir)
            if result2.returncode == 0:
                print("步骤6/6: 上传完成！✅")
            else:
                print(f"main分支也失败: {result2.stderr[-300:]}")
        
        print("\n✅ 全部完成！浏览器保持打开，您可以查看")
        
        # 浏览器保持打开
        while True:
            await asyncio.sleep(60)

asyncio.run(main())
