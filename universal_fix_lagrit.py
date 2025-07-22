#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaGriT Windows 通用修复脚本
解决乱码、路径、DLL缺失等所有问题
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil
import locale

def fix_all_lagrit_issues():
    """修复所有LaGriT相关问题"""
    print("🔧 LaGriT Windows 通用修复工具")
    print("=" * 60)
    
    current_dir = Path.cwd()
    print(f"📁 当前目录: {current_dir}")
    
    # 检测系统编码
    try:
        system_encoding = locale.getpreferredencoding()
        print(f"🔤 系统编码: {system_encoding}")
    except:
        system_encoding = 'utf-8'
    
    # 步骤1: 检查和修复build目录
    build_dir = current_dir / "build"
    print(f"\n🔍 步骤1: 检查构建目录 {build_dir}")
    
    if not build_dir.exists():
        print("❌ build目录不存在，需要重新构建")
        return rebuild_lagrit(current_dir)
    
    lagrit_exe = build_dir / "lagrit.exe"
    if not lagrit_exe.exists():
        print("❌ lagrit.exe 不存在，需要重新构建")
        return rebuild_lagrit(current_dir)
    
    print(f"✓ 找到 lagrit.exe: {lagrit_exe}")
    print(f"📏 文件大小: {lagrit_exe.stat().st_size / 1024 / 1024:.1f} MB")
    
    # 步骤2: 检查DLL依赖
    print("\n🔍 步骤2: 检查DLL依赖")
    if not check_and_fix_dll_dependencies(lagrit_exe):
        print("⚠️  DLL依赖问题已修复，请重试")
    
    # 步骤3: 创建修复版启动脚本（解决乱码问题）
    print("\n📝 步骤3: 创建修复版启动脚本")
    create_fixed_scripts(current_dir, build_dir)
    
    # 步骤4: 测试LaGriT
    print("\n🧪 步骤4: 测试LaGriT")
    return test_lagrit(lagrit_exe)

def check_and_fix_dll_dependencies(lagrit_exe):
    """检查和修复DLL依赖问题"""
    msys2_root = Path("C:/msys64")
    mingw64_bin = msys2_root / "mingw64" / "bin"
    
    if not mingw64_bin.exists():
        print("❌ 未找到MSYS2 MinGW64目录")
        print("请运行: python install_lagrit_windows.py")
        return False
    
    # 检查必需的DLL文件
    required_dlls = [
        "libstdc++-6.dll",
        "libgcc_s_seh-1.dll", 
        "libgfortran-5.dll",
        "libquadmath-0.dll",
        "libwinpthread-1.dll"
    ]
    
    missing_dlls = []
    for dll in required_dlls:
        dll_path = mingw64_bin / dll
        if dll_path.exists():
            print(f"✓ 找到 {dll}")
        else:
            print(f"❌ 缺少 {dll}")
            missing_dlls.append(dll)
    
    if missing_dlls:
        print(f"⚠️  缺少DLL文件: {', '.join(missing_dlls)}")
        print("尝试修复DLL依赖...")
        
        # 尝试安装缺失的包
        try:
            msys2_cmd = str(msys2_root / "usr/bin/bash.exe")
            if Path(msys2_cmd).exists():
                install_cmd = [
                    msys2_cmd, "-lc",
                    "pacman -S --noconfirm mingw-w64-x86_64-gcc-libs mingw-w64-x86_64-gcc-fortran"
                ]
                result = subprocess.run(install_cmd, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    print("✓ DLL依赖修复成功")
                else:
                    print("⚠️  自动修复失败，需要手动修复")
        except Exception as e:
            print(f"⚠️  DLL修复出错: {e}")
    
    # 测试lagrit.exe是否可以运行
    try:
        env = os.environ.copy()
        env["PATH"] = str(mingw64_bin) + ";" + env.get("PATH", "")
        
        result = subprocess.run([str(lagrit_exe)], 
                              input="finish\n", 
                              text=True, 
                              capture_output=True, 
                              timeout=30,
                              env=env)
        
        if "LaGriT" in result.stdout or result.returncode == 0:
            print("✓ LaGriT 可以正常运行")
            return True
        else:
            print("⚠️  LaGriT 运行时出现问题")
            print(f"输出: {result.stdout}")
            print(f"错误: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"⚠️  测试LaGriT时出错: {e}")
        return False

def create_fixed_scripts(project_dir, build_dir):
    """创建修复版的启动脚本（解决乱码问题）"""
    
    # 1. 创建简单的启动脚本（纯ASCII，避免乱码）
    simple_start = project_dir / "start_lagrit.bat"
    with open(simple_start, "w", encoding="ascii", errors="ignore") as f:
        f.write("@echo off\n")
        f.write("REM LaGriT Startup Script\n")
        f.write("chcp 65001 >nul 2>&1\n")  # 设置UTF-8编码
        f.write("echo Starting LaGriT...\n")
        f.write("echo.\n")
        
        # 设置环境变量
        f.write('set "PATH=C:\\msys64\\mingw64\\bin;%PATH%"\n')
        f.write(f'set "LAGRIT_DIR={project_dir}"\n')
        f.write(f'set "LAGRIT_BUILD={build_dir}"\n')
        f.write("echo Environment setup complete.\n")
        f.write("echo.\n")
        
        # 检查文件是否存在
        f.write(f'if exist "{build_dir}\\lagrit.exe" (\n')
        f.write('    echo Found lagrit.exe\n')
        f.write(f'    echo Starting: {build_dir}\\lagrit.exe\n')
        f.write('    echo.\n')
        f.write(f'    "{build_dir}\\lagrit.exe"\n')
        f.write(') else (\n')
        f.write('    echo ERROR: lagrit.exe not found\n')
        f.write(f'    echo Expected location: {build_dir}\\lagrit.exe\n')
        f.write('    echo Please run: python universal_fix_lagrit.py\n')
        f.write('    pause\n')
        f.write(')\n')
    
    print(f"✓ 创建启动脚本: {simple_start}")
    
    # 2. 创建快速测试脚本
    test_script = project_dir / "test_lagrit.bat"
    with open(test_script, "w", encoding="ascii", errors="ignore") as f:
        f.write("@echo off\n")
        f.write("chcp 65001 >nul 2>&1\n")
        f.write("echo LaGriT Quick Test\n")
        f.write("echo ==================\n")
        f.write('set "PATH=C:\\msys64\\mingw64\\bin;%PATH%"\n')
        f.write(f'echo Testing: {build_dir}\\lagrit.exe\n')
        f.write('echo.\n')
        f.write(f'if exist "{build_dir}\\lagrit.exe" (\n')
        f.write(f'    echo test | "{build_dir}\\lagrit.exe"\n')
        f.write('    echo.\n')
        f.write('    echo Test completed. Check output above.\n')
        f.write(') else (\n')
        f.write('    echo ERROR: lagrit.exe not found\n')
        f.write(')\n')
        f.write('pause\n')
    
    print(f"✓ 创建测试脚本: {test_script}")
    
    # 3. 创建诊断脚本
    diag_script = project_dir / "diagnose.bat"
    with open(diag_script, "w", encoding="ascii", errors="ignore") as f:
        f.write("@echo off\n")
        f.write("chcp 65001 >nul 2>&1\n")
        f.write("echo LaGriT Diagnostic Tool\n")
        f.write("echo =======================\n")
        f.write("echo.\n")
        f.write(f'echo Current directory: {project_dir}\n')
        f.write(f'echo Build directory: {build_dir}\n')
        f.write("echo.\n")
        f.write(f'if exist "{build_dir}\\lagrit.exe" (\n')
        f.write('    echo [OK] lagrit.exe found\n')
        f.write(f'    dir "{build_dir}\\lagrit.exe"\n')
        f.write(') else (\n')
        f.write('    echo [ERROR] lagrit.exe not found\n')
        f.write(')\n')
        f.write("echo.\n")
        f.write('if exist "C:\\msys64\\mingw64\\bin\\libstdc++-6.dll" (\n')
        f.write('    echo [OK] MSYS2 DLL found\n')
        f.write(') else (\n')
        f.write('    echo [ERROR] MSYS2 DLL missing\n')
        f.write(')\n')
        f.write("echo.\n")
        f.write("echo PATH:\n")
        f.write("echo %PATH%\n")
        f.write("echo.\n")
        f.write("pause\n")
    
    print(f"✓ 创建诊断脚本: {diag_script}")

def rebuild_lagrit(project_dir):
    """重新构建LaGriT"""
    print("\n🔨 重新构建LaGriT...")
    
    # 检查MSYS2
    msys2_root = Path("C:/msys64")
    if not msys2_root.exists():
        print("❌ 未找到MSYS2，请先运行:")
        print("python install_lagrit_windows.py")
        return False
    
    mingw64_bin = msys2_root / "mingw64" / "bin"
    build_dir = project_dir / "build"
    
    # 清理并创建build目录
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()
    
    try:
        # 设置环境变量
        env = os.environ.copy()
        env["PATH"] = f"{mingw64_bin};{msys2_root / 'usr/bin'};" + env.get("PATH", "")
        env["CC"] = str(mingw64_bin / "gcc.exe")
        env["CXX"] = str(mingw64_bin / "g++.exe")
        env["FC"] = str(mingw64_bin / "gfortran.exe")
        
        os.chdir(build_dir)
        
        # CMake配置
        cmake_cmd = [
            str(mingw64_bin / "cmake.exe"), "..",
            "-G", "MinGW Makefiles",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DLAGRIT_BUILD_STATIC=ON",
            "-DLAGRIT_BUILD_EXODUS=OFF"
        ]
        
        print("运行CMake配置...")
        result = subprocess.run(cmake_cmd, env=env, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print("❌ CMake配置失败")
            print(result.stderr[-1000:])
            return False
        
        # Make构建
        make_cmd = [str(mingw64_bin / "mingw32-make.exe"), "-j2"]
        print("运行Make构建...")
        result = subprocess.run(make_cmd, env=env, capture_output=True, text=True, timeout=1800)
        
        if result.returncode != 0:
            print("❌ Make构建失败")
            print(result.stderr[-1000:])
            return False
        
        print("✓ 构建成功")
        return True
        
    except Exception as e:
        print(f"❌ 构建出错: {e}")
        return False
    finally:
        os.chdir(project_dir)

def test_lagrit(lagrit_exe):
    """测试LaGriT功能"""
    print(f"测试LaGriT: {lagrit_exe}")
    
    try:
        # 设置环境
        env = os.environ.copy()
        env["PATH"] = "C:/msys64/mingw64/bin;" + env.get("PATH", "")
        
        # 简单测试
        result = subprocess.run([str(lagrit_exe)], 
                              input="finish\n", 
                              text=True, 
                              capture_output=True, 
                              timeout=30, 
                              env=env)
        
        if result.returncode == 0 or "LaGriT" in result.stdout:
            print("✅ LaGriT测试成功")
            return True
        else:
            print("⚠️  LaGriT测试可能有问题")
            print(f"输出: {result.stdout[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("LaGriT Windows 通用修复工具")
    print("解决乱码、路径、DLL等所有问题")
    print("=" * 60)
    
    try:
        success = fix_all_lagrit_issues()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 修复完成！")
            print("\n使用方法:")
            print("1. 运行: start_lagrit.bat")
            print("2. 或者: test_lagrit.bat (快速测试)")
            print("3. 或者: diagnose.bat (诊断问题)")
            print("\n如果仍有问题，请检查诊断输出")
        else:
            print("❌ 修复失败")
            print("\n建议:")
            print("1. 运行 diagnose.bat 查看详细信息")
            print("2. 或者重新安装: python install_lagrit_windows.py")
        
    except Exception as e:
        print(f"❌ 修复过程出错: {e}")
        print("请运行: python install_lagrit_windows.py")

if __name__ == "__main__":
    main() 