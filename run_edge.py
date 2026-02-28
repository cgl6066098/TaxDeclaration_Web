"""
持久化浏览器会话 - 后台运行版本
使用 subprocess 启动浏览器进程
"""
import subprocess
import time
import os
import sys

USER_DATA_DIR = "C:\\Users\\15606\\miniconda3\\envs\\tax_python\\browser_profile"
os.makedirs(USER_DATA_DIR, exist_ok=True)

# 直接使用 Edge 浏览器启动参数
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

print("=" * 50)
print("持久化浏览器模式")
print("=" * 50)
print(f"用户数据目录：{USER_DATA_DIR}")
print()

# 启动 Edge 浏览器
args = [
    edge_path,
    f"--user-data-dir={USER_DATA_DIR}",
    "--no-first-run",
    "--no-default-browser-check",
    "https://www.zhihu.com/signin",
]

print("正在启动 Edge 浏览器...")
proc = subprocess.Popen(args)

print("[OK] 浏览器已启动")
print("\n按 Ctrl+C 关闭浏览器")

try:
    proc.wait()
except KeyboardInterrupt:
    print("\n正在关闭浏览器...")
    proc.terminate()
    proc.wait()
    print("浏览器已关闭")
