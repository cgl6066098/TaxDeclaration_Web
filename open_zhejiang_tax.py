"""
访问浙江省电子税务局统一登录页面并点击"代理业务"
"""
from playwright.sync_api import sync_playwright
import time

# 浙江省电子税务局统一登录 URL
LOGIN_URL = "https://tpass.zhejiang.chinatax.gov.cn:8443/#/login?redirect_uri=https%3A%2F%2Fetax.zhejiang.chinatax.gov.cn%3A8443%2Fmhzx%2Fapi%2Fmh%2Ftpass%2Fcode&client_id=tct8zta97w6c46zdt9zc2648227df5z2&response_type=code&state=232c3847df0f4f36a00c1b5e55ca3fe9"

print("=" * 60)
print("浙江省电子税务局 - 点击代理业务")
print("=" * 60)

playwright = sync_playwright().start()

# 启动 Edge 浏览器
browser = playwright.chromium.launch(
    channel="msedge",
    headless=False,
    args=["--no-first-run", "--no-default-browser-check"]
)

context = browser.new_context(
    viewport={"width": 1280, "height": 720}
)

page = context.new_page()

# 访问登录页面
print(f"\n访问：{LOGIN_URL}")
page.goto(LOGIN_URL)
page.wait_for_load_state("networkidle")
time.sleep(2)

# 截图 - 点击前
page.screenshot(path="before_click_daili.png")
print("\n[截图 1] 点击前：before_click_daili.png")

# 分析当前状态
print("\n=== 当前登录方式 ===")
qiye_tab = page.locator('text=企业业务').first
ziran_tab = page.locator('text=自然人业务').first
daili_tab = page.locator('text=代理业务').first

print(f"企业业务可见：{qiye_tab.is_visible()}")
print(f"自然人业务可见：{ziran_tab.is_visible()}")
print(f"代理业务可见：{daili_tab.is_visible()}")

# 点击代理业务
print("\n=== 执行点击 ===")
print("点击：代理业务")
daili_tab.click()
time.sleep(2)

# 截图 - 点击后
page.screenshot(path="after_click_daili.png")
print("\n[截图 2] 点击后：after_click_daili.png")

# 分析点击后的变化
print("\n=== 点击后的表单 ===")
inputs = page.locator("input[type=text], input[type=password], input[name]")
input_count = inputs.count()

print(f"输入框数量：{input_count}")

for i in range(min(input_count, 10)):
    try:
        inp = inputs.nth(i)
        if inp.is_visible():
            placeholder = inp.get_attribute("placeholder") or ""
            name = inp.get_attribute("name") or ""
            print(f"  [{i}] name={name}, placeholder={placeholder}")
    except:
        pass

# 检查是否有变化
print("\n[OK] 已完成点击代理业务")

print("\n" + "=" * 60)
print("浏览器保持打开，按 Ctrl+C 关闭...")
print("=" * 60)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n关闭浏览器...")
    context.close()
    browser.close()
    playwright.stop()
