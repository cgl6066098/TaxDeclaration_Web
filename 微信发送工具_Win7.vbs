' 微信发送工具 - Windows 7 完全兼容版
' 纯 VBScript 编写，无需 Python，双击即可运行
' 支持单发、群发功能

Option Explicit

Dim fso, shell, wechatDir, users, user
Dim fileChoice, chatChoice, sendMode
Dim selectedFile, targetDir, fileName
Dim i, result, chatList, chatName

' 创建对象
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

' 主程序
Main

Sub Main()
    Dim title
    title = "微信发送工具 - Windows 7 版"
    
    ' 1. 获取微信目录
    wechatDir = GetWeChatDir()
    If wechatDir = "" Then
        result = shell.Popup("未找到微信文件目录！" & vbCrLf & vbCrLf & _
            "可能原因：" & vbCrLf & _
            "1. 微信未安装" & vbCrLf & _
            "2. 微信未登录" & vbCrLf & _
            "3. 微信版本过旧" & vbCrLf & vbCrLf & _
            "是否查看帮助？", _
            10, title, 16 + 4)
        
        If result = 6 Then
            shell.Run "notepad.exe"
        End If
        WScript.Quit
    End If
    
    ' 2. 选择微信用户
    users = GetUserList(wechatDir)
    If UBound(users) < 0 Then
        shell.Popup "未找到微信用户目录", 5, title, 16
        WScript.Quit
    End If
    
    user = SelectUser(users, title)
    If user = "" Then
        WScript.Quit
    End If
    
    ' 3. 选择文件
    fileChoice = shell.Popup("请选择要发送的文件:" & vbCrLf & vbCrLf & _
        "1. 登录模块 (登录.py)" & vbCrLf & _
        "2. 浏览器管理模块 (browser.py)" & vbCrLf & _
        "3. 使用说明文档 (使用说明.md)" & vbCrLf & _
        "4. 自定义文件", _
        0, title, 1 + 32 + 256) ' 1=Yes/No/Cancel, 32=Info, 256=Default 1
    
    selectedFile = GetFilePath(fileChoice, title)
    If selectedFile = "" Then
        shell.Popup "已取消", 2, title, 48
        WScript.Quit
    End If
    
    ' 检查文件
    If Not fso.FileExists(selectedFile) Then
        shell.Popup "文件不存在：" & vbCrLf & selectedFile, 5, title, 16
        WScript.Quit
    End If
    
    ' 4. 选择发送模式
    sendMode = shell.Popup("请选择发送模式:" & vbCrLf & vbCrLf & _
        "1. 单发 - 发送到一个聊天" & vbCrLf & _
        "2. 群发 - 发送到多个聊天", _
        0, title, 1 + 32)
    
    If sendMode = 1 Then
        ' 单发模式
        SendSingle user, selectedFile, title
    ElseIf sendMode = 2 Then
        ' 群发模式
        SendMultiple user, selectedFile, title
    Else
        shell.Popup "已取消", 2, title, 48
        WScript.Quit
    End If
End Sub

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

Function GetUserList(wcDir)
    Dim f, users(), i
    i = 0
    
    On Error Resume Next
    For Each f In wcDir.SubFolders
        If f.Name <> "All Users" Then
            ReDim Preserve users(i)
            users(i) = f.Name
            i = i + 1
        End If
    Next
    On Error GoTo 0
    
    GetUserList = users
End Function

Function SelectUser(users, title)
    Dim i, userList, selected
    
    If UBound(users) = 0 Then
        SelectUser = users(0)
        Exit Function
    End If
    
    userList = "找到 " & (UBound(users)+1) & " 个微信账号：" & vbCrLf & vbCrLf
    For i = 0 To UBound(users)
        userList = userList & "  [" & (i+1) & "] " & users(i) & vbCrLf
    Next
    
    selected = shell.InputBox(userList & vbCrLf & "请输入序号（默认 1）:", title & " - 选择账号", "1")
    
    If selected = "" Then
        SelectUser = ""
        Exit Function
    End If
    
    If IsNumeric(selected) Then
        i = CInt(selected) - 1
        If i >= 0 And i <= UBound(users) Then
            SelectUser = users(i)
        Else
            SelectUser = users(0)
        End If
    Else
        SelectUser = users(0)
    End If
End Function

Function GetFilePath(choice, title)
    Dim scriptDir, filePath
    
    scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
    
    Select Case choice
        Case 1 ' 登录模块
            filePath = scriptDir & "\纳税申报模块\执行模块\登录.py"
        Case 2 ' 浏览器管理模块
            filePath = scriptDir & "\纳税申报模块\执行模块\browser.py"
        Case 3 ' 使用说明
            filePath = scriptDir & "\纳税申报模块\执行模块\使用说明.md"
        Case 4 ' 自定义文件
            filePath = shell.InputBox("请输入文件完整路径:", title, scriptDir)
        Case Else
            filePath = ""
    End Select
    
    GetFilePath = filePath
End Function

Sub SendSingle(user, filePath, title)
    Dim chatList, chats, i, chatCount, selected
    
    ' 获取聊天列表
    chats = GetChatList(user)
    chatCount = UBound(chats) + 1
    
    If chatCount = 0 Then
        shell.Popup "未找到聊天目录", 5, title, 16
        Exit Sub
    End If
    
    ' 显示聊天列表
    chatList = "找到 " & chatCount & " 个聊天：" & vbCrLf & vbCrLf
    For i = 0 To UBound(chats)
        chatList = chatList & "  [" & (i+1) & "] " & chats(i) & vbCrLf
    Next
    
    ' 选择聊天
    selected = shell.InputBox(chatList & vbCrLf & _
        "输入序号选择聊天，或输入名称：" & vbCrLf & vbCrLf & _
        "输入 0 发送到文件传输助手", _
        title & " - 选择聊天", "0")
    
    If selected = "" Then
        Exit Sub
    End If
    
    If selected = "0" Then
        CopyToChat filePath, user, "文件传输助手"
    ElseIf IsNumeric(selected) Then
        i = CInt(selected) - 1
        If i >= 0 And i <= UBound(chats) Then
            CopyToChat filePath, user, chats(i)
        Else
            shell.Popup "无效的序号", 3, title, 16
        End If
    Else
        CopyToChat filePath, user, selected
    End If
End Sub

Sub SendMultiple(user, filePath, title)
    Dim chats, i, chatCount, selected, chatList
    Dim successCount, failCount
    
    ' 获取聊天列表
    chats = GetChatList(user)
    chatCount = UBound(chats) + 1
    
    If chatCount = 0 Then
        shell.Popup "未找到聊天目录", 5, title, 16
        Exit Sub
    End If
    
    ' 显示聊天列表
    chatList = "聊天列表：" & vbCrLf & vbCrLf
    For i = 0 To UBound(chats)
        chatList = chatList & "  [" & (i+1) & "] " & chats(i) & vbCrLf
    Next
    
    ' 选择要发送的聊天
    selected = shell.InputBox(chatList & vbCrLf & _
        "请输入要发送的聊天序号（用逗号分隔）" & vbCrLf & _
        "例如：1,3,5 表示发送给第 1、3、5 个聊天" & vbCrLf & vbCrLf & _
        "输入 all 发送给所有聊天", _
        title & " - 群发设置", "")
    
    If selected = "" Then
        Exit Sub
    End If
    
    successCount = 0
    failCount = 0
    
    If LCase(selected) = "all" Then
        ' 发送所有
        For i = 0 To UBound(chats)
            If CopyToChat(filePath, user, chats(i)) Then
                successCount = successCount + 1
            Else
                failCount = failCount + 1
            End If
        Next
    Else
        ' 发送选择的
        Dim indices, idx
        indices = Split(selected, ",")
        
        For Each idx In indices
            idx = Trim(idx)
            If IsNumeric(idx) Then
                i = CInt(idx) - 1
                If i >= 0 And i <= UBound(chats) Then
                    If CopyToChat(filePath, user, chats(i)) Then
                        successCount = successCount + 1
                    Else
                        failCount = failCount + 1
                    End If
                End If
            End If
        Next
    End If
    
    ' 显示结果
    shell.Popup "群发完成！" & vbCrLf & vbCrLf & _
        "成功：" & successCount & " 个" & vbCrLf & _
        "失败：" & failCount & " 个", _
        10, title, 64
End Sub

Function GetChatList(user)
    Dim base, chatDir, chats(), i, f
    base = wechatDir & user
    
    i = 0
    On Error Resume Next
    
    ' 查找 Chat 目录
    chatDir = base & "\Chat"
    If fso.FolderExists(chatDir) Then
        For Each f In chatDir.SubFolders
            ReDim Preserve chats(i)
            chats(i) = f.Name
            i = i + 1
        Next
    End If
    
    On Error GoTo 0
    GetChatList = chats
End Function

Function CopyToChat(filePath, user, chatName)
    Dim targetDir, fileName, result
    
    On Error Resume Next
    
    ' 确定目标目录
    If chatName = "文件传输助手" Then
        targetDir = wechatDir & user & "\Msg\Attachment\"
    Else
        targetDir = wechatDir & user & "\Chat\" & chatName & "\Attachment\"
    End If
    
    ' 创建目录
    If Not fso.FolderExists(targetDir) Then
        fso.CreateFolder(targetDir)
    End If
    
    ' 复制文件
    fileName = fso.GetFileName(filePath)
    fso.CopyFile filePath, targetDir & fileName, True
    
    If Err.Number = 0 Then
        CopyToChat = True
    Else
        CopyToChat = False
    End If
    
    On Error GoTo 0
End Function
