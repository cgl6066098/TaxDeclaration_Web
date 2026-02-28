@echo off
chcp 65001 >nul
title 知乎自动化 - 持久化浏览器
echo ============================================================
echo 知乎自动化 - 持久化浏览器
echo ============================================================
echo.
echo 用户数据目录：%~dp0browser_profile
echo.
echo 正在启动浏览器...
echo.

C:\Users\15606\miniconda3\envs\tax_python\python.exe "%~dp0browser.py"

pause
