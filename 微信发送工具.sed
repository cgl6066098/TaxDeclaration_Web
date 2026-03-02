[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=0
HideExtractAnimation=1
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=%InstallPrompt%
DisplayLicense=%DisplayLicense%
FinishMessage=%FinishMessage%
TargetName=%TargetName%
FriendlyName=%FriendlyName%
AppLaunched=%AppLaunched%
PostInstallCmd=%PostInstallCmd%
AdminQuietInstCmd=
UserQuietInstCmd=
SourceFiles=SourceFiles

[Strings]
InstallPrompt=
DisplayLicense=
FinishMessage=
TargetName=%USERPROFILE%\Desktop\微信发送工具_Win7.exe
FriendlyName=微信发送工具 Win7 版
AppLaunched=cscript.exe //nologo wechat_send_win7.vbs
PostInstallCmd=
[SourceFiles]
SourceFiles0=%USERPROFILE%\Desktop\AI_Project\纳税申报\

[SourceFiles0]
%USERPROFILE%\Desktop\AI_Project\纳税申报\wechat_send_win7.vbs=
