@echo off
chcp 65001 >nul
title 测试点击账务中心

echo ============================================================
echo 测试点击账务中心
echo ============================================================
echo.
echo 用法:
echo   双击运行 - 前台保持打开（默认）
echo   添加参数 --headless  - 后台无头模式
echo   添加参数 --no-keep-alive - 完成后关闭浏览器
echo.
echo ============================================================
echo.

C:\Users\15606\miniconda3\envs\tax_python\python.exe "%~dp0test_click.py" %*

pause
