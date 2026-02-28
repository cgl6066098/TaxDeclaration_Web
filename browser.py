"""
知乎自动化 - 持久化浏览器
每次运行都会复用同一个浏览器配置文件，保持登录状态

使用方法：
    C:\Users\15606\miniconda3\envs\tax_python\python.exe browser.py
"""
from playwright.sync_api import sync_playwright
import time
import os

# 用户数据目录 - 浏览器状态会保存到这里
USER_DATA_DIR = os.path.join(os.path.dirname(__file__), "browser_profile")
os.makedirs(USER_DATA_DIR, exist_ok=True)

print("=" * 60)
print("知乎自动化 - 持久化浏览器")
print("=" * 60)
print(f"用户数据目录：{USER_DATA_DIR}")
print()

with sync_playwright() as p:
    # 启动浏览器，使用持久化用户数据
    browser = p.chromium.launch(
        channel="msedge",
        headless=False,
        args=[
            f"--user-data-dir={USER_DATA_DIR}",
            "--no-first-run",
            "--no-default-browser-check",
        ]
    )
    
    context = browser.new_context(
        viewport={"width": 1280, "height": 720}
    )
    
    page = context.new_page()
    
    # 打开知乎
    print("正在打开知乎...")
    page.goto("https://www.zhihu.com/signin")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    
    print("[OK] 页面已打开")
    print(f"当前 URL: {page.url}")
    print(f"页面标题：{page.title()}")
    
    # 截图
    screenshot_path = os.path.join(os.path.dirname(__file__), "current_page.png")
    page.screenshot(path=screenshot_path)
    print(f"截图：{screenshot_path}")
    
    print("\n浏览器保持打开，按 Ctrl+C 关闭...")
    print("提示：登录状态会保存，下次运行自动保持登录")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在关闭浏览器...")
        browser.close()
        print("浏览器已关闭")
        print(f"\n提示：浏览器数据保存在：{USER_DATA_DIR}")
