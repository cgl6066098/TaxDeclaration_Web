# 知乎自动化 - 长连接浏览器方案

## 使用方法

### 方案 1：最简单 - 持久化上下文（推荐）

直接运行 `browser.py`，每次都会复用同一个浏览器配置文件：

```bash
C:\Users\15606\miniconda3\envs\tax_python\python.exe browser.py
```

**特点：**
- 浏览器状态保存在 `browser_profile` 目录
- 下次运行时，登录状态、Cookie 都会保留
- 适合需要长期保持登录状态的场景

---

### 方案 2：CDP 连接（高级）

1. 先运行 `start_browser.py` 启动浏览器（保持运行）
2. 然后可以多次运行 `connect_browser.py` 连接到同一个浏览器执行操作

**特点：**
- 浏览器可以一直运行不关闭
- 可以多次连接执行不同操作
- 适合需要频繁操作的场景

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `browser.py` | 持久化浏览器（推荐） |
| `start_browser.py` | 启动浏览器（CDP 模式） |
| `connect_browser.py` | 连接已运行的浏览器 |
| `run_edge.py` | 直接启动 Edge |
| `connect_edge.py` | 连接 Edge 并操作 |

---

## 快速开始

1. 双击 `启动浏览器.bat` 打开浏览器
2. 双击 `连接浏览器.bat` 连接并执行操作

或者直接运行：
```bash
python browser.py
```
