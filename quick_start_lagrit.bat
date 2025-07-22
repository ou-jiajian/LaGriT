@echo off
echo LaGriT 快速启动脚本
echo ====================

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
echo 脚本目录: %SCRIPT_DIR%

REM 检查build目录
set BUILD_DIR=%SCRIPT_DIR%build
echo 构建目录: %BUILD_DIR%

REM 检查lagrit.exe是否存在
if exist "%BUILD_DIR%\lagrit.exe" (
    echo ✓ 找到 lagrit.exe
    echo 启动 LaGriT...
    echo.
    
    REM 设置环境变量
    set "PATH=%BUILD_DIR%;%PATH%"
    
    REM 启动LaGriT
    "%BUILD_DIR%\lagrit.exe"
) else (
    echo ❌ 未找到 lagrit.exe
    echo.
    echo 请检查以下位置:
    echo   %BUILD_DIR%\lagrit.exe
    echo.
    echo 如果文件不存在，请运行安装脚本:
    echo   python install_lagrit_windows.py
    echo.
    pause
) 