"""
连接到已运行的 Edge 浏览器并执行操作
前提：先运行 run_edge.py 或 启动浏览器.bat 打开浏览器
"""
from playwright.sync_api import sync_playwright
import time
import os

USER_DATA_DIR = "C:\\Users\\15606\\miniconda3\\envs\\tax_python\\browser_profile"

print("=" * 50)
print("连接已运行的浏览器")
print("=" * 50)

with sync_playwright() as p:
    # 连接到已运行的浏览器实例
    # 使用 persistent_context 复用用户数据目录
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        channel="msedge",
        headless=False,
        viewport={"width": 1280, "height": 720},
        args=[
            "--no-first-run",
            "--no-default-browser-check",
        ]
    )
    
    print("[OK] 已连接到浏览器")
    
    # 获取当前页面
    page = context.pages[0] if context.pages else context.new_page()
    
    print(f"\n当前页面 URL: {page.url}")
    print(f"页面标题：{page.title()}")
    
    # 截图
    screenshot_path = os.path.join(os.path.dirname(__file__), f"snapshot_{int(time.time())}.png")
    page.screenshot(path=screenshot_path)
    print(f"\n截图已保存：{screenshot_path}")
    
    # 如果当前在知乎，执行一些操作
    if "zhihu.com" in page.url:
        print("\n检测到知乎页面，可以执行操作...")
        
        # 检查登录状态
        if "signin" in page.url.lower():
            print("当前在登录页面")
            
            # 检查登录方式
            yan_tab = page.locator('text=验证码登录').first
            pwd_tab = page.locator('text=密码登录').first
            
            print(f"  '验证码登录' 可见：{yan_tab.is_visible()}")
            print(f"  '密码登录' 可见：{pwd_tab.is_visible()}")
            
            # 如果需要，切换到密码登录
            if yan_tab.is_visible():
                print("\n点击切换到密码登录...")
                pwd_tab.click()
                time.sleep(1)
                print("[OK] 已切换")
                
                # 截图
                time.sleep(1)
                screenshot2 = os.path.join(os.path.dirname(__file__), f"after_{int(time.time())}.png")
                page.screenshot(path=screenshot2)
                print(f"切换后截图：{screenshot2}")
        else:
            print("当前已登录或不在登录页面")
    
    print("\n[OK] 操作完成")
    print("\n按 Ctrl+C 关闭浏览器")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在关闭浏览器...")
        context.close()
        print("浏览器已关闭")
