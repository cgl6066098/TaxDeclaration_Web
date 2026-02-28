"""
访问知乎并点击密码登录
"""
from playwright.sync_api import sync_playwright
import time
import os

USER_DATA_DIR = os.path.join(os.path.dirname(__file__), "browser_profile")
os.makedirs(USER_DATA_DIR, exist_ok=True)

print("正在启动浏览器...")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        channel="msedge",
        headless=False,
        viewport={"width": 1280, "height": 720},
        args=["--no-first-run", "--no-default-browser-check"],
    )
    
    page = context.pages[0] if context.pages else context.new_page()
    
    # 访问知乎
    print("正在访问知乎...")
    page.goto("https://www.zhihu.com/signin")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    
    # 截图 - 点击前
    page.screenshot(path=os.path.join(os.path.dirname(__file__), "before.png"))
    print("截图：before.png")
    
    # 检查当前状态
    yan_tab = page.locator('text=验证码登录').first
    pwd_tab = page.locator('text=密码登录').first
    
    print(f"验证码登录可见：{yan_tab.is_visible()}")
    print(f"密码登录可见：{pwd_tab.is_visible()}")
    
    # 点击密码登录
    print("正在点击 '密码登录'...")
    pwd_tab.click()
    time.sleep(3)
    
    # 截图 - 点击后
    page.screenshot(path=os.path.join(os.path.dirname(__file__), "after.png"))
    print("截图：after.png")
    
    # 验证
    password_input = page.locator('input[type="password"]')
    print(f"密码输入框可见：{password_input.count() > 0}")
    
    if password_input.count() > 0:
        print("[OK] 已成功切换到密码登录界面")
    
    print("\n[OK] 操作完成，3 秒后关闭浏览器...")
    time.sleep(3)
    context.close()
    print("浏览器已关闭")
