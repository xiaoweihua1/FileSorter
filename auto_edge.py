import subprocess, time, re as re_m
from pywinauto import Application, keyboard
import pywinauto

# 先关掉所有Edge
subprocess.run("taskkill /F /IM msedge.exe 2>nul", shell=True, capture_output=True)
time.sleep(1)

# 打开Edge到GitHub登录
subprocess.Popen(r'start msedge https://github.com/login', shell=True)
time.sleep(5)

# 连接到Edge窗口
try:
    app = Application(backend="uia").connect(title_re=".*GitHub.*", timeout=10)
    dlg = app.top_window()
    dlg.set_focus()
    time.sleep(1)
    
    # 发送Tab键导航到输入框
    keyboard.send_keys("{TAB 5}")  # 跳到第一个输入框
    time.sleep(0.5)
    keyboard.send_keys("xiaoweihua1")  # 输入用户名
    time.sleep(0.3)
    keyboard.send_keys("{TAB}")  # 跳到密码框
    time.sleep(0.3)
    keyboard.send_keys("awei031212")  # 输入密码
    time.sleep(0.3)
    keyboard.send_keys("{ENTER}")  # 提交
    time.sleep(5)
    
    # 打开token创建页面
    keyboard.send_keys("^l")  # Ctrl+L 选中地址栏
    time.sleep(0.5)
    keyboard.send_keys("https://github.com/settings/tokens/new{ENTER}")
    time.sleep(5)
    
    # 填写token名称
    keyboard.send_keys("{TAB 3}")  # 跳到Note输入框
    time.sleep(0.3)
    keyboard.send_keys("FileSorter_pyauto")
    time.sleep(0.3)
    
    # Tab到repo复选框
    keyboard.send_keys("{TAB 8}")
    time.sleep(0.3)
    keyboard.send_keys(" ")  # 空格勾选
    time.sleep(0.3)
    
    # 滚动到底部
    keyboard.send_keys("{PAGEDOWN 3}")
    time.sleep(0.5)
    
    # Tab到Generate按钮
    keyboard.send_keys("{TAB 15}")
    time.sleep(0.3)
    keyboard.send_keys("{ENTER}")  # 点击Generate
    time.sleep(5)
    
    # 全选复制token
    keyboard.send_keys("^a")  # 全选
    time.sleep(0.3)
    keyboard.send_keys("^c")  # 复制
    time.sleep(1)
    
    print("操作完成，token已复制到剪贴板")
    
except Exception as e:
    print(f"自动化出错: {e}")
    print("请手动操作：")
    print("1. 在打开的浏览器中登录GitHub")
    print("2. 打开 https://github.com/settings/tokens/new")
    print("3. 创建token并复制给我")
