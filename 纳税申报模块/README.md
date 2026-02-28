# 纳税申报自动化模块

## 目录结构

```
纳税申报/
├── 纳税申报模块/
│   ├── __init__.py          # 模块初始化
│   ├── browser_manager.py   # 浏览器管理模块
│   ├── page_utils.py        # 页面识别工具
│   ├── tax_filing.py        # 纳税申报主流程
│   ├── config.py            # 配置和日志
│   ├── run.py               # 运行脚本
│   ├── logs/                # 日志目录
│   ├── screenshots/         # 截图目录
│   ├── data/                # 数据目录
│   └── browser_profile/     # 浏览器配置目录
├── 启动纳税申报.bat         # 一键启动脚本
└── README.md                # 本文档
```

## 快速开始

### 方法 1：双击批处理文件
```
双击：启动纳税申报.bat
```

### 方法 2：Python 命令行
```bash
C:\Users\15606\miniconda3\envs\tax_python\python.exe 纳税申报模块\run.py
```

### 方法 3：代码调用
```python
from 纳税申报模块 import TaxFiling

with TaxFiling() as tax:
    tax.start()
    tax.run_demo()  # 运行演示
```

## 模块说明

### 1. BrowserManager - 浏览器管理

```python
from browser_manager import create_browser

browser = create_browser()
browser.start()
browser.goto("https://example.com")
browser.click("登录")
browser.fill("input[name=username]", "admin")
browser.screenshot("page")
browser.close()
```

**功能：**
- 浏览器启动/关闭
- 自动截图录制
- 持久化会话（保持登录状态）

### 2. PageUtils - 页面识别

```python
from page_utils import PageUtils

utils = PageUtils(page)

# 查找元素
element = utils.find_by_text("密码登录")
element = utils.find_by_selector("input[name=username]")
element = utils.find_by_placeholder("请输入手机号")

# 检查可见性
if utils.is_visible("提交按钮"):
    print("按钮可见")

# 页面分析
info = utils.analyze_page()
print(info["buttons"])  # 所有按钮
print(info["form_fields"])  # 所有表单字段
```

**功能：**
- 文本/选择器查找元素
- 页面内容分析
- 表单字段识别

### 3. TaxFiling - 纳税申报流程

```python
from tax_filing import TaxFiling

tax = TaxFiling()
tax.start()
tax.login(username="xxx", password="xxx")
tax.navigate_to_filing()
tax.fill_tax_form({"revenue": 100000, "tax_amount": 5000})
tax.submit_filing()
tax.save_result()
tax.close()
```

**功能：**
- 登录电子税务局
- 导航到申报页面
- 填写申报表
- 提交申报
- 保存结果

## 配置说明

编辑 `config.py` 修改配置：

```python
# 网站配置
TAX_WEBSITE_URL = "https://etax.chinatax.gov.cn/"

# 浏览器配置
BROWSER_HEADLESS = False  # False=显示窗口，True=后台运行

# 超时配置
NAVIGATION_TIMEOUT = 30000  # 导航超时（毫秒）
```

## 日志和截图

- **日志文件**: `纳税申报模块/logs/`
- **截图文件**: `纳税申报模块/screenshots/`

每次操作都会自动截图并记录日志。

## 功能特点

| 功能 | 说明 |
|------|------|
| 持久化会话 | 登录状态自动保存，下次无需重新登录 |
| 自动截图 | 每个操作步骤自动截图记录 |
| 页面识别 | 智能识别页面元素和表单字段 |
| 日志记录 | 详细的操作日志和错误日志 |
| 长连接 | 浏览器保持打开，可多次执行操作 |

## 注意事项

1. 首次运行会创建浏览器配置文件目录
2. 确保已安装 Python 3.12 和 Playwright
3. 确保系统已安装 Microsoft Edge 浏览器
4. 纳税申报功能需要根据实际税务局网站调整
