"""
浏览器管理模块
负责浏览器的启动、连接、关闭以及截图录制功能
"""
from playwright.sync_api import sync_playwright, Page, BrowserContext
import time
import os
from datetime import datetime


class BrowserManager:
    """浏览器管理器 - 支持长连接和全程录制"""
    
    def __init__(self, user_data_dir: str = None, screenshot_dir: str = None):
        """
        初始化浏览器管理器
        
        Args:
            user_data_dir: 用户数据目录，用于保存登录状态
            screenshot_dir: 截图保存目录
        """
        self.user_data_dir = user_data_dir or os.path.join(
            os.path.dirname(__file__), "browser_profile"
        )
        self.screenshot_dir = screenshot_dir or os.path.join(
            os.path.dirname(__file__), "screenshots"
        )
        
        os.makedirs(self.user_data_dir, exist_ok=True)
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        self.playwright = None
        self.context = None
        self.page = None
        self.step_count = 0  # 步骤计数器
        self.screenshot_count = 0  # 截图计数器
        
    def start(self, headless: bool = False) -> 'BrowserManager':
        """
        启动浏览器
        
        Args:
            headless: 是否无头模式，默认 False（显示浏览器窗口）
            
        Returns:
            self
        """
        print("=" * 60)
        print("启动浏览器")
        print("=" * 60)
        print(f"用户数据目录：{self.user_data_dir}")
        print(f"截图保存目录：{self.screenshot_dir}")
        
        self.playwright = sync_playwright().start()
        
        # 使用持久化上下文，保存登录状态
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            channel="msedge",
            headless=headless,
            viewport={"width": 1280, "height": 720},
            args=[
                "--no-first-run",
                "--no-default-browser-check",
            ]
        )
        
        # 获取或创建页面
        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()
            
        print("[OK] 浏览器已启动")
        return self
    
    def goto(self, url: str, wait_state: str = "networkidle") -> 'BrowserManager':
        """
        访问 URL 并自动截图
        
        Args:
            url: 目标网址
            wait_state: 等待状态，默认 networkidle
            
        Returns:
            self
        """
        self.step_count += 1
        print(f"\n[步骤 {self.step_count}] 访问：{url}")
        
        self.page.goto(url)
        self.page.wait_for_load_state(wait_state)
        time.sleep(1)
        
        self._screenshot(f"goto_{self.step_count:03d}")
        return self
    
    def click(self, selector: str, description: str = None) -> 'BrowserManager':
        """
        点击元素并自动截图
        
        Args:
            selector: CSS 选择器或文本
            description: 操作描述
            
        Returns:
            self
        """
        self.step_count += 1
        desc = description or f"点击：{selector}"
        print(f"\n[步骤 {self.step_count}] {desc}")
        
        # 支持 text= 选择器
        if not selector.startswith("text=") and not selector.startswith("css="):
            element = self.page.locator(f'text={selector}').first
        else:
            element = self.page.locator(selector).first
            
        element.click()
        time.sleep(1)
        
        self._screenshot(f"click_{self.step_count:03d}")
        return self
    
    def fill(self, selector: str, value: str, description: str = None) -> 'BrowserManager':
        """
        填写表单并自动截图
        
        Args:
            selector: 输入框选择器
            value: 填写的值
            description: 操作描述
            
        Returns:
            self
        """
        self.step_count += 1
        desc = description or f"填写：{selector} = {value}"
        print(f"\n[步骤 {self.step_count}] {desc}")
        
        self.page.fill(selector, value)
        time.sleep(0.5)
        
        self._screenshot(f"fill_{self.step_count:03d}")
        return self
    
    def screenshot(self, name: str = None) -> str:
        """
        手动截图
        
        Args:
            name: 截图名称
            
        Returns:
            截图路径
        """
        return self._screenshot(name or f"manual_{self.screenshot_count:03d}")
    
    def _screenshot(self, name: str) -> str:
        """内部截图方法"""
        self.screenshot_count += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        self.page.screenshot(path=filepath)
        print(f"  截图：{filename}")
        return filepath
    
    def get_page(self) -> Page:
        """获取当前页面对象"""
        return self.page
    
    def get_context(self) -> BrowserContext:
        """获取浏览器上下文"""
        return self.context
    
    def wait(self, seconds: int) -> 'BrowserManager':
        """等待指定秒数"""
        print(f"  等待 {seconds} 秒...")
        time.sleep(seconds)
        return self
    
    def close(self):
        """关闭浏览器"""
        print("\n" + "=" * 60)
        print("关闭浏览器")
        print("=" * 60)
        
        if self.context:
            self.context.close()
            print("[OK] 浏览器已关闭")
            print(f"截图保存位置：{self.screenshot_dir}")
            print(f"共执行 {self.step_count} 步，截图 {self.screenshot_count} 张")
            
    def __enter__(self):
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 便捷函数
def create_browser(user_data_dir: str = None, screenshot_dir: str = None) -> BrowserManager:
    """创建浏览器管理器实例"""
    return BrowserManager(user_data_dir, screenshot_dir)
