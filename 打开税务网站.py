"""
打开浙江省电子税务局 - 永久保持浏览器打开
不关闭浏览器，用于调试和生产环境
"""
from playwright.sync_api import sync_playwright
import time

LOGIN_URL = "https://tpass.zhejiang.chinatax.gov.cn:8443/#/login?redirect_uri=https%3A%2F%2Fetax.zhejiang.chinatax.gov.cn%3A8443%2Fmhzx%2Fapi%2Fmh%2Ftpass%2Fcode&client_id=tct8zta97w6c46zdt9zc2648227df5z2&response_type=code&state=232c3847df0f4f36a00c1b5e55ca3fe9"

print("=" * 70)
print("浙江省电子税务局 - 永久保持浏览器打开")
print("=" * 70)
print("\n浏览器窗口将保持可见，不会关闭")
print("=" * 70)

playwright = sync_playwright().start()
browser = playwright.chromium.launch(
    channel="msedge",
    headless=False,
    args=["--no-first-run", "--no-default-browser-check"]
)
context = browser.new_context(viewport={"width": 1280, "height": 720})
page = context.new_page()

print("\n访问登录页面...")
page.goto(LOGIN_URL)
page.wait_for_load_state("networkidle")
time.sleep(2)
print("完成")

print("\n" + "=" * 70)
print("浏览器已打开，可以手动操作")
print("=" * 70)
print("\n按 Ctrl+C 退出脚本（浏览器保持打开）")
print("=" * 70)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n退出脚本")
    print("浏览器保持打开状态")
