# -*- coding: utf-8 -*-
"""
纳税申报自动化 - Windows 7 兼容版
通过微信发送文件

依赖：
- Python 2.7 或 3.4-3.8（Windows 7 支持）
- 无需额外依赖，只使用标准库

使用方法：
1. 将此文件复制到 Windows 7 电脑
2. 双击运行
3. 按提示操作
"""

import os
import sys
import time
import shutil

# 微信文件目录（需要根据实际路径修改）
WECHAT_FILES_DIR = os.path.expanduser("~/Documents/WeChat Files/")


def find_wechat_user():
    """查找微信用户目录"""
    if not os.path.exists(WECHAT_FILES_DIR):
        print("错误：未找到微信文件目录")
        print("请确认微信已安装并登录")
        return None
    
    # 获取所有微信账号目录
    users = [d for d in os.listdir(WECHAT_FILES_DIR) 
             if d != "All Users" and os.path.isdir(os.path.join(WECHAT_FILES_DIR, d))]
    
    if not users:
        print("错误：未找到微信用户")
        return None
    
    print("\n找到以下微信账号:")
    for i, user in enumerate(users, 1):
        print("  [%d] %s" % (i, user))
    
    # 选择第一个（或让用户选择）
    if len(users) == 1:
        return users[0]
    
    try:
        choice = input("\n请选择微信账号 (输入序号，默认 1): ").strip()
        idx = int(choice) - 1 if choice else 0
        return users[idx] if 0 <= idx < len(users) else users[0]
    except:
        return users[0]


def get_chat_folder(user, chat_name=None):
    """获取聊天文件夹路径"""
    base = os.path.join(WECHAT_FILES_DIR, user)
    
    if chat_name:
        # 特定聊天
        return os.path.join(base, "Chat", chat_name)
    else:
        # 文件传输助手
        return os.path.join(base, "Msg", "Attachment")


def send_file(file_path, chat_name=None):
    """
    发送文件到微信（通过复制到微信文件夹）
    
    注意：这种方法需要微信运行中
    """
    if not os.path.exists(file_path):
        print("错误：文件不存在 - %s" % file_path)
        return False
    
    user = find_wechat_user()
    if not user:
        return False
    
    # 获取目标文件夹
    target_dir = get_chat_folder(user, chat_name)
    
    if not os.path.exists(target_dir):
        print("错误：未找到微信聊天目录 - %s" % target_dir)
        print("请确保微信已运行")
        return False
    
    # 复制文件
    file_name = os.path.basename(file_path)
    target_path = os.path.join(target_dir, file_name)
    
    try:
        shutil.copy2(file_path, target_path)
        print("\n[成功] 文件已复制到微信文件夹:")
        print("  %s" % target_path)
        print("\n请在微信中手动发送该文件")
        return True
    except Exception as e:
        print("\n[失败] 复制文件失败：%s" % str(e))
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("纳税申报 - 微信发送文件工具 (Windows 7 兼容版)")
    print("=" * 60)
    
    # 选择文件
    print("\n请选择要发送的文件:")
    print("  [1] 登录模块 (纳税申报模块/执行模块/登录.py)")
    print("  [2] 浏览器管理模块 (纳税申报模块/执行模块/browser.py)")
    print("  [3] 使用说明文档 (纳税申报模块/执行模块/使用说明.md)")
    print("  [4] 自定义文件")
    
    choice = input("\n请输入选项 (1-4): ").strip()
    
    file_map = {
        "1": "纳税申报模块/执行模块/登录.py",
        "2": "纳税申报模块/执行模块/browser.py",
        "3": "纳税申报模块/执行模块/使用说明.md",
    }
    
    if choice in file_map:
        file_path = os.path.join(os.path.dirname(__file__), file_map[choice])
    else:
        file_path = input("请输入文件路径：").strip().strip('"')
    
    # 确认文件
    if not os.path.exists(file_path):
        print("\n错误：文件不存在 - %s" % file_path)
        return
    
    print("\n准备发送文件:")
    print("  %s" % file_path)
    
    # 选择聊天对象
    print("\n发送到:")
    print("  [1] 文件传输助手")
    print("  [2] 特定聊天")
    
    chat_choice = input("请输入选项 (1-2): ").strip()
    chat_name = None if chat_choice == "1" else input("请输入聊天对象名称：").strip()
    
    # 发送
    print("\n正在发送...")
    if send_file(file_path, chat_name):
        print("\n[完成] 文件已准备发送")
    else:
        print("\n[失败] 发送失败")
    
    print("\n按回车键退出...")
    input()


if __name__ == "__main__":
    main()
