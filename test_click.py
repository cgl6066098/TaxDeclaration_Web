"""
测试点击账务中心
使用浏览器管理器 - 支持前台/后台模式配置

使用方法:
    python test_click.py                    # 默认：前台保持打开
    python test_click.py --headless         # 后台无头模式
    python test_click.py --keep-alive       # 明确指定保持打开
    python test_click.py --no-keep-alive    # 不保持打开（完成后关闭）
"""
from 纳税申报模块.browser import get_page, screenshot, wait, set_keep_alive
import time
import argparse

# 默认登录信息
SHEHUI_XINYONG = "913301040709922876"
PHONE_NUMBER = "15606523222"
PASSWORD = "Cgl@6066098"

LOGIN_URL = "https://tpass.zhejiang.chinatax.gov.cn:8443/#/login?redirect_uri=https%3A%2F%2Fetax.zhejiang.chinatax.gov.cn%3A8443%2Fmhzx%2Fapi%2Fmh%2Ftpass%2Fcode&client_id=tct8zta97w6c46zdt9zc2648227df5z2&response_type=code&state=232c3847df0f4f36a00c1b5e55ca3fe9"


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='测试点击账务中心')
    
    parser.add_argument('--headless', action='store_true',
                        help='无头模式（后台运行，不显示窗口）')
    parser.add_argument('--keep-alive', action='store_true', default=True,
                        help='保持浏览器打开（默认）')
    parser.add_argument('--no-keep-alive', action='store_false', dest='keep_alive',
                        help='不保持浏览器打开（完成后关闭）')
    parser.add_argument('--auto-verify', action='store_true',
                        help='自动完成验证码（跳过手动确认）')
    
    return parser.parse_args()


def login(page):
    """执行登录流程"""
    print("\n" + "=" * 70)
    print("登录流程")
    print("=" * 70)
    
    # 访问登录页面
    print("\n[1/6] 访问登录页面...")
    page.goto(LOGIN_URL)
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    screenshot("01_login_page")
    print("      完成")
    
    # 点击代理业务
    print("[2/6] 点击 '代理业务'...")
    page.locator('text=代理业务').first.click()
    time.sleep(1)
    screenshot("02_daili")
    print("      完成")
    
    # 填写登录信息
    print(f"[3/6] 填写社会信用代码：{SHEHUI_XINYONG}")
    page.locator('input[placeholder*="代理机构统一社会信用代码"]').first.fill(SHEHUI_XINYONG)
    time.sleep(0.5)
    print("      完成")
    
    print(f"[4/6] 填写手机号码：{PHONE_NUMBER}")
    page.locator('input[placeholder*="手机号码"]').first.fill(PHONE_NUMBER)
    time.sleep(0.5)
    print("      完成")
    
    print(f"[5/6] 填写密码：{'*' * len(PASSWORD)}")
    page.locator('input[type="password"]').first.fill(PASSWORD)
    time.sleep(0.5)
    print("      完成")
    
    # 点击登录
    print("[6/6] 点击 '登录' 按钮...")
    page.locator('button:has-text("登录")').first.click()
    time.sleep(3)
    screenshot("04_after_login")
    print("      完成")
    
    return page


def find_elements(page, keywords=None):
    """查找页面上的元素"""
    if keywords is None:
        keywords = ["财务", "账务", "中心", "会计", "税务", "申报", "我的"]
    
    print("\n查找页面上的菜单项...")
    elements = page.locator("a, button, div[role='menuitem'], div[role='button'], span, label")
    count = elements.count()
    
    print(f"\n找到 {count} 个元素")
    
    found_items = []
    for i in range(min(count, 50)):
        try:
            elem = elements.nth(i)
            if elem.is_visible():
                text = elem.inner_text().strip()
                if text and len(text) < 50:
                    highlight = ""
                    for kw in keywords:
                        if kw in text:
                            highlight = " <--"
                            found_items.append((i, text))
                            break
                    print(f"  [{i:2d}] {text}{highlight}")
        except:
            pass
    
    print(f"\n找到 {len(found_items)} 个相关元素:")
    for idx, text in found_items:
        print(f"  [{idx}] {text}")
    
    return found_items


def main():
    """主函数"""
    args = parse_args()
    
    print("=" * 70)
    print("测试点击账务中心")
    print("=" * 70)
    print(f"无头模式：{args.headless}")
    print(f"保持打开：{args.keep_alive}")
    print(f"自动验证：{args.auto_verify}")
    print("=" * 70)
    
    # 设置保持打开模式
    set_keep_alive(args.keep_alive)
    
    # 获取浏览器
    page = get_page(headless=args.headless, keep_alive=args.keep_alive)
    
    # 执行登录
    login(page)
    
    print("\n" + "=" * 70)
    if args.auto_verify:
        print("自动验证模式 - 等待 5 秒...")
        time.sleep(5)
    else:
        print("验证码已显示！")
        print("=" * 70)
        print("\n请在浏览器窗口中手动完成验证码")
        print("完成后，按回车键继续...")
        input("\n按回车键继续...")
    
    screenshot("verified")
    print("\n[OK] 验证码已完成")
    
    # 等待页面加载
    time.sleep(3)
    screenshot("dashboard")
    
    # 显示当前状态
    print(f"\n当前 URL: {page.url}")
    print(f"页面标题：{page.title()}")
    
    # 查找元素
    find_elements(page)
    
    # 保持运行
    print("\n" + "=" * 70)
    if args.keep_alive:
        wait("浏览器保持打开 - 可以手动操作或调试")
    else:
        wait("操作完成，按任意键关闭浏览器...")


if __name__ == "__main__":
    main()
