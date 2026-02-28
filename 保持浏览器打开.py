"""
保持浏览器打开状态 - 用于调试
不关闭浏览器，方便手动操作和调试
"""
from playwright.sync_api import sync_playwright
import time
import os

# 浙江省电子税务局统一登录 URL
LOGIN_URL = "https://tpass.zhejiang.chinatax.gov.cn:8443/#/login?redirect_uri=https%3A%2F%2Fetax.zhejiang.chinatax.gov.cn%3A8443%2Fmhzx%2Fapi%2Fmh%2Ftpass%2Fcode&client_id=tct8zta97w6c46zdt9zc2648227df5z2&response_type=code&state=232c3847df0f4f36a00c1b5e55ca3fe9"

# 登录信息（从 Excel 读取）
SHEHUI_XINYONG = "913301040709922876"  # 社会信用代码
PHONE_NUMBER = "15606523222"           # 手机号
PASSWORD = "Cgl@6066098"               # 个人用户密码

print("=" * 70)
print("浙江省电子税务局 - 调试模式")
print("=" * 70)
print("\n此脚本用于保持浏览器打开状态，方便调试")
print("浏览器不会自动关闭，按 Ctrl+C 手动关闭")
print("=" * 70)

playwright = sync_playwright().start()
browser = playwright.chromium.launch(
    channel="msedge",
    headless=False,
    args=["--no-first-run", "--no-default-browser-check"]
)
context = browser.new_context(viewport={"width": 1280, "height": 720})
page = context.new_page()

# 访问登录页面
print("\n[1/6] 访问登录页面...")
page.goto(LOGIN_URL)
page.wait_for_load_state("networkidle")
time.sleep(2)
print("      完成")

# 点击代理业务
print("[2/6] 点击 '代理业务'...")
page.locator('text=代理业务').first.click()
time.sleep(1)
print("      完成")

# 填写社会信用代码
print(f"[3/6] 填写社会信用代码：{SHEHUI_XINYONG}")
page.locator('input[placeholder*="代理机构统一社会信用代码"]').first.fill(SHEHUI_XINYONG)
time.sleep(0.5)
print("      完成")

# 填写手机号码
print(f"[4/6] 填写手机号码：{PHONE_NUMBER}")
page.locator('input[placeholder*="手机号码"]').first.fill(PHONE_NUMBER)
time.sleep(0.5)
print("      完成")

# 填写密码
print(f"[5/6] 填写密码：{PASSWORD}")
page.locator('input[type="password"]').first.fill(PASSWORD)
time.sleep(0.5)
print("      完成")

# 点击登录
print("[6/6] 点击 '登录' 按钮...")
page.locator('button:has-text("登录")').first.click()
time.sleep(3)
print("      完成")

# 保存当前状态截图
screenshot_dir = os.path.join(os.path.dirname(__file__), "纳税申报模块", "screenshots")
os.makedirs(screenshot_dir, exist_ok=True)
timestamp = time.strftime("%Y%m%d_%H%M%S")
screenshot_path = os.path.join(screenshot_dir, f"{timestamp}_debug_state.png")
page.screenshot(path=screenshot_path)
print(f"\n[OK] 当前状态已截图：{screenshot_path}")

# 显示当前状态
print(f"\n当前 URL: {page.url}")
print(f"页面标题：{page.title()}")

print("\n" + "=" * 70)
print("浏览器保持打开状态 - 可进行调试")
print("=" * 70)
print("\n提示:")
print("  - 可以在浏览器中手动操作")
print("  - 按 Ctrl+C 关闭浏览器")
print("  - 浏览器进程将保持运行")
print("=" * 70)
print("\n等待中...\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n关闭浏览器...")
    context.close()
    browser.close()
    playwright.stop()
    print("浏览器已关闭")
