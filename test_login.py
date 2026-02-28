"""
登录测试脚本 - 登录知乎
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "纳税申报模块"))

from login import LoginModule

print("=" * 60)
print("登录测试 - 知乎")
print("=" * 60)

try:
    login = LoginModule()
    login.start()
    login.login_zhihu()
    
    print("\n浏览器保持打开，按 Ctrl+C 关闭...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n退出")
    login.close()
