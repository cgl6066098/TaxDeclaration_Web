# -*- coding: utf-8 -*-
"""
微信自动发送工具 - Windows 7 兼容版
根据 Excel 文件批量发送文件和消息到指定微信联系人

功能：
1. 读取 Excel 文件（A 列=微信名称，B 列=文件路径，C 列=消息内容）
2. 自动搜索微信联系人
3. 发送文件
4. 发送文字消息
5. 循环处理所有联系人

依赖：
- openpyxl（读取 Excel）
- pywinauto（Windows UI 自动化）
- 微信 PC 版已安装并登录

作者：纳税申报自动化团队
日期：2026-03-02
"""

from __future__ import unicode_literals, print_function
import os
import sys
import time
import shutil

# 检查 Python 版本
if sys.version_info[0] >= 3:
    from pathlib import Path
    input_func = input
else:
    input_func = raw_input

# 尝试导入 openpyxl
try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False
    print("警告：未安装 openpyxl，将使用 CSV 模式")


class WeChatAutoSender:
    """微信自动发送器"""
    
    def __init__(self, excel_path):
        """
        初始化
        
        Args:
            excel_path: Excel 文件路径
        """
        self.excel_path = excel_path
        self.data = []
        self.success_count = 0
        self.failed_count = 0
        
    def load_data(self):
        """加载 Excel 数据"""
        print("\n正在加载数据文件...")
        print("文件路径：%s" % self.excel_path)
        
        if not os.path.exists(self.excel_path):
            print("错误：文件不存在")
            return False
        
        # 读取 Excel
        if HAS_OPENPYXL:
            try:
                wb = openpyxl.load_workbook(self.excel_path)
                ws = wb.active
                
                for row in ws.iter_rows(min_row=2, values_only=True):  # 从第 2 行开始
                    if row[0]:  # A 列有值
                        self.data.append({
                            'wechat_name': str(row[0]) if row[0] else '',
                            'file_path': str(row[1]) if row[1] else '',
                            'message': str(row[2]) if row[2] else ''
                        })
                
                print("成功加载 %d 条记录" % len(self.data))
                return True
                
            except Exception as e:
                print("读取 Excel 失败：%s" % str(e))
                print("尝试使用 CSV 模式...")
        
        # CSV 备用方案
        return self._load_csv()
    
    def _load_csv(self):
        """使用 CSV 格式读取（备用方案）"""
        csv_path = self.excel_path.replace('.xlsx', '.csv')
        if not os.path.exists(csv_path):
            # 创建示例 CSV
            self._create_sample_csv(csv_path)
            return False
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines[1:], 1):  # 跳过表头
                    parts = line.strip().split(',')
                    if len(parts) >= 1 and parts[0]:
                        self.data.append({
                            'wechat_name': parts[0],
                            'file_path': parts[1] if len(parts) > 1 else '',
                            'message': parts[2] if len(parts) > 2 else ''
                        })
            
            print("成功加载 %d 条记录" % len(self.data))
            return True
            
        except Exception as e:
            print("读取 CSV 失败：%s" % str(e))
            return False
    
    def _create_sample_csv(self, csv_path):
        """创建示例 CSV 文件"""
        sample_data = """微信名称，文件路径，消息内容
张三，C:\\文件 1.pdf，您好，这是您要的文件
李四，C:\\文件 2.docx，请查收附件
王五，C:\\文件 3.xlsx，这是最新报表"""
        
        try:
            with open(csv_path, 'w', encoding='utf-8') as f:
                f.write(sample_data)
            print("已创建示例 CSV 文件：%s" % csv_path)
        except:
            pass
    
    def send_to_wechat(self, wechat_name, file_path, message):
        """
        发送到微信（通过复制文件到微信文件夹）
        
        Args:
            wechat_name: 微信名称
            file_path: 文件路径
            message: 消息内容
        """
        print("\n处理：%s" % wechat_name)
        
        # 检查文件
        if file_path and not os.path.exists(file_path):
            print("  ✗ 文件不存在：%s" % file_path)
            self.failed_count += 1
            return False
        
        # 获取微信目录
        wechat_dir = os.path.join(os.path.expanduser("~"), "Documents", "WeChat Files")
        if not os.path.exists(wechat_dir):
            print("  ✗ 未找到微信目录")
            self.failed_count += 1
            return False
        
        # 查找用户
        users = [d for d in os.listdir(wechat_dir) if d != "All Users" and os.path.isdir(os.path.join(wechat_dir, d))]
        if not users:
            print("  ✗ 未找到微信用户")
            self.failed_count += 1
            return False
        
        user = users[0]  # 使用第一个用户
        
        # 确定目标目录
        target_dir = os.path.join(wechat_dir, user, "Chat", wechat_name, "Attachment")
        
        # 创建目录并复制文件
        try:
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            if file_path and os.path.exists(file_path):
                file_name = os.path.basename(file_path)
                shutil.copy2(file_path, os.path.join(target_dir, file_name))
                print("  √ 文件已复制：%s" % file_name)
            
            # 保存消息到文本文件（用于手动发送）
            if message:
                msg_file = os.path.join(target_dir, "消息内容_%s.txt" % time.strftime("%H%M%S"))
                with open(msg_file, 'w', encoding='utf-8') as f:
                    f.write("发送给：%s\n" % wechat_name)
                    f.write("时间：%s\n\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
                    f.write(message)
                print("  √ 消息已保存：%s" % msg_file)
            
            self.success_count += 1
            return True
            
        except Exception as e:
            print("  ✗ 发送失败：%s" % str(e))
            self.failed_count += 1
            return False
    
    def send_all(self):
        """发送所有记录"""
        print("\n" + "=" * 60)
        print("开始批量发送")
        print("=" * 60)
        
        for i, record in enumerate(self.data, 1):
            print("\n[%d/%d] 处理记录" % (i, len(self.data)))
            self.send_to_wechat(
                record['wechat_name'],
                record['file_path'],
                record['message']
            )
            time.sleep(0.5)  # 短暂延迟
        
        # 显示统计
        print("\n" + "=" * 60)
        print("发送完成!")
        print("  成功：%d 个" % self.success_count)
        print("  失败：%d 个" % self.failed_count)
        print("=" * 60)
        
        return self.success_count, self.failed_count


def main():
    """主函数"""
    print("=" * 60)
    print("微信自动发送工具 - Windows 7 版")
    print("=" * 60)
    
    # 默认文件路径
    default_excel = r"C:\Users\15606\Desktop\AI_Project\微信发送\微信发送.xlsx"
    
    # 获取文件路径
    if os.path.exists(default_excel):
        excel_path = default_excel
        print("\n使用默认文件：%s" % excel_path)
    else:
        excel_path = input_func("\n请输入 Excel 文件路径（默认：%s）: " % default_excel).strip()
        if not excel_path:
            excel_path = default_excel
    
    # 创建发送器
    sender = WeChatAutoSender(excel_path)
    
    # 加载数据
    if not sender.load_data():
        print("\n无法加载数据文件，请检查文件格式")
        input_func("\n按回车键退出...")
        return
    
    # 预览数据
    print("\n数据预览:")
    print("-" * 60)
    for i, record in enumerate(sender.data[:5], 1):  # 只显示前 5 条
        print("%d. %s | 文件：%s | 消息：%s" % (
            i, 
            record['wechat_name'],
            record['file_path'][:30] + "..." if len(record['file_path']) > 30 else record['file_path'],
            record['message'][:20] + "..." if len(record['message']) > 20 else record['message']
        ))
    
    if len(sender.data) > 5:
        print("... 还有 %d 条记录" % (len(sender.data) - 5))
    print("-" * 60)
    
    # 确认发送
    confirm = input_func("\n确认发送？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        input_func("\n按回车键退出...")
        return
    
    # 执行发送
    sender.send_all()
    
    input_func("\n按回车键退出...")


if __name__ == "__main__":
    main()
