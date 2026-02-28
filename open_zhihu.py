from playwright.sync_api import sync_playwright
import time

print("正在启动浏览器...")

with sync_playwright() as p:
    # 启动 Edge 浏览器（非 headless 模式）
    browser = p.chromium.launch(
        channel="msedge",
        headless=False,
        args=["--start-maximized"]
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
    time.sleep(3)
    
    # 切换到密码登录
    print("尝试切换到密码登录...")
    try:
        # 查找密码登录选项
        password_tab = page.locator('text=密码登录').first
        if password_tab.is_visible():
            password_tab.click()
            print("已切换到密码登录")
            time.sleep(1)
        else:
            print("密码登录选项未找到，可能已在密码登录页面")
    except Exception as e:
        print(f"切换密码登录时出错：{e}")
    
    print("\n浏览器已打开知乎登录页面")
    print("请在浏览器中完成登录操作")
    print("按 Ctrl+C 退出脚本并关闭浏览器\n")
    
    # 保持浏览器打开，等待用户操作
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在关闭浏览器...")
        browser.close()
        print("浏览器已关闭")
