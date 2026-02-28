"""
纳税申报主流程模块
提供完整的纳税申报自动化流程
"""
import os
import sys
from datetime import datetime
from typing import Optional, Dict

# 添加模块路径
sys.path.insert(0, os.path.dirname(__file__))

from browser_manager import BrowserManager, create_browser
from page_utils import PageUtils
from config import Config, Logger, init_logging


class TaxFiling:
    """纳税申报主类"""
    
    def __init__(self):
        """初始化纳税申报模块"""
        Config.init_dirs()
        self.logger = Logger.get_logger("tax_filing")
        self.browser: Optional[BrowserManager] = None
        self.page_utils = None
        
        # 申报数据
        self.filing_data = {
            "taxpayer_id": "",  # 纳税人识别号
            "tax_period": "",   # 所属时期
            "tax_type": "",     # 税种
            "revenue": 0,       # 营业收入
            "tax_amount": 0,    # 应纳税额
        }
        
    def start(self, headless: bool = False) -> 'TaxFiling':
        """
        启动浏览器
        
        Args:
            headless: 是否无头模式
            
        Returns:
            self
        """
        self.logger.info("=" * 60)
        self.logger.info("纳税申报系统 - 启动")
        self.logger.info("=" * 60)
        
        self.browser = create_browser(
            user_data_dir=Config.BROWSER_PROFILE_DIR,
            screenshot_dir=Config.SCREENSHOT_DIR
        )
        self.browser.start(headless=headless)
        self.page_utils = PageUtils(self.browser.get_page())
        
        self.logger.info("浏览器已启动")
        return self
    
    def login(self, username: str = None, password: str = None) -> 'TaxFiling':
        """
        登录电子税务局
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            self
        """
        self.logger.info("\n[阶段] 登录电子税务局")
        
        # 访问电子税务局
        self.browser.goto(Config.TAX_WEBSITE_URL)
        
        # 分析登录页面
        page_info = self.page_utils.analyze_page()
        self.logger.info(f"当前页面：{page_info['title']}")
        self.logger.info(f"可用按钮：{page_info['buttons']}")
        
        # 查找登录方式
        if self.page_utils.is_visible("密码登录"):
            self.logger.info("检测到密码登录选项")
            self.browser.click("密码登录", "切换到密码登录")
        
        # 填写用户名
        if username:
            self.logger.info("填写用户名")
            # 尝试多种选择器
            for selector in ['input[name="username"]', 'input[placeholder*="用户名"]', 
                           'input[placeholder*="手机号"]', '#username']:
                if self.page_utils.is_visible(selector):
                    self.browser.fill(selector, username, f"填写用户名：{username}")
                    break
        
        # 填写密码
        if password:
            self.logger.info("填写密码")
            for selector in ['input[name="password"]', 'input[type="password"]']:
                if self.page_utils.is_visible(selector):
                    self.browser.fill(selector, password, "填写密码")
                    break
        
        # 点击登录按钮
        self.logger.info("点击登录")
        for btn_text in ['登录', '立即登录', '登 录']:
            if self.page_utils.is_visible(btn_text):
                self.browser.click(btn_text, "点击登录按钮")
                break
        
        self.browser.wait(3)
        self.logger.info("登录操作完成")
        return self
    
    def navigate_to_filing(self) -> 'TaxFiling':
        """
        导航到申报页面
        
        Returns:
            self
        """
        self.logger.info("\n[阶段] 导航到申报页面")
        
        # 查找申报菜单
        filing_menus = ['我要办税', '纳税申报', '申报缴税', '综合申报']
        
        for menu in filing_menus:
            if self.page_utils.is_visible(menu):
                self.logger.info(f"找到菜单：{menu}")
                self.browser.click(menu, f"点击{menu}")
                self.browser.wait(2)
        
        self.logger.info("导航完成")
        return self
    
    def fill_tax_form(self, filing_data: Dict = None) -> 'TaxFiling':
        """
        填写申报表
        
        Args:
            filing_data: 申报数据字典
            
        Returns:
            self
        """
        self.logger.info("\n[阶段] 填写申报表")
        
        data = filing_data or self.filing_data
        
        # 分析页面表单字段
        fields = self.page_utils.get_form_fields()
        self.logger.info(f"检测到 {len(fields)} 个表单字段")
        
        # 填写收入数据
        if data.get("revenue"):
            self.logger.info(f"填写营业收入：{data['revenue']}")
            for selector in ['input[name="revenue"]', 'input[placeholder*="收入"]',
                           'input[placeholder*="销售额"]']:
                if self.page_utils.is_visible(selector):
                    self.browser.fill(selector, str(data['revenue']), "填写营业收入")
                    break
        
        # 填写税额数据
        if data.get("tax_amount"):
            self.logger.info(f"填写应纳税额：{data['tax_amount']}")
            for selector in ['input[name="tax_amount"]', 'input[placeholder*="税额"]']:
                if self.page_utils.is_visible(selector):
                    self.browser.fill(selector, str(data['tax_amount']), "填写应纳税额")
                    break
        
        self.logger.info("申报表填写完成")
        return self
    
    def submit_filing(self) -> 'TaxFiling':
        """
        提交申报
        
        Returns:
            self
        """
        self.logger.info("\n[阶段] 提交申报")
        
        # 查找提交按钮
        submit_buttons = ['提交', '申报', '立即申报', '确认申报']
        
        for btn in submit_buttons:
            if self.page_utils.is_visible(btn):
                self.logger.info(f"点击{btn}按钮")
                self.browser.click(btn, f"点击{btn}")
                self.browser.wait(3)
                break
        
        # 处理确认对话框
        confirm_buttons = ['确定', '确认', '是', 'OK']
        for btn in confirm_buttons:
            if self.page_utils.is_visible(btn):
                self.logger.info(f"点击{btn}确认")
                self.browser.click(btn, f"确认{btn}")
                self.browser.wait(2)
                break
        
        self.logger.info("申报提交完成")
        return self
    
    def save_result(self) -> 'TaxFiling':
        """
        保存申报结果
        
        Returns:
            self
        """
        self.logger.info("\n[阶段] 保存申报结果")
        
        # 截图保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_path = self.browser.screenshot(f"filing_result_{timestamp}")
        
        self.logger.info(f"申报结果截图：{result_path}")
        return self
    
    def close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        self.logger.info("纳税申报系统 - 已关闭")
    
    def run_demo(self) -> 'TaxFiling':
        """
        运行演示流程（以知乎登录为例）
        
        Returns:
            self
        """
        self.logger.info("\n" + "=" * 60)
        self.logger.info("运行演示流程 - 知乎登录")
        self.logger.info("=" * 60)
        
        # 访问知乎
        self.browser.goto("https://www.zhihu.com/signin")
        
        # 分析页面
        page_info = self.page_utils.analyze_page()
        self.logger.info(f"页面标题：{page_info['title']}")
        self.logger.info(f"可用按钮：{page_info['buttons']}")
        
        # 检查登录方式
        if self.page_utils.is_visible("验证码登录"):
            self.logger.info("当前默认：验证码登录")
        
        if self.page_utils.is_visible("密码登录"):
            self.logger.info("检测到密码登录选项")
            self.browser.click("密码登录", "切换到密码登录")
            
            # 验证切换
            if self.page_utils.is_visible("密码"):
                self.logger.info("已成功切换到密码登录界面")
        
        # 保存结果
        self.browser.screenshot("zhihu_demo")
        
        return self
    
    def __enter__(self):
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 便捷函数
def create_tax_filing() -> TaxFiling:
    """创建纳税申报实例"""
    return TaxFiling()


def run_demo():
    """运行演示"""
    with create_tax_filing() as tax:
        tax.run_demo()


if __name__ == "__main__":
    run_demo()
