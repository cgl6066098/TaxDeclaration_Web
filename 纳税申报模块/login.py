"""
登录模块 - 知乎和电子税务局
已验证可用的登录实现
"""
from playwright.sync_api import sync_playwright
import time
import os


class Login:
    """登录类"""
    
    def __init__(self, headless: bool = False):
        """
        初始化登录
        
        Args:
            headless: 是否无头模式
        """
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
    def start(self) -> 'Login':
        """启动浏览器"""
        print("=" * 60)
        print("启动浏览器")
        print("=" * 60)
        
        self.playwright = sync_playwright().start()
        
        # 使用 Edge 浏览器（系统已安装）
        self.browser = self.playwright.chromium.launch(
            channel="msedge",
            headless=self.headless,
            args=["--no-first-run", "--no-default-browser-check"]
        )
        
        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        
        self.page = self.context.new_page()
        
        print("[OK] 浏览器已启动")
        return self
    
    def login_zhihu(self, username: str = None, password: str = None) -> 'Login':
        """
        登录知乎
        
        Args:
            username: 手机号/邮箱
            password: 密码
        """
        print("\n" + "=" * 60)
        print("知乎登录")
        print("=" * 60)
        
        # 访问知乎登录页
        print("\n访问知乎登录页...")
        self.page.goto("https://www.zhihu.com/signin")
        self.page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # 分析页面
        print(f"页面：{self.page.title()}")
        
        # 查找密码登录
        pwd_tab = self.page.locator('text=密码登录').first
        yan_tab = self.page.locator('text=验证码登录').first
        
        print(f"验证码登录可见：{yan_tab.is_visible()}")
        print(f"密码登录可见：{pwd_tab.is_visible()}")
        
        # 切换到密码登录
        if pwd_tab.is_visible():
            print("\n点击密码登录...")
            pwd_tab.click()
            time.sleep(2)
            
            # 验证切换
            password_input = self.page.locator('input[type="password"]')
            if password_input.is_visible():
                print("[OK] 已切换到密码登录界面")
        
        # 填写账号
        if username:
            print(f"\n填写账号：{username}")
            text_input = self.page.locator('input[type="text"]').first
            if text_input.is_visible():
                text_input.fill(username)
                time.sleep(0.5)
        
        # 填写密码
        if password:
            print(f"填写密码：{'*' * len(password)}")
            password_input = self.page.locator('input[type="password"]').first
            if password_input.is_visible():
                password_input.fill(password)
                time.sleep(0.5)
        
        # 截图
        screenshot_path = os.path.join(os.path.dirname(__file__), "login_result.png")
        self.page.screenshot(path=screenshot_path)
        print(f"\n截图已保存：{screenshot_path}")
        
        if username and password:
            # 点击登录
            print("\n点击登录按钮...")
            login_btn = self.page.locator('button:has-text("登录")').first
            if login_btn.is_visible():
                login_btn.click()
                time.sleep(3)
        
        return self
    
    def close(self):
        """关闭浏览器"""
        print("\n关闭浏览器...")
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("[OK] 浏览器已关闭")
    
    def wait(self):
        """保持浏览器打开"""
        print("\n浏览器保持打开，按 Ctrl+C 关闭...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n退出")
            self.close()


def login_zhihu(username: str = None, password: str = None, keep_open: bool = True):
    """
    快捷登录知乎函数
    
    Args:
        username: 手机号/邮箱
        password: 密码
        keep_open: 是否保持浏览器打开
    """
    login = Login()
    login.start()
    login.login_zhihu(username, password)
    
    if keep_open:
        login.wait()
    else:
        login.close()


if __name__ == "__main__":
    print("=" * 60)
    print("登录模块 - 测试")
    print("=" * 60)
    
    # 登录知乎（不带账号密码，手动输入）
    login_zhihu()
