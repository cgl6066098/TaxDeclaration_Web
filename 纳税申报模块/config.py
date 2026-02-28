"""
配置和日志模块
提供统一的配置管理和日志记录功能
"""
import os
import logging
from datetime import datetime
from typing import Optional


class Config:
    """配置管理类"""
    
    # 基础路径
    BASE_DIR = os.path.dirname(__file__)
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    BROWSER_PROFILE_DIR = os.path.join(BASE_DIR, "browser_profile")
    
    # 网站配置
    TAX_WEBSITE_URL = "https://etax.chinatax.gov.cn/"  # 电子税务局
    ZHIHU_URL = "https://www.zhihu.com/"
    
    # 浏览器配置
    BROWSER_CHANNEL = "msedge"
    BROWSER_VIEWPORT_WIDTH = 1280
    BROWSER_VIEWPORT_HEIGHT = 720
    BROWSER_HEADLESS = False  # 默认显示浏览器窗口
    
    # 超时配置
    NAVIGATION_TIMEOUT = 30000  # 导航超时 30 秒
    ACTION_TIMEOUT = 5000  # 操作超时 5 秒
    DEFAULT_WAIT = 2  # 默认等待 2 秒
    
    @classmethod
    def init_dirs(cls):
        """初始化所有目录"""
        for dir_path in [cls.LOG_DIR, cls.SCREENSHOT_DIR, cls.DATA_DIR, cls.BROWSER_PROFILE_DIR]:
            os.makedirs(dir_path, exist_ok=True)
        return cls
    
    @classmethod
    def get_log_file(cls, prefix: str = "tax") -> str:
        """获取日志文件路径"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(cls.LOG_DIR, f"{prefix}_{timestamp}.log")
    
    @classmethod
    def get_screenshot_path(cls, name: str) -> str:
        """获取截图保存路径"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(cls.SCREENSHOT_DIR, f"{timestamp}_{name}.png")


class Logger:
    """日志记录类"""
    
    _instance: Optional[logging.Logger] = None
    
    @classmethod
    def get_logger(cls, name: str = "tax_filing") -> logging.Logger:
        """
        获取日志记录器
        
        Args:
            name: 日志记录器名称
            
        Returns:
            logging.Logger 实例
        """
        if cls._instance is None:
            cls._instance = cls._create_logger(name)
        return cls._instance
    
    @classmethod
    def _create_logger(cls, name: str) -> logging.Logger:
        """创建日志记录器"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # 清除已有的处理器
        logger.handlers.clear()
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # 创建文件处理器
        log_file = Config.get_log_file()
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        return logger
    
    @classmethod
    def set_file(cls, log_file: str):
        """设置日志文件"""
        if cls._instance:
            # 添加新的文件处理器
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_format)
            cls._instance.addHandler(file_handler)


def init_logging() -> logging.Logger:
    """初始化日志系统"""
    Config.init_dirs()
    return Logger.get_logger()


# 便捷函数
def log_info(message: str):
    """记录 INFO 级别日志"""
    Logger.get_logger().info(message)


def log_error(message: str):
    """记录 ERROR 级别日志"""
    Logger.get_logger().error(message)


def log_debug(message: str):
    """记录 DEBUG 级别日志"""
    Logger.get_logger().debug(message)


def log_warning(message: str):
    """记录 WARNING 级别日志"""
    Logger.get_logger().warning(message)
