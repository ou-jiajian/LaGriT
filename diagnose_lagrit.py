#!/usr/bin/env python3
"""
LaGriT 安装诊断脚本
检查LaGriT安装状态和可执行文件位置
"""

import os
import sys
from pathlib import Path
import subprocess

def check_lagrit_installation():
    """检查LaGriT安装状态"""
    print("🔍 LaGriT 安装诊断")
    print("=" * 50)
    
    # 获取当前目录
    current_dir = Path.cwd()
    print(f"📁 当前目录: {current_dir}")
    
    # 检查build目录
    build_dir = current_dir / "build"
    print(f"\n🔨 检查构建目录: {build_dir}")
    
    if build_dir.exists():
        print("✓ build目录存在")
        
        # 查找lagrit.exe
        lagrit_exe = build_dir / "lagrit.exe"
        if lagrit_exe.exists():
            print(f"✓ 找到 lagrit.exe: {lagrit_exe}")
            print(f"  文件大小: {lagrit_exe.stat().st_size / 1024 / 1024:.1f} MB")
            
            # 检查文件权限
            try:
                # 尝试运行lagrit.exe
                result = subprocess.run([str(lagrit_exe), "--help"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print("✓ lagrit.exe 可以正常执行")
                else:
                    print("⚠️  lagrit.exe 执行时返回非零状态码")
                    print(f"   错误输出: {result.stderr}")
            except subprocess.TimeoutExpired:
                print("⚠️  lagrit.exe 执行超时")
            except Exception as e:
                print(f"❌ lagrit.exe 执行失败: {e}")
        else:
            print("❌ 未找到 lagrit.exe")
            
            # 列出build目录中的文件
            print("📋 build目录中的文件:")
            for file in build_dir.iterdir():
                if file.is_file():
                    print(f"   {file.name}")
    else:
        print("❌ build目录不存在")
    
    # 检查激活脚本
    print(f"\n📝 检查激活脚本")
    activate_script = current_dir / "activate_lagrit.bat"
    if activate_script.exists():
        print(f"✓ 找到激活脚本: {activate_script}")
        
        # 读取激活脚本内容
        with open(activate_script, 'r', encoding='utf-8') as f:
            content = f.read()
            if "lagrit" in content:
                print("✓ 激活脚本包含lagrit相关配置")
            else:
                print("⚠️  激活脚本中未找到lagrit配置")
    else:
        print("❌ 未找到激活脚本")
    
    # 检查环境变量脚本
    setup_env_script = current_dir / "setup_env.bat"
    if setup_env_script.exists():
        print(f"✓ 找到环境变量脚本: {setup_env_script}")
    else:
        print("❌ 未找到环境变量脚本")
    
    # 检查PATH环境变量
    print(f"\n🔍 检查PATH环境变量")
    path_dirs = os.environ.get('PATH', '').split(';')
    lagrit_in_path = False
    
    for path_dir in path_dirs:
        if path_dir.strip():
            lagrit_exe_in_path = Path(path_dir.strip()) / "lagrit.exe"
            if lagrit_exe_in_path.exists():
                print(f"✓ 在PATH中找到lagrit.exe: {lagrit_exe_in_path}")
                lagrit_in_path = True
                break
    
    if not lagrit_in_path:
        print("❌ lagrit.exe 不在PATH中")
    
    # 检查conda环境
    print(f"\n🐍 检查conda环境")
    try:
        result = subprocess.run(["conda", "env", "list"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            if "lagrit-env" in result.stdout:
                print("✓ 找到 lagrit-env conda环境")
            else:
                print("❌ 未找到 lagrit-env conda环境")
        else:
            print("⚠️  无法检查conda环境")
    except Exception as e:
        print(f"❌ 检查conda环境失败: {e}")
    
    # 提供解决方案
    print(f"\n💡 解决方案")
    print("=" * 50)
    
    if build_dir.exists() and (build_dir / "lagrit.exe").exists():
        print("✅ LaGriT已正确构建")
        print("\n🔧 解决方法:")
        print("1. 使用完整路径运行:")
        print(f"   {build_dir / 'lagrit.exe'}")
        print("\n2. 或者运行激活脚本:")
        print("   activate_lagrit.bat")
        print("\n3. 或者手动添加到PATH:")
        print(f"   set PATH={build_dir};%PATH%")
        print("   然后运行: lagrit")
    else:
        print("❌ LaGriT未正确构建")
        print("\n🔧 解决方法:")
        print("1. 重新运行安装脚本:")
        print("   python install_lagrit_windows.py")
        print("\n2. 或者手动构建:")
        print("   mkdir build")
        print("   cd build")
        print("   cmake ..")
        print("   make")
    
    # 创建快速修复脚本
    create_quick_fix_script(current_dir, build_dir)

def create_quick_fix_script(current_dir, build_dir):
    """创建快速修复脚本"""
    fix_script = current_dir / "fix_lagrit_path.bat"
    
    with open(fix_script, "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("echo 修复 LaGriT PATH 问题...\n\n")
        
        if build_dir.exists() and (build_dir / "lagrit.exe").exists():
            f.write(f'set "PATH={build_dir};%PATH%"\n')
            f.write("echo ✓ 已将 LaGriT 添加到 PATH\n")
            f.write("echo 现在可以运行: lagrit\n")
            f.write("echo.\n")
            f.write("lagrit\n")
        else:
            f.write("echo ❌ 未找到 lagrit.exe\n")
            f.write("echo 请先运行安装脚本: python install_lagrit_windows.py\n")
            f.write("pause\n")
    
    print(f"\n📝 已创建快速修复脚本: {fix_script}")
    print("   运行此脚本可以临时修复PATH问题")

if __name__ == "__main__":
    check_lagrit_installation() 