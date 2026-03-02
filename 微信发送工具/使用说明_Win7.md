# 微信发送工具 - Windows 7 版本

## 📁 桌面文件说明

桌面上有两个文件：

### 1. `微信发送工具_Win7.vbs` ✅ **推荐**
- **直接双击运行**
- 100% 兼容 Windows 7
- 无需安装任何软件
- 无需 Python

### 2. `微信发送工具_Win7.bat`
- 批处理启动器
- 双击也可运行
- 效果与 .vbs 相同

## ⚠️ 关于 EXE 版本

**问题**: 之前打包的 EXE 版本需要 `api-ms-win-core-path-l1-1-0.dll`，这是 Windows 10 的 DLL 文件。

**原因**: 
- Python 3.12 打包的 EXE 需要 Windows 10+ 的 DLL
- Python 3.8 是最后一个支持 Windows 7 的版本，但当前环境无法安装

**解决方案**: 
- ✅ **使用 VBScript 版本**（`.vbs` 或 `.bat` 文件）
- VBScript 是 Windows 内置脚本引擎，所有 Windows 版本都支持

## ✅ 使用方法（Windows 7）

### 方法 1：双击 VBS 文件（推荐）
```
双击：微信发送工具_Win7.vbs
```

### 方法 2：双击 BAT 文件
```
双击：微信发送工具_Win7.bat
```

两种方法效果相同，都会启动微信发送工具。

## 📋 功能

1. 选择要发送的文件
   - 登录模块
   - 浏览器管理模块
   - 使用说明文档
   - 自定义文件

2. 选择发送对象
   - 文件传输助手
   - 特定聊天

3. 自动复制文件到微信文件夹

## 🔧 故障排除

### 如果双击 .vbs 没有反应
**解决**: 右键 → 打开方式 → Microsoft Windows Based Script Host

### 如果提示找不到微信目录
**解决**: 
1. 确认微信已安装并登录
2. 检查目录：`C:\Users\你的用户名\Documents\WeChat Files\`

---

**版本**: 1.0.0 (VBScript)
**兼容性**: Windows 7/8/10/11 (100%)
