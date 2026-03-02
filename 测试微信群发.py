# -*- coding: utf-8 -*-
"""
微信群发测试工具
用于测试将文件发送到多个微信聊天

注意：此脚本需要 Python 环境，建议在 Windows 10/11 上运行
Windows 7 用户请使用 微信发送工具_Win7.vbs
"""

import os
import sys
import shutil
from pathlib import Path

# 微信文件目录
WECHAT_FILES_DIR = Path.home() / "Documents" / "WeChat Files"


class WeChatMultiSender:
    """微信多发送工具类"""
    
    def __init__(self):
        self.wechat_dir = WECHAT_FILES_DIR
        self.user = None
        self.sent_count = 0
        self.failed_count = 0
    
    def find_wechat_users(self):
        """查找所有微信用户"""
        if not self.wechat_dir.exists():
            print("错误：未找到微信文件目录")
            print(f"检查路径：{self.wechat_dir}")
            return []
        
        users = []
        for item in self.wechat_dir.iterdir():
            if item.is_dir() and item.name != "All Users":
                users.append(item.name)
        
        return users
    
    def select_user(self, users):
        """选择微信用户"""
        if len(users) == 0:
            print("未找到微信用户")
            return None
        
        if len(users) == 1:
            print(f"\n找到微信账号：{users[0]}")
            return users[0]
        
        print("\n找到多个微信账号:")
        for i, user in enumerate(users, 1):
            print(f"  [{i}] {user}")
        
        try:
            choice = input("\n请选择微信账号 (输入序号，默认 1): ").strip()
            idx = int(choice) - 1 if choice else 0
            return users[idx] if 0 <= idx < len(users) else users[0]
        except:
            return users[0]
    
    def get_chat_dirs(self, user):
        """获取所有可能的聊天目录"""
        base = self.wechat_dir / user
        chat_dirs = []
        
        # 查找 Chat 目录
        chat_dir = base / "Chat"
        if chat_dir.exists():
            for item in chat_dir.iterdir():
                if item.is_dir():
                    chat_dirs.append(item.name)
        
        return chat_dirs
    
    def send_to_chat(self, file_path, user, chat_name):
        """发送文件到指定聊天"""
        if not os.path.exists(file_path):
            print(f"错误：文件不存在 - {file_path}")
            self.failed_count += 1
            return False
        
        # 确定目标目录
        if chat_name == "文件传输助手":
            target_dir = self.wechat_dir / user / "Msg" / "Attachment"
        else:
            target_dir = self.wechat_dir / user / "Chat" / chat_name / "Attachment"
        
        # 创建目录
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"错误：无法创建目录 - {target_dir}")
            print(f"详情：{e}")
            self.failed_count += 1
            return False
        
        # 复制文件
        file_name = os.path.basename(file_path)
        target_path = target_dir / file_name
        
        try:
            shutil.copy2(file_path, target_path)
            print(f"  ✓ 已发送：{chat_name}")
            self.sent_count += 1
            return True
        except Exception as e:
            print(f"  ✗ 发送失败：{chat_name}")
            print(f"    错误：{e}")
            self.failed_count += 1
            return False
    
    def send_to_multiple(self, file_path, user, chat_list):
        """群发到多个聊天"""
        print(f"\n准备发送到 {len(chat_list)} 个聊天...")
        print(f"文件：{file_path}")
        print()
        
        for chat in chat_list:
            self.send_to_chat(file_path, user, chat)
        
        # 显示统计
        print()
        print("=" * 60)
        print("发送完成!")
        print(f"  成功：{self.sent_count} 个")
        print(f"  失败：{self.failed_count} 个")
        print("=" * 60)


def main():
    """主函数"""
    print("=" * 60)
    print("微信群发测试工具")
    print("=" * 60)
    
    sender = WeChatMultiSender()
    
    # 查找微信用户
    print("\n正在查找微信用户...")
    users = sender.find_wechat_users()
    
    if not users:
        print("\n未找到微信用户，请确认:")
        print("  1. 微信已安装")
        print("  2. 微信已登录")
        print("  3. 微信文件目录存在")
        input("\n按回车键退出...")
        return
    
    # 选择用户
    user = sender.select_user(users)
    if not user:
        input("\n按回车键退出...")
        return
    
    # 获取聊天列表
    print("\n正在获取聊天列表...")
    chat_dirs = sender.get_chat_dirs(user)
    
    if not chat_dirs:
        print("未找到聊天目录")
        input("\n按回车键退出...")
        return
    
    print(f"找到 {len(chat_dirs)} 个聊天")
    
    # 选择要发送的文件
    print("\n请选择要发送的文件:")
    print("  [1] 登录模块 (登录.py)")
    print("  [2] 浏览器管理模块 (browser.py)")
    print("  [3] 使用说明文档 (使用说明.md)")
    print("  [4] 自定义文件")
    
    file_choice = input("\n请输入选项 (1-4): ").strip()
    
    file_map = {
        "1": "纳税申报模块/执行模块/登录.py",
        "2": "纳税申报模块/执行模块/browser.py",
        "3": "纳税申报模块/执行模块/使用说明.md",
    }
    
    if file_choice in file_map:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, file_map[file_choice])
    else:
        file_path = input("请输入文件路径：").strip().strip('"')
    
    # 确认文件
    if not os.path.exists(file_path):
        print(f"\n错误：文件不存在 - {file_path}")
        input("\n按回车键退出...")
        return
    
    # 选择发送方式
    print("\n发送方式:")
    print("  [1] 发送到所有聊天（群发）")
    print("  [2] 选择部分聊天发送")
    print("  [3] 只发送到文件传输助手")
    
    send_choice = input("\n请输入选项 (1-3): ").strip()
    
    chat_list = []
    
    if send_choice == "1":
        # 群发所有
        chat_list = chat_dirs + ["文件传输助手"]
        print(f"\n将发送到 {len(chat_list)} 个聊天")
        
        confirm = input("\n确认发送？(y/n): ").strip().lower()
        if confirm != 'y':
            print("已取消")
            input("\n按回车键退出...")
            return
    
    elif send_choice == "2":
        # 选择部分
        print("\n聊天列表:")
        for i, chat in enumerate(chat_dirs, 1):
            print(f"  [{i:2d}] {chat}")
        
        print("\n请输入要发送的聊天序号（用逗号分隔，如：1,3,5）:")
        indices = input("> ").strip()
        
        try:
            idx_list = [int(x.strip()) - 1 for x in indices.split(",")]
            chat_list = [chat_dirs[i] for i in idx_list if 0 <= i < len(chat_dirs)]
            chat_list.append("文件传输助手")
        except:
            print("输入无效")
            input("\n按回车键退出...")
            return
    
    else:
        # 只发送到文件传输助手
        chat_list = ["文件传输助手"]
    
    # 执行发送
    print()
    sender.send_to_multiple(file_path, user, chat_list)
    
    input("\n按回车键退出...")


if __name__ == "__main__":
    main()
