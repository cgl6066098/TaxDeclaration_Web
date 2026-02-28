"""
页面识别工具模块
提供页面元素识别、内容提取、截图对比等功能
"""
from playwright.sync_api import Page, Locator
import time
from typing import List, Dict, Optional, Tuple


class PageUtils:
    """页面工具类 - 用于识别和操作页面元素"""
    
    def __init__(self, page: Page):
        """
        初始化工具类
        
        Args:
            page: Playwright Page 对象
        """
        self.page = page
    
    def find_by_text(self, text: str, exact: bool = False) -> Optional[Locator]:
        """
        通过文本查找元素
        
        Args:
            text: 要查找的文本
            exact: 是否精确匹配
            
        Returns:
            Locator 对象，未找到返回 None
        """
        if exact:
            return self.page.locator(f'text="{text}"').first
        else:
            return self.page.locator(f'text={text}').first
    
    def find_by_selector(self, selector: str) -> Optional[Locator]:
        """
        通过 CSS 选择器查找元素
        
        Args:
            selector: CSS 选择器
            
        Returns:
            Locator 对象，未找到返回 None
        """
        return self.page.locator(selector).first
    
    def find_by_placeholder(self, placeholder: str) -> Optional[Locator]:
        """
        通过 placeholder 查找输入框
        
        Args:
            placeholder: 占位符文本
            
        Returns:
            Locator 对象，未找到返回 None
        """
        return self.page.locator(f'input[placeholder="{placeholder}"]').first
    
    def find_by_label(self, label: str) -> Optional[Locator]:
        """
        通过 label 查找关联的输入框
        
        Args:
            label: 标签文本
            
        Returns:
            Locator 对象，未找到返回 None
        """
        # 先找 label 元素，然后找关联的 input
        label_element = self.page.locator(f'label:has-text("{label}")').first
        if label_element:
            # 尝试找同一容器内的 input
            parent = label_element.locator("..")
            input_elem = parent.locator("input").first
            if input_elem.count() > 0:
                return input_elem
        return None
    
    def is_visible(self, selector_or_text: str) -> bool:
        """
        检查元素是否可见
        
        Args:
            selector_or_text: 选择器或文本
            
        Returns:
            True 如果元素可见
        """
        try:
            locator = self.find_by_text(selector_or_text)
            if locator:
                return locator.is_visible()
            return False
        except:
            return False
    
    def get_element_text(self, selector: str) -> str:
        """
        获取元素文本内容
        
        Args:
            selector: CSS 选择器
            
        Returns:
            元素文本
        """
        element = self.find_by_selector(selector)
        if element and element.count() > 0:
            return element.inner_text()
        return ""
    
    def get_all_links(self) -> List[Dict[str, str]]:
        """
        获取页面所有链接信息
        
        Returns:
            链接信息列表 [{text, href}]
        """
        links = []
        elements = self.page.locator("a")
        count = elements.count()
        
        for i in range(min(count, 50)):  # 最多获取 50 个
            try:
                elem = elements.nth(i)
                if elem.is_visible():
                    text = elem.inner_text().strip()
                    href = elem.get_attribute("href") or ""
                    links.append({"text": text, "href": href})
            except:
                continue
        return links
    
    def get_all_buttons(self) -> List[str]:
        """
        获取页面所有按钮文本
        
        Returns:
            按钮文本列表
        """
        buttons = []
        elements = self.page.locator("button, input[type=button], input[type=submit]")
        count = elements.count()
        
        for i in range(min(count, 30)):
            try:
                elem = elements.nth(i)
                if elem.is_visible():
                    text = elem.inner_text() or elem.get_attribute("value") or ""
                    text = text.strip()
                    if text:
                        buttons.append(text)
            except:
                continue
        return buttons
    
    def get_form_fields(self) -> List[Dict[str, str]]:
        """
        获取页面所有表单字段信息
        
        Returns:
            表单字段信息列表 [{type, name, placeholder, label}]
        """
        fields = []
        inputs = self.page.locator("input, textarea, select")
        count = inputs.count()
        
        for i in range(min(count, 30)):
            try:
                elem = inputs.nth(i)
                if elem.is_visible():
                    field_info = {
                        "type": elem.get_attribute("type") or "text",
                        "name": elem.get_attribute("name") or "",
                        "placeholder": elem.get_attribute("placeholder") or "",
                        "id": elem.get_attribute("id") or "",
                    }
                    fields.append(field_info)
            except:
                continue
        return fields
    
    def analyze_page(self) -> Dict:
        """
        分析当前页面，返回综合信息
        
        Returns:
            页面分析结果字典
        """
        return {
            "url": self.page.url,
            "title": self.page.title(),
            "links_count": len(self.get_all_links()),
            "buttons": self.get_all_buttons(),
            "form_fields": self.get_form_fields(),
        }
    
    def wait_for_element(self, selector_or_text: str, timeout: int = 5000) -> bool:
        """
        等待元素出现
        
        Args:
            selector_or_text: 选择器或文本
            timeout: 超时时间（毫秒）
            
        Returns:
            True 如果元素出现
        """
        try:
            self.page.wait_for_selector(
                f'text={selector_or_text}' if not selector_or_text.startswith(('css=', 'text=')) else selector_or_text,
                timeout=timeout,
                state="visible"
            )
            return True
        except:
            return False
    
    def wait_for_navigation(self, timeout: int = 30000):
        """等待页面导航完成"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def scroll_to_bottom(self):
        """滚动到页面底部"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)
    
    def scroll_to_top(self):
        """滚动到页面顶部"""
        self.page.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.5)


def analyze(page: Page) -> Dict:
    """便捷函数：分析页面"""
    utils = PageUtils(page)
    return utils.analyze_page()
