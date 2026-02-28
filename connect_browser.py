"""
连接到已运行的浏览器（通过 CDP 端口）
执行操作前请确保 start_browser.py 已经启动
"""
from playwright.sync_api import sync_playwright
import time
import os

print("正在连接到已运行的浏览器...")

with sync_playwright() as p:
    # 通过 CDP 端口连接到已运行的浏览器
    browser = p.chromium.connect_over_cdp(
        "http://localhost:9222",
        timeout=10000
    )
    
    print("[OK] 连接成功!")
    
    # 获取第一个上下文和页面
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    
    # 如果有现成的页面就用，否则创建新页面
    if context.pages:
        page = context.pages[0]
    else:
        page = context.new_page()
    
    # 执行操作
    print("\n执行操作...")
    
    # 检查当前页面 URL
    current_url = page.url
    print(f"当前页面：{current_url}")
    
    # 如果当前不是知乎，打开知乎
    if "zhihu.com" not in current_url:
        print("正在打开知乎...")
        page.goto("https://www.zhihu.com/signin")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
    
    # 截图
    screenshot_path = os.path.join(os.path.dirname(__file__), f"snapshot_{int(time.time())}.png")
    page.screenshot(path=screenshot_path)
    print(f"截图已保存：{screenshot_path}")
    
    # 获取页面标题
    title = page.title()
    print(f"页面标题：{title}")
    
    # 示例：检查是否在登录页面
    if "sign" in current_url.lower() or "login" in current_url.lower():
        print("\n检测到登录页面，可以执行登录操作...")
        
        # 检查登录方式
        yan_tab = page.locator('text=验证码登录').first
        pwd_tab = page.locator('text=密码登录').first
        
        print(f"  '验证码登录' 可见：{yan_tab.is_visible()}")
        print(f"  '密码登录' 可见：{pwd_tab.is_visible()}")
        
        # 如果需要切换到密码登录
        if yan_tab.is_visible() and pwd_tab.is_visible():
            print("\n点击切换到密码登录...")
            pwd_tab.click()
            time.sleep(1)
            print("[OK] 已切换到密码登录")
            
            # 再次截图
            time.sleep(1)
            screenshot_path2 = os.path.join(os.path.dirname(__file__), f"after_switch_{int(time.time())}.png")
            page.screenshot(path=screenshot_path2)
            print(f"切换后截图：{screenshot_path2}")
    
    print("\n[OK] 操作完成，浏览器保持打开状态")
    
    # 不关闭浏览器，只断开连接
    browser.close()
