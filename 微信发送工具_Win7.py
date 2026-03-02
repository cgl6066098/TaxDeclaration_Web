# -*- coding: utf-8 -*-
"""
微信发送工具 - Windows 7 兼容版
纯 Python 实现，打包为 EXE

兼容性：Windows 7/8/10/11
Python: 3.8.x
"""

from __future__ import unicode_literals
import os
import sys
import shutil
import ctypes

# 检查是否为 Windows 7
def is_windows_7():
    """检查是否为 Windows 7"""
    try:
        if sys.platform != 'win32':
            return False
        version = sys.getwindowsversion()
        return version.major == 6 and version.minor == 1
    except:
        return False

# 高 DPI 支持
if is_windows_7():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass

# 微信文件目录
if sys.version_info[0] >= 3:
    from pathlib import Path
    WECHAT_DIR = Path.home() / "Documents" / "WeChat Files"
else:
    WECHAT_DIR = os.path.join(os.path.expanduser("~"), "Documents", "WeChat Files")


class WeChatSender:
    """微信发送工具类"""
    
    def __init__(self):
        self.wechat_dir = WECHAT_DIR
        self.user = None
        self.sent_count = 0
        self.failed_count = 0
    
    def find_wechat_users(self):
        """查找所有微信用户"""
        if not os.path.exists(self.wechat_dir):
            return []
        
        users = []
        try:
            for item in os.listdir(self.wechat_dir):
                item_path = os.path.join(self.wechat_dir, item)
                if os.path.isdir(item_path) and item != "All Users":
                    users.append(item)
        except:
            pass
        
        return users
    
    def select_user(self, users):
        """选择微信用户"""
        if len(users) == 0:
            return None
        
        if len(users) == 1:
            print("\n找到微信账号：%s" % users[0])
            return users[0]
        
        print("\n找到多个微信账号:")
        for i, user in enumerate(users, 1):
            print("  [%d] %s" % (i, user))
        
        try:
            if sys.version_info[0] >= 3:
                choice = input("\n请选择微信账号 (输入序号，默认 1): ").strip()
            else:
                choice = raw_input("\n请选择微信账号 (输入序号，默认 1): ").strip()
            idx = int(choice) - 1 if choice else 0
            return users[idx] if 0 <= idx < len(users) else users[0]
        except:
            return users[0]
    
    def get_chat_dirs(self, user):
        """获取所有聊天目录"""
        base = os.path.join(self.wechat_dir, user)
        chat_dirs = []
        
        chat_dir = os.path.join(base, "Chat")
        if os.path.exists(chat_dir):
            try:
                for item in os.listdir(chat_dir):
                    item_path = os.path.join(chat_dir, item)
                    if os.path.isdir(item_path):
                        chat_dirs.append(item)
            except:
                pass
        
        return chat_dirs
    
    def send_to_chat(self, file_path, user, chat_name):
        """发送文件到指定聊天"""
        if not os.path.exists(file_path):
            self.failed_count += 1
            return False
        
        if chat_name == "文件传输助手":
            target_dir = os.path.join(self.wechat_dir, user, "Msg", "Attachment")
        else:
            target_dir = os.path.join(self.wechat_dir, user, "Chat", chat_name, "Attachment")
        
        try:
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
        except:
            self.failed_count += 1
            return False
        
        file_name = os.path.basename(file_path)
        target_path = os.path.join(target_dir, file_name)
        
        try:
            shutil.copy2(file_path, target_path)
            print("  √ 已发送：%s" % chat_name)
            self.sent_count += 1
            return True
        except:
            self.failed_count += 1
            return False
    
    def send_multiple(self, file_path, user, chat_list):
        """群发到多个聊天"""
        print("\n准备发送到 %d 个聊天..." % len(chat_list))
        print("文件：%s" % file_path)
        print()
        
        for chat in chat_list:
            self.send_to_chat(file_path, user, chat)
        
        print("\n" + "=" * 60)
        print("发送完成!")
        print("  成功：%d 个" % self.sent_count)
        print("  失败：%d 个" % self.failed_count)
        print("=" * 60)


def get_script_dir():
    """获取脚本所在目录"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def main():
    """主函数"""
    print("=" * 60)
    print("微信发送工具 - Windows 7 版")
    print("=" * 60)
    
    sender = WeChatSender()
    
    # 查找微信用户
    print("\n正在查找微信用户...")
    users = sender.find_wechat_users()
    
    if not users:
        print("\n未找到微信用户，请确认:")
        print("  1. 微信已安装")
        print("  2. 微信已登录")
        print("  3. 微信文件目录存在")
        if sys.version_info[0] >= 3:
            input("\n按回车键退出...")
        else:
            raw_input("\n按回车键退出...")
        return
    
    # 选择用户
    user = sender.select_user(users)
    if not user:
        if sys.version_info[0] >= 3:
            input("\n按回车键退出...")
        else:
            raw_input("\n按回车键退出...")
        return
    
    # 获取聊天列表
    print("\n正在获取聊天列表...")
    chat_dirs = sender.get_chat_dirs(user)
    
    if not chat_dirs:
        print("未找到聊天目录")
        if sys.version_info[0] >= 3:
            input("\n按回车键退出...")
        else:
            raw_input("\n按回车键退出...")
        return
    
    print("找到 %d 个聊天" % len(chat_dirs))
    
    # 选择文件
    script_dir = get_script_dir()
    
    print("\n请选择要发送的文件:")
    print("  [1] 登录模块 (登录.py)")
    print("  [2] 浏览器管理模块 (browser.py)")
    print("  [3] 使用说明文档 (使用说明.md)")
    print("  [4] 自定义文件")
    
    if sys.version_info[0] >= 3:
        file_choice = input("\n请输入选项 (1-4): ").strip()
    else:
        file_choice = raw_input("\n请输入选项 (1-4): ").strip()
    
    file_map = {
        "1": os.path.join(script_dir, "纳税申报模块", "执行模块", "登录.py"),
        "2": os.path.join(script_dir, "纳税申报模块", "执行模块", "browser.py"),
        "3": os.path.join(script_dir, "纳税申报模块", "执行模块", "使用说明.md"),
    }
    
    if file_choice in file_map:
        file_path = file_map[file_choice]
    else:
        if sys.version_info[0] >= 3:
            file_path = input("请输入文件路径：").strip().strip('"')
        else:
            file_path = raw_input("请输入文件路径：").strip().strip('"')
    
    if not os.path.exists(file_path):
        print("\n错误：文件不存在 - %s" % file_path)
        if sys.version_info[0] >= 3:
            input("\n按回车键退出...")
        else:
            raw_input("\n按回车键退出...")
        return
    
    # 选择发送方式
    print("\n发送方式:")
    print("  [1] 发送到所有聊天（群发）")
    print("  [2] 选择部分聊天发送")
    print("  [3] 只发送到文件传输助手")
    
    if sys.version_info[0] >= 3:
        send_choice = input("\n请输入选项 (1-3): ").strip()
    else:
        send_choice = raw_input("\n请输入选项 (1-3): ").strip()
    
    chat_list = []
    
    if send_choice == "1":
        chat_list = chat_dirs + ["文件传输助手"]
        print("\n将发送到 %d 个聊天" % len(chat_list))
        
        if sys.version_info[0] >= 3:
            confirm = input("\n确认发送？(y/n): ").strip().lower()
        else:
            confirm = raw_input("\n确认发送？(y/n): ").strip().lower()
        if confirm != 'y':
            print("已取消")
            if sys.version_info[0] >= 3:
                input("\n按回车键退出...")
            else:
                raw_input("\n按回车键退出...")
            return
    
    elif send_choice == "2":
        print("\n聊天列表:")
        for i, chat in enumerate(chat_dirs, 1):
            print("  [%2d] %s" % (i, chat))
        
        print("\n请输入要发送的聊天序号（用逗号分隔，如：1,3,5）:")
        if sys.version_info[0] >= 3:
            indices = input("> ").strip()
        else:
            indices = raw_input("> ").strip()
        
        try:
            idx_list = [int(x.strip()) - 1 for x in indices.split(",")]
            chat_list = [chat_dirs[i] for i in idx_list if 0 <= i < len(chat_dirs)]
            chat_list.append("文件传输助手")
        except:
            print("输入无效")
            if sys.version_info[0] >= 3:
                input("\n按回车键退出...")
            else:
                raw_input("\n按回车键退出...")
            return
    
    else:
        chat_list = ["文件传输助手"]
    
    # 执行发送
    print()
    sender.send_multiple(file_path, user, chat_list)
    
    if sys.version_info[0] >= 3:
        input("\n按回车键退出...")
    else:
        raw_input("\n按回车键退出...")


if __name__ == "__main__":
    main()
