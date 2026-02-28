"""
简单登录脚本 - 知乎
"""
from playwright.sync_api import sync_playwright
import time

USER_DATA_DIR = "C:\\Users\\15606\\miniconda3\\envs\\tax_python\\browser_profile"

print("启动浏览器...")

p = sync_playwright().start()

context = p.chromium.launch_persistent_context(
    user_data_dir=USER_DATA_DIR,
    channel="msedge",
    headless=False,
    viewport={"width": 1280, "height": 720},
    args=["--no-first-run", "--no-default-browser-check"],
)

page = context.pages[0] if context.pages else context.new_page()

print("访问知乎...")
page.goto("https://www.zhihu.com/signin")
page.wait_for_load_state("networkidle")
time.sleep(2)

# 分析页面
print(f"\n页面标题：{page.title()}")

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
page.screenshot("test_login_result.png")
print("截图已保存：test_login_result.png")

print("\n浏览器保持打开，按 Ctrl+C 关闭...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n关闭浏览器...")
    context.close()
    p.stop()
