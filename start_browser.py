"""
启动浏览器并监听 CDP 端口，保持长连接
后续脚本可以通过 CDP 端口连接到这个浏览器
"""
from playwright.sync_api import sync_playwright
import time
import os

# 用户数据目录
USER_DATA_DIR = "C:\\Users\\15606\\miniconda3\\envs\\tax_python\\browser_profile"

# 创建用户数据目录
os.makedirs(USER_DATA_DIR, exist_ok=True)

print("正在启动浏览器（CDP 模式）...")
print(f"用户数据目录：{USER_DATA_DIR}")

with sync_playwright() as p:
    # 启动 Chromium 浏览器（使用 Edge 通道），开启 CDP 端口
    browser = p.chromium.launch(
        channel="msedge",
        headless=False,
        args=[
            f"--remote-debugging-port=9222",
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
    
    print("\n[OK] 浏览器已启动！")
    print("CDP 端口：9222")
    print("\n保持浏览器运行，按 Ctrl+C 关闭...")
    print("\n你可以运行 connect_browser.py 来连接这个浏览器并执行操作")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在关闭浏览器...")
        browser.close()
        print("浏览器已关闭")
