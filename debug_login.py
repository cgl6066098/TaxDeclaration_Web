"""
调试登录脚本
"""
from playwright.sync_api import sync_playwright
import time

USER_DATA_DIR = "C:\\Users\\15606\\miniconda3\\envs\\tax_python\\browser_profile"

print("启动 Playwright...")
p = sync_playwright().start()

print("启动浏览器...")
browser = p.chromium.launch(
    channel="msedge",
    headless=False,
    args=["--no-first-run", "--no-default-browser-check"]
)

print("创建上下文...")
context = browser.new_context(viewport={"width": 1280, "height": 720})

print("创建页面...")
page = context.new_page()

print("访问知乎...")
page.goto("https://www.zhihu.com/signin")
page.wait_for_load_state("networkidle")
time.sleep(2)

print(f"页面标题：{page.title()}")

# 查找密码登录
pwd_tab = page.locator('text=密码登录').first
yan_tab = page.locator('text=验证码登录').first

print(f"验证码登录可见：{yan_tab.is_visible()}")
print(f"密码登录可见：{pwd_tab.is_visible()}")

# 点击密码登录
print("\n点击密码登录...")
pwd_tab.click()
time.sleep(2)

# 截图
page.screenshot(path="test_login_result.png")
print("截图已保存：test_login_result.png")

print("\n浏览器保持打开，按 Ctrl+C 关闭...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n关闭浏览器...")
    context.close()
    browser.close()
    p.stop()
