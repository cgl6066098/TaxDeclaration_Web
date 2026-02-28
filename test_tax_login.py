"""
浙江省电子税务局 - 登录测试
- 自动检测现有浏览器
- 如果浏览器已打开则连接
- 检查是否在税务局页面，不在则打开新标签
- 永久保持浏览器打开
"""
from 纳税申报模块.browser import get_page, get_page_by_url, screenshot, wait, list_pages
import time

# 登录信息
SHEHUI_XINYONG = "913301040709922876"
PHONE_NUMBER = "15606523222"
PASSWORD = "Cgl@6066098"

# 登录 URL
LOGIN_URL = "https://tpass.zhejiang.chinatax.gov.cn:8443/#/login?redirect_uri=https%3A%2F%2Fetax.zhejiang.chinatax.gov.cn%3A8443%2Fmhzx%2Fapi%2Fmh%2Ftpass%2Fcode&client_id=tct8zta97w6c46zdt9zc2648227df5z2&response_type=code&state=232c3847df0f4f36a00c1b5e55ca3fe9"

print("=" * 70)
print("浙江省电子税务局 - 登录测试")
print("=" * 70)
print(f"社会信用代码：{SHEHUI_XINYONG}")
print(f"手机号码：{PHONE_NUMBER}")
print(f"密码：{'*' * len(PASSWORD)}")
print("=" * 70)

# 获取浏览器（自动检测现有浏览器并连接）
print("\n[浏览器] 获取浏览器...")
page = get_page()

# 检查当前页面
print(f"\n当前 URL: {page.url}")
print(f"当前标题：{page.title()}")

# 检查是否在税务局页面
if "zhejiang.chinatax.gov.cn" not in page.url:
    print("\n[提示] 当前不在税务局页面，打开新标签...")
    page = get_page_by_url("zhejiang.chinatax.gov.cn")

# 显示所有页面
print(f"\n当前所有页面：{list_pages()}")

# 访问登录页面
print("\n[步骤 1] 访问登录页面...")
page.goto(LOGIN_URL)
page.wait_for_load_state("networkidle")
time.sleep(2)
screenshot("01_login_page")
print("        完成")

# 点击代理业务
print("\n[步骤 2] 点击 '代理业务'...")
page.locator('text=代理业务').first.click()
time.sleep(1)
screenshot("02_daili")
print("        完成")

# 填写登录信息
print(f"\n[步骤 3] 填写社会信用代码：{SHEHUI_XINYONG}")
page.locator('input[placeholder*="代理机构统一社会信用代码"]').first.fill(SHEHUI_XINYONG)
time.sleep(0.5)
print("        完成")

print(f"[步骤 4] 填写手机号码：{PHONE_NUMBER}")
page.locator('input[placeholder*="手机号码"]').first.fill(PHONE_NUMBER)
time.sleep(0.5)
print("        完成")

print(f"[步骤 5] 填写密码：{'*' * len(PASSWORD)}")
page.locator('input[type="password"]').first.fill(PASSWORD)
time.sleep(0.5)
screenshot("03_filled")
print("        完成")

# 点击登录
print(f"\n[步骤 6] 点击 '登录' 按钮...")
page.locator('button:has-text("登录")').first.click()
time.sleep(3)
screenshot("04_after_login")
print("        完成")

# 显示当前状态
print(f"\n当前 URL: {page.url}")
print(f"页面标题：{page.title()}")

print("\n" + "=" * 70)
print("验证码已显示，请手动完成")
print("=" * 70)
print("\n完成后按回车键继续...")
input("\n按回车键继续...")

# 截图
screenshot("05_verified")
print("\n[OK] 验证码已完成")

# 等待页面加载
time.sleep(3)
screenshot("06_dashboard")

# 显示当前状态
print(f"\n当前 URL: {page.url}")
print(f"页面标题：{page.title()}")

# 列出所有页面
print(f"\n所有页面：{list_pages()}")

# 查找页面上的元素
print("\n查找页面上的菜单项...")
elements = page.locator("a, button, div[role='menuitem'], div[role='button'], span, label")
count = elements.count()

print(f"\n找到 {count} 个元素")
print("\n前 50 个元素:")

found_items = []
for i in range(min(count, 50)):
    try:
        elem = elements.nth(i)
        if elem.is_visible():
            text = elem.inner_text().strip()
            if text and len(text) < 50:
                highlight = ""
                for kw in ["财务", "账务", "中心", "会计", "税务", "申报", "我的", "首页"]:
                    if kw in text:
                        highlight = " <--"
                        found_items.append((i, text))
                        break
                print(f"  [{i:2d}] {text}{highlight}")
    except:
        pass

print(f"\n找到 {len(found_items)} 个相关元素")

print("\n" + "=" * 70)
print("浏览器保持打开 - 可以手动操作或调试")
print("=" * 70)

# 保持运行（浏览器不关闭）
wait()
