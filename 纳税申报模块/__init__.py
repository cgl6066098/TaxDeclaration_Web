"""
纳税申报自动化模块

功能：
- 浏览器自动化管理
- 页面元素识别
- 纳税申报流程自动化
- 全程截图录制

使用方法：
    from tax_filing import TaxFiling
    
    with TaxFiling() as tax:
        tax.start()
        tax.login(username="xxx", password="xxx")
        tax.navigate_to_filing()
        tax.fill_tax_form(data)
        tax.submit_filing()
"""

from .tax_filing import TaxFiling, create_tax_filing
from .browser_manager import BrowserManager, create_browser
from .page_utils import PageUtils
from .config import Config, Logger

__version__ = "1.0.0"
__all__ = [
    "TaxFiling",
    "create_tax_filing",
    "BrowserManager",
    "create_browser",
    "PageUtils",
    "Config",
    "Logger",
]
