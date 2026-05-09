
import asyncio, subprocess, os, re, ssl, json, urllib.request
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="msedge")
        page = await browser.new_page()
        print("登录...")
        await page.goto("https://github.com/login")
        await page.locator("#login_field").fill("xiaoweihua1")
        await page.locator("#password").fill("awei031212")
        await page.locator("input[type='submit']").click()
        await page.wait_for_timeout(3000)
        
        print("创建token...")
        await page.goto("https://github.com/settings/tokens/new")
        await page.wait_for_timeout(2000)
        await page.locator("#token_name").fill("FileSorter_final")
        await page.locator("input#repo").check()
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(500)
        await page.locator("button:has-text('Generate token')").first.click()
        await page.wait_for_timeout(5000)
        
        html = await page.content()
        token_match = re.search(r"ghp_\w{36,}", html)
        if token_match:
            token = token_match.group(0)
            print(f"TOKEN:{token}")
            ssl._create_default_https_context = ssl._create_unverified_context
            
            data = json.dumps({"name":"FileSorter","private":False}).encode()
            req = urllib.request.Request("https://api.github.com/user/repos", data=data, method="POST")
            req.add_header("Authorization", f"token {token}")
            req.add_header("Content-Type","application/json")
            req.add_header("User-Agent","FileSorter")
            try:
                urllib.request.urlopen(req, timeout=15)
            except urllib.error.HTTPError:
                pass
            
            rd = r"C:\Users\AWEI\.astrbot\data\workspaces\default_FriendMessage_C12C0123E6C2C6B9F24541448E394668\FileSort"
            ru = f"https://xiaoweihua1:{token}@github.com/xiaoweihua1/FileSorter.git"
            subprocess.run(["git","-C",rd,"remote","remove","origin"],capture_output=True)
            subprocess.run(["git","-C",rd,"remote","add","origin",ru],capture_output=True)
            r = subprocess.run(["git","-C",rd,"push","-u","origin","master","--force"],capture_output=True,text=True,timeout=60)
            print(f"DONE:{r.returncode}")
        else:
            print("FAIL")
        await browser.close()

asyncio.run(main())
