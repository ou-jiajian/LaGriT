#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成LaGriT Windows启动脚本
"""

import os
from pathlib import Path

def create_startup_scripts():
    """创建LaGriT启动脚本"""
    current_dir = Path.cwd()
    build_dir = current_dir / "build"
    
    print("🔧 创建LaGriT启动脚本")
    print("=" * 40)
    print(f"项目目录: {current_dir}")
    print(f"构建目录: {build_dir}")
    
    # 创建 start_lagrit.bat
    start_script = current_dir / "start_lagrit.bat"
    start_content = f"""@echo off
REM LaGriT 启动脚本
chcp 65001 >nul 2>&1
echo 启动 LaGriT...

set "PATH=C:\\msys64\\mingw64\\bin;%PATH%"
set "LAGRIT_DIR={current_dir}"
set "BUILD_DIR={build_dir}"

if exist "%BUILD_DIR%\\lagrit.exe" (
    echo ✓ 找到 lagrit.exe
    echo 当前目录: %cd%
    echo 启动 LaGriT...
    "%BUILD_DIR%\\lagrit.exe"
) else (
    echo ❌ 未找到 lagrit.exe
    echo 请检查构建目录: %BUILD_DIR%
    echo 如果需要重新构建，请运行: python rebuild_lagrit.py
    pause
)
"""
    
    with open(start_script, 'w', encoding='ascii', errors='ignore') as f:
        f.write(start_content)
    print(f"✓ 创建了 {start_script}")
    
    # 创建 test_lagrit.bat
    test_script = current_dir / "test_lagrit.bat"
    test_content = f"""@echo off
REM LaGriT 测试脚本
chcp 65001 >nul 2>&1
echo 测试 LaGriT...

set "PATH=C:\\msys64\\mingw64\\bin;%PATH%"
set "BUILD_DIR={build_dir}"

if exist "%BUILD_DIR%\\lagrit.exe" (
    echo ✓ 找到 lagrit.exe
    echo 运行快速测试...
    echo finish | "%BUILD_DIR%\\lagrit.exe"
    echo.
    echo 测试完成！
) else (
    echo ❌ 未找到 lagrit.exe
    echo 请先运行: python rebuild_lagrit.py
)
pause
"""
    
    with open(test_script, 'w', encoding='ascii', errors='ignore') as f:
        f.write(test_content)
    print(f"✓ 创建了 {test_script}")
    
    # 创建 diagnose.bat
    diagnose_script = current_dir / "diagnose.bat"
    diagnose_content = f"""@echo off
REM LaGriT 诊断脚本
chcp 65001 >nul 2>&1
echo LaGriT 诊断信息
echo ==================

echo 项目目录: {current_dir}
echo 构建目录: {build_dir}
echo.

echo 检查文件存在性:
if exist "{build_dir}\\lagrit.exe" (
    echo ✓ lagrit.exe 存在
    dir "{build_dir}\\lagrit.exe"
) else (
    echo ❌ lagrit.exe 不存在
)
echo.

echo 检查MSYS2:
if exist "C:\\msys64\\mingw64\\bin\\gcc.exe" (
    echo ✓ MSYS2/MinGW64 存在
) else (
    echo ❌ MSYS2/MinGW64 不存在
)
echo.

echo 当前PATH:
echo %PATH%
echo.

echo 可用命令:
where python 2>nul
where conda 2>nul
where gcc 2>nul
echo.

pause
"""
    
    with open(diagnose_script, 'w', encoding='ascii', errors='ignore') as f:
        f.write(diagnose_content)
    print(f"✓ 创建了 {diagnose_script}")
    
    print("\n🎉 启动脚本创建完成！")
    print("\n使用方法:")
    print("- start_lagrit.bat  : 启动LaGriT")
    print("- test_lagrit.bat   : 快速测试LaGriT")
    print("- diagnose.bat      : 诊断系统状态")
    print("- python rebuild_lagrit.py : 重新编译")

if __name__ == "__main__":
    create_startup_scripts() 