"""
浙江省电子税务局 - 完整登录测试（正确密码）
浏览器保持打开，不自动关闭
"""
from playwright.sync_api import sync_playwright
import time

# 浙江省电子税务局统一登录 URL
LOGIN_URL = "https://tpass.zhejiang.chinatax.gov.cn:8443/#/login?redirect_uri=https%3A%2F%2Fetax.zhejiang.chinatax.gov.cn%3A8443%2Fmhzx%2Fapi%2Fmh%2Ftpass%2Fcode&client_id=tct8zta97w6c46zdt9zc2648227df5z2&response_type=code&state=232c3847df0f4f36a00c1b5e55ca3fe9"

# 登录信息（从 Excel 读取）
SHEHUI_XINYONG = "913301040709922876"  # 纳税人识别号
PHONE_NUMBER = "15606523222"           # 手机号
PASSWORD = "Cgl@6066098"               # 个人用户密码

print("=" * 60)
print("浙江省电子税务局 - 完整登录测试")
print("=" * 60)
print(f"社会信用代码：{SHEHUI_XINYONG}")
print(f"手机号码：{PHONE_NUMBER}")
print(f"密码：{PASSWORD}")
print("=" * 60)

playwright = sync_playwright().start()
browser = playwright.chromium.launch(
    channel="msedge",
    headless=False,
    args=["--no-first-run", "--no-default-browser-check"]
)
context = browser.new_context(viewport={"width": 1280, "height": 720})
page = context.new_page()

# 步骤 1：访问登录页面
print("\n[步骤 1] 访问登录页面...")
page.goto(LOGIN_URL)
page.wait_for_load_state("networkidle")
time.sleep(2)
print("页面已加载")
page.screenshot(path="step1_login.png")

# 步骤 2：点击代理业务
print("\n[步骤 2] 点击 '代理业务'...")
page.locator('text=代理业务').first.click()
time.sleep(1)
print("已切换到代理业务")
page.screenshot(path="step2_daili.png")

# 步骤 3：填写社会信用代码
print(f"\n[步骤 3] 填写社会信用代码：{SHEHUI_XINYONG}")
page.locator('input[placeholder*="代理机构统一社会信用代码"]').first.fill(SHEHUI_XINYONG)
time.sleep(0.5)

# 步骤 4：填写手机号码
print(f"[步骤 4] 填写手机号码：{PHONE_NUMBER}")
page.locator('input[placeholder*="手机号码"]').first.fill(PHONE_NUMBER)
time.sleep(0.5)

# 步骤 5：填写密码
print(f"[步骤 5] 填写密码：{PASSWORD}")
page.locator('input[type="password"]').first.fill(PASSWORD)
time.sleep(0.5)
page.screenshot(path="step3_filled.png")

# 步骤 6：点击登录
print("\n[步骤 6] 点击 '登录' 按钮...")
page.locator('button:has-text("登录")').first.click()
time.sleep(5)
page.screenshot(path="step4_after_login.png")

# 显示当前状态
print(f"\n当前 URL: {page.url}")
print(f"页面标题：{page.title()}")

print("\n" + "=" * 60)
print("[OK] 登录流程完成，浏览器保持打开用于调试")
print("=" * 60)
print("\n按 Ctrl+C 关闭浏览器\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n关闭浏览器...")
    context.close()
    browser.close()
    playwright.stop()
