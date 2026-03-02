' 纳税申报 - 微信发送工具 (VBScript 版)
' 完全兼容 Windows 7，无需 Python
' 双击即可运行

Option Explicit

Dim fso, shell, userProfiles, wechatDir, users
Dim i, userInput, fileChoice, chatChoice, selectedFile, targetDir

' 创建对象
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

' 主程序
Main

Sub Main()
    Dim title, message
    title = "纳税申报 - 微信发送工具 (Win7 版)"
    
    ' 选择文件
    fileChoice = shell.Popup("请选择要发送的文件:" & vbCrLf & vbCrLf & _
        "1. 登录模块 (登录.py)" & vbCrLf & _
        "2. 浏览器管理模块 (browser.py)" & vbCrLf & _
        "3. 使用说明文档 (使用说明.md)" & vbCrLf & _
        "4. 自定义文件", _
        0, title, 1 + 32)
    
    ' 处理选择
    Select Case fileChoice
        Case 1 ' 登录模块
            selectedFile = GetCurrentDir() & "\纳税申报模块\执行模块\登录.py"
        Case 2 ' 浏览器管理模块
            selectedFile = GetCurrentDir() & "\纳税申报模块\执行模块\browser.py"
        Case 3 ' 使用说明
            selectedFile = GetCurrentDir() & "\纳税申报模块\执行模块\使用说明.md"
        Case 4 ' 自定义文件
            selectedFile = shell.InputBox("请输入文件完整路径:", title, "")
        Case Else
            shell.Popup "已取消", 2, title, 48
            WScript.Quit
    End Select
    
    ' 检查文件是否存在
    If Not fso.FileExists(selectedFile) Then
        shell.Popup "文件不存在:" & vbCrLf & selectedFile, 5, title, 16
        WScript.Quit
    End If
    
    ' 选择聊天对象
    chatChoice = shell.Popup("发送到:" & vbCrLf & vbCrLf & _
        "1. 文件传输助手" & vbCrLf & _
        "2. 特定聊天", _
        0, title, 1 + 32)
    
    ' 获取微信目录
    wechatDir = GetWeChatDir()
    If wechatDir = "" Then
        shell.Popup "未找到微信文件目录!" & vbCrLf & vbCrLf & _
            "请确认:" & vbCrLf & _
            "1. 微信已安装" & vbCrLf & _
            "2. 微信已登录" & vbCrLf & _
            "3. 微信文件目录在 Documents\WeChat Files\", _
            10, title, 16
        WScript.Quit
    End If
    
    ' 复制文件
    If CopyToWeChat(selectedFile, wechatDir, chatChoice) Then
        shell.Popup "✓ 文件已复制到微信文件夹!" & vbCrLf & vbCrLf & _
            "请在微信中手动发送该文件", 5, title, 64
    Else
        shell.Popup "× 复制失败!" & vbCrLf & _
            "请确保微信正在运行", 5, title, 16
    End If
End Sub

Function GetCurrentDir()
    GetCurrentDir = fso.GetParentFolderName(WScript.ScriptFullName)
End Function

Function GetWeChatDir()
    Dim docPath, wcPath
    docPath = shell.SpecialFolders("MyDocuments")
    wcPath = docPath & "\WeChat Files\"
    
    If fso.FolderExists(wcPath) Then
        GetWeChatDir = wcPath
    Else
        GetWeChatDir = ""
    End If
End Function

Function CopyToWeChat(filePath, wechatDir, chatType)
    Dim users, user, targetDir, fileName, result
    On Error Resume Next
    
    ' 获取微信用户列表
    users = GetUserList(wechatDir)
    If UBound(users) < 0 Then
        CopyToWeChat = False
        Exit Function
    End If
    
    ' 使用第一个用户（或选择）
    user = users(0)
    If UBound(users) > 0 Then
        user = shell.InputBox("找到多个微信账号，请输入要使用的账号:" & vbCrLf & vbCrLf & _
            Join(users, vbCrLf), "选择微信账号", user)
    End If
    
    ' 确定目标目录
    If chatType = 1 Then
        ' 文件传输助手
        targetDir = wechatDir & user & "\Msg\Attachment\"
    Else
        ' 特定聊天 - 需要输入聊天名称
        Dim chatName
        chatName = shell.InputBox("请输入聊天对象名称:", "特定聊天", "")
        If chatName = "" Then
            CopyToWeChat = False
            Exit Function
        End If
        targetDir = wechatDir & user & "\Chat\" & chatName & "\Attachment\"
    End If
    
    ' 创建目录（如果不存在）
    If Not fso.FolderExists(targetDir) Then
        fso.CreateFolder(targetDir)
    End If
    
    ' 复制文件
    fileName = fso.GetFileName(filePath)
    fso.CopyFile filePath, targetDir & fileName, True
    
    If Err.Number = 0 Then
        CopyToWeChat = True
    Else
        CopyToWeChat = False
    End If
    
    On Error GoTo 0
End Function

Function GetUserList(wechatDir)
    Dim f, users(), i
    i = 0
    
    For Each f In fso.GetFolder(wechatDir).SubFolders
        If f.Name <> "All Users" Then
            ReDim Preserve users(i)
            users(i) = f.Name
            i = i + 1
        End If
    Next
    
    GetUserList = users
End Function
