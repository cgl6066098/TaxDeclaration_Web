@echo off
chcp 65001 >nul
title 登录模块

echo ============================================================
echo 登录模块
echo ============================================================
echo.
echo 请选择登录目标:
echo.
echo   1. 知乎
echo   2. 电子税务局
echo   3. 交互式登录（知乎）
echo   4. 交互式登录（电子税务局）
echo.

set /p choice="请输入选项 (1-4): "

if "%choice%"=="1" goto zhihu
if "%choice%"=="2" goto tax
if "%choice%"=="3" goto zhihu_interactive
if "%choice%"=="4" goto tax_interactive

echo 无效的选项
pause
exit /b

:zhihu
echo.
echo 正在登录知乎...
C:\Users\15606\miniconda3\envs\tax_python\python.exe "%~dp0纳税申报模块\login.py"
pause
exit /b

:tax
echo.
echo 正在登录电子税务局...
C:\Users\15606\miniconda3\envs\tax_python\python.exe "%~dp0纳税申报模块\login.py"
pause
exit /b

:zhihu_interactive
echo.
echo 正在启动交互式登录...
C:\Users\15606\miniconda3\envs\tax_python\python.exe "%~dp0纳税申报模块\login.py"
pause
exit /b

:tax_interactive
echo.
echo 正在启动交互式登录...
C:\Users\15606\miniconda3\envs\tax_python\python.exe "%~dp0纳税申报模块\login.py"
pause
exit /b
