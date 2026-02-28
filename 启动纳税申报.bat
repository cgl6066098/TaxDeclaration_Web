@echo off
chcp 65001 >nul
title 纳税申报自动化系统

echo ============================================================
echo 纳税申报自动化系统
echo ============================================================
echo.
echo 模块目录：%~dp0纳税申报模块
echo Python 环境：C:\Users\15606\miniconda3\envs\tax_python\python.exe
echo.
echo 正在启动...
echo.

C:\Users\15606\miniconda3\envs\tax_python\python.exe "%~dp0纳税申报模块\run.py"

pause
