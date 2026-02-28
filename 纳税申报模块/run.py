"""
纳税申报模块 - 主运行脚本
演示完整的纳税申报流程
"""
import os
import sys

# 添加模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "纳税申报模块"))

from tax_filing import TaxFiling, create_tax_filing


def main():
    """主函数"""
    print("=" * 60)
    print("纳税申报自动化系统")
    print("=" * 60)
    print()
    
    # 创建纳税申报实例
    tax = create_tax_filing()
    
    try:
        # 启动浏览器
        tax.start(headless=False)
        
        # 运行演示流程（知乎登录示例）
        tax.run_demo()
        
        print("\n" + "=" * 60)
        print("演示完成！")
        print("=" * 60)
        print("\n按 Ctrl+C 关闭浏览器...")
        
        # 保持浏览器打开
        while True:
            import time
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"\n发生错误：{e}")
    finally:
        tax.close()


if __name__ == "__main__":
    main()
