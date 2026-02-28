# 项目指令 - 纳税申报自动化

## 自动同步到云端

**每次完成一个功能模块的封装后，自动执行"上传代码"指令：**

1. 检查 Git 变更
2. 按模块分组提交
3. 推送到远程仓库

**触发条件：**
- 完成一个封装模块（如 `登录.py`、` 申报.py` 等）
- 用户说"封装 xxx 完成"
- 用户说"上传代码"、"同步到云端"、"push"

**执行流程：**
```
封装完成 → git add → git commit → git push
```

## 浏览器使用规范（重要）

### 默认行为

**所有测试代码和生产代码，浏览器默认配置：**

1. ✅ **永久打开浏览器** - `keep_alive=True`（默认）
2. ✅ **显示浏览器窗口** - `headless=False`（默认）
3. ❌ **不关闭浏览器** - 代码中不包含关闭浏览器的指令
4. ❌ **不设置 timeout** - 运行命令时不设置任何超时限制

### 登录模块功能（必须包含）

**所有登录/浏览器相关代码必须集成以下功能：**

1. ✅ **检测现有浏览器** - 使用 CDP 端口检测 Edge 是否运行
2. ✅ **连接现有浏览器** - 通过 CDP 连接到已有 Edge
3. ✅ **多标签管理** - 列出所有页面，找到匹配的标签
4. ✅ **智能打开** - 不在目标页面时打开/切换到新标签
5. ✅ **永久保持浏览器** - 脚本退出后浏览器继续运行（写入 instruction）
6. ✅ **不设置 timeout** - 没有任何超时限制（写入 instruction）

### 运行命令规范

**运行 Python 脚本时：**
- ❌ 不设置 `timeout` 参数
- ✅ 使用 `is_background=True` 后台启动（让脚本持续运行）
- ✅ 或直接用批处理文件让用户双击运行

```python
# ❌ 错误 - 不要设置 timeout
run_shell_command(command="python test.py", timeout=60000)

# ✅ 正确 - 后台运行，不设置 timeout
run_shell_command(command="python test.py", is_background=True)
```

### 代码要求

#### 1. 浏览器管理器使用

所有代码必须使用 `纳税申报模块/browser.py` 中的浏览器管理器：

```python
from 纳税申报模块.browser import get_page, screenshot, wait

# 默认：前台显示，保持打开
page = get_page()

# 或明确指定
page = get_page(headless=False, keep_alive=True)

# 保持运行
wait()
```

#### 2. 禁止关闭浏览器

代码中**不得包含**以下指令：
- ❌ `browser.close()`
- ❌ `context.close()`
- ❌ `playwright.stop()`
- ❌ `context.__exit__()`

#### 3. 命令行参数默认值

所有脚本的命令行参数默认值：
```python
parser.add_argument('--headless', action='store_true', 
                    default=False,  # 默认显示窗口
                    help='无头模式')
parser.add_argument('--keep-alive', action='store_true', 
                    default=True,   # 默认保持打开
                    help='保持浏览器打开')
```

### 运行方式

#### 推荐：双击批处理文件
```
双击：测试 - 点击账务中心.bat
```

#### 命令行运行
```bash
# 默认：前台显示，保持打开
python test_click.py

# 仅当明确需要后台运行时
python test_click.py --headless --auto-verify
```

### 浏览器检测

所有代码运行第一步：**检测浏览器是否已打开**

```python
from 纳税申报模块.browser import get_page

# 自动检测：
# - 如果浏览器已打开 → 使用现有浏览器
# - 如果浏览器未打开 → 自动打开新浏览器
page = get_page()
```

### 示例代码模板

```python
"""
脚本说明
"""
from 纳税申报模块.browser import get_page, screenshot, wait
import time

# 获取浏览器（默认前台显示，保持打开）
page = get_page()

# 执行操作
page.goto("...")
page.click("...")
screenshot("step1")

# 保持运行（浏览器不关闭）
wait("操作完成，浏览器保持打开")
```

## 项目结构

```
纳税申报/
├── .qwen/
│   └── instruction.md       # 本文件（项目指令）
├── 纳税申报模块/
│   ├── browser.py           # 浏览器管理器（核心）
│   ├── 登录.py              # 登录模块
│   ├── screenshots/         # 截图目录
│   └── ...
├── test_click.py            # 测试脚本
└── *.bat                    # 批处理文件
```

## 依赖安装

```bash
# Python 环境
C:\Users\15606\miniconda3\envs\tax_python\python.exe

# 安装依赖
pip install playwright openpyxl psutil
```

## 登录信息

从 Excel 文件读取：
```
纳税申报模块/员工登录方式/登录密码.xlsx
```

| 字段 | 值 |
|------|-----|
| 社会信用代码 | 913301040709922876 |
| 手机号 | 15606523222 |
| 密码 | Cgl@6066098 |

## 浙江省电子税务局

登录 URL：
```
https://tpass.zhejiang.chinatax.gov.cn:8443/#/login?redirect_uri=https%3A%2F%2Fetax.zhejiang.chinatax.gov.cn%3A8443%2Fmhzx%2Fapi%2Fmh%2Ftpass%2Fcode&client_id=tct8zta97w6c46zdt9zc2648227df5z2&response_type=code&state=232c3847df0f4f36a00c1b5e55ca3fe9
```

登录方式：**代理业务** → 填写信息 → 登录 → 验证码

---

**重要：本文件中的所有浏览器使用规范必须严格遵守！**
