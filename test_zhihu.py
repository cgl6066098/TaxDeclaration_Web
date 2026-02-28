from playwright.sync_api import sync_playwright
import time
import os

print("正在启动浏览器...")

with sync_playwright() as p:
    # 启动 Edge 浏览器（非 headless 模式）
    browser = p.chromium.launch(
        channel="msedge",
        headless=False
    )
    
    context = browser.new_context(
        viewport={"width": 1280, "height": 720}
    )
    
    page = context.new_page()
    
    # 打开知乎登录页面
    print("正在打开知乎登录页面...")
    page.goto("https://www.zhihu.com/signin")
    
    # 等待页面加载
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    
    # 截图 - 登录前
    screenshot_path = os.path.join(os.path.dirname(__file__), "before_click.png")
    page.screenshot(path=screenshot_path)
    print(f"截图已保存：{screenshot_path}")
    
    # 分析页面元素
    print("\n=== 页面分析 ===")
    
    # 检查当前登录方式
    print("1. 检查当前登录标签...")
    yan_tab = page.locator('text=验证码登录').first
    pwd_tab = page.locator('text=密码登录').first
    
    print(f"   '验证码登录' 可见：{yan_tab.is_visible()}")
    print(f"   '密码登录' 可见：{pwd_tab.is_visible()}")
    
    # 获取所有 tab 元素
    print("\n2. 查找所有登录方式标签...")
    tabs = page.locator('[role="tab"], .SignFlow-tab, a[href*="signin"]')
    count = tabs.count()
    print(f"   找到 {count} 个标签")
    
    for i in range(count):
        try:
            tab = tabs.nth(i)
            text = tab.inner_text().strip()
            visible = tab.is_visible()
            print(f"   [{i}] '{text}' (可见：{visible})")
        except Exception as e:
            print(f"   [{i}] 读取失败：{e}")
    
    # 执行点击 - 密码登录
    print("\n=== 执行点击 ===")
    print("点击 '密码登录' 标签...")
    
    try:
        # 直接点击文本
        password_tab = page.locator('text=密码登录').first
        if password_tab.is_visible():
            password_tab.click()
            print("[OK] 点击成功!")
            time.sleep(2)
            
            # 验证切换
            print("\n验证是否切换到密码登录...")
            password_input = page.locator('input[type="password"]')
            phone_input = page.locator('input[type="tel"], input[placeholder*="手机"]')
            
            print(f"   密码输入框可见：{password_input.count() > 0}")
            print(f"   手机号输入框可见：{phone_input.count() > 0}")
            
            if password_input.count() > 0:
                print("[OK] 已切换到密码登录界面!")
        else:
            print("[ERROR] '密码登录' 不可见")
            
    except Exception as e:
        print(f"[ERROR] 点击失败：{e}")
    
    # 截图 - 点击后
    time.sleep(1)
    screenshot_path2 = os.path.join(os.path.dirname(__file__), "after_click.png")
    page.screenshot(path=screenshot_path2)
    print(f"\n操作后截图：{screenshot_path2}")
    
    print("\n浏览器保持打开，按 Ctrl+C 退出...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        browser.close()
