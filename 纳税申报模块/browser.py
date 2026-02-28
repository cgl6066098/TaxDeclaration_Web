"""
浏览器管理模块
- 自动检测 Edge 浏览器是否已打开
- 如果有则连接，没有则创建
- 永久保持浏览器打开，不关闭
- 支持多标签页管理
"""
from playwright.sync_api import sync_playwright, Page, BrowserContext, Browser
import time
import os
import psutil
import subprocess
from typing import Optional, Tuple, List


class BrowserManager:
    """浏览器管理器 - 单例模式，永久保持浏览器"""
    
    _instance: Optional['BrowserManager'] = None
    _playwright = None
    _browser: Optional[Browser] = None
    _context: Optional[BrowserContext] = None
    _page: Optional[Page] = None
    
    # CDP 端口（用于连接现有浏览器）
    CDP_PORT = 9222
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._playwright is not None:
            return
        
        self.screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # 用户数据目录（保持登录状态）
        self.user_data_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "browser_profile"
        )
        os.makedirs(self.user_data_dir, exist_ok=True)
    
    def is_edge_running(self) -> bool:
        """检测是否有 Edge 浏览器在运行"""
        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info.get('cmdline', []) or [])
                if 'msedge' in proc.info['name'].lower() and '--remote-debugging-port' in cmdline:
                    return True
            except:
                pass
        return False
    
    def start_edge_with_cdp(self):
        """启动带 CDP 端口的 Edge 浏览器"""
        edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        
        # 检查是否已有带 CDP 的 Edge 进程
        if self.is_edge_running():
            print("[浏览器] 检测到带 CDP 的 Edge 已在运行")
            return
        
        # 启动 Edge 浏览器（独立进程，带 CDP 端口）
        print("[浏览器] 启动 Edge 浏览器（CDP 模式）...")
        
        args = [
            edge_path,
            f"--remote-debugging-port={self.CDP_PORT}",
            f"--user-data-dir={self.user_data_dir}",
            "--no-first-run",
            "--no-default-browser-check",
        ]
        
        # 后台启动 Edge
        subprocess.Popen(args, creationflags=subprocess.DETACHED_PROCESS)
        time.sleep(3)
    
    def connect_to_edge(self) -> Tuple:
        """连接到现有 Edge 浏览器"""
        print(f"[浏览器] 连接到 CDP 端口 {self.CDP_PORT}...")
        
        self._playwright = sync_playwright().start()
        
        # 通过 CDP 连接
        self._browser = self._playwright.chromium.connect_over_cdp(
            f"http://localhost:{self.CDP_PORT}"
        )
        
        # 获取或创建上下文
        if self._browser.contexts:
            self._context = self._browser.contexts[0]
        else:
            self._context = self._browser.new_context(viewport={"width": 1280, "height": 720})
        
        # 获取或创建页面
        if self._context.pages:
            self._page = self._context.pages[0]
        else:
            self._page = self._context.new_page()
        
        print("[浏览器] 已连接到现有 Edge")
        return self._playwright, self._browser, self._context, self._page
    
    def create_new_browser(self) -> Tuple:
        """创建新浏览器"""
        print("[浏览器] 启动新浏览器...")
        
        self._playwright = sync_playwright().start()
        
        self._browser = self._playwright.chromium.launch(
            channel="msedge",
            headless=False,
            args=[
                "--no-first-run",
                "--no-default-browser-check",
                f"--user-data-dir={self.user_data_dir}",
            ]
        )
        
        self._context = self._browser.new_context(viewport={"width": 1280, "height": 720})
        self._page = self._context.new_page()
        
        print("[浏览器] 浏览器已启动")
        return self._playwright, self._browser, self._context, self._page
    
    def get_or_create(self, headless: bool = False) -> Tuple:
        """
        获取或创建浏览器
        优先连接现有 Edge，没有则创建新的
        """
        # 检查是否已有连接
        if self._playwright is not None and self._browser is not None:
            try:
                _ = self._browser.browser_type
                print("[浏览器] 使用已连接的浏览器")
                return self._playwright, self._browser, self._context, self._page
            except:
                self._cleanup()
        
        # 尝试连接现有 Edge
        self.start_edge_with_cdp()
        time.sleep(2)
        
        try:
            return self.connect_to_edge()
        except Exception as e:
            print(f"[浏览器] 连接失败：{e}")
            print("[浏览器] 创建新浏览器...")
            return self.create_new_browser()
    
    def _cleanup(self):
        """清理（但实际不关闭浏览器）"""
        try:
            if self._context:
                # 只关闭上下文，不关闭浏览器
                pass
            if self._browser:
                # 只断开连接，不关闭浏览器
                pass
            if self._playwright:
                self._playwright.stop()
        except:
            pass
        
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None
    
    def get_page(self, headless: bool = False) -> Page:
        """获取页面对象"""
        _, _, _, page = self.get_or_create(headless)
        return page
    
    def get_page_by_url(self, url_contains: str) -> Optional[Page]:
        """根据 URL 查找或创建页面"""
        _, _, _, _ = self.get_or_create()
        
        # 查找匹配的页面
        for page in self._context.pages:
            if url_contains in page.url:
                print(f"[页面] 找到匹配的页面：{page.url}")
                self._page = page
                return page
        
        # 没有则创建新页面
        print(f"[页面] 创建新页面（URL 包含：{url_contains}）")
        self._page = self._context.new_page()
        return self._page
    
    def list_pages(self) -> List[dict]:
        """列出所有页面"""
        if self._context is None:
            return []
        
        pages = []
        for i, page in enumerate(self._context.pages):
            pages.append({
                "index": i,
                "url": page.url,
                "title": page.title()
            })
        return pages
    
    def screenshot(self, name: str) -> str:
        """截图并保存"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.screenshot_dir, f"{timestamp}_{name}.png")
        self.get_page().screenshot(path=filepath)
        print(f"[截图] {os.path.basename(filepath)}")
        return filepath
    
    def wait(self, message: str = None):
        """保持运行（不关闭浏览器）"""
        if message:
            print(message)
        
        print("\n浏览器保持打开，按 Ctrl+C 退出脚本（浏览器不关闭）...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n退出脚本")
            print("浏览器保持打开状态")


# 全局浏览器管理器实例
browser_manager = BrowserManager()


# 便捷函数
def get_page(headless: bool = False) -> Page:
    """获取页面（自动检测并连接现有浏览器）"""
    return browser_manager.get_page(headless)


def get_page_by_url(url_contains: str) -> Page:
    """根据 URL 获取页面（没有则创建新标签）"""
    return browser_manager.get_page_by_url(url_contains)


def screenshot(name: str) -> str:
    """截图"""
    return browser_manager.screenshot(name)


def list_pages() -> List[dict]:
    """列出所有页面"""
    return browser_manager.list_pages()


def set_keep_alive(keep_alive: bool):
    """设置是否保持浏览器打开"""
    browser_manager._keep_alive = keep_alive
    print(f"[浏览器] 保持打开模式：{'开启' if keep_alive else '关闭'}")


def wait(message: str = None):
    """保持运行"""
    browser_manager.wait(message)


# 测试用
if __name__ == "__main__":
    print("=" * 60)
    print("浏览器管理模块 - 测试")
    print("=" * 60)
    
    # 第一次调用 - 应该启动或连接浏览器
    print("\n[测试 1] 第一次调用...")
    page1 = get_page()
    print(f"页面 URL: {page1.url}")
    
    # 列出页面
    print(f"\n当前页面列表：{list_pages()}")
    
    # 第二次调用 - 应该使用同一浏览器
    print("\n[测试 2] 第二次调用...")
    page2 = get_page()
    print(f"page1 is page2: {page1 is page2}")
    
    # 访问网页
    print("\n[测试 3] 访问网页...")
    page2.goto("https://www.example.com")
    screenshot("test")
    
    print("\n[OK] 浏览器保持打开")
    wait()
