#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaGriT 重新编译脚本
用于修改源代码后重新构建LaGriT
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil
import re

def rebuild_lagrit():
    """重新编译LaGriT"""
    print("🔨 LaGriT 重新编译工具")
    print("=" * 50)
    
    current_dir = Path.cwd()
    build_dir = current_dir / "build"
    
    print(f"📁 项目目录: {current_dir}")
    print(f"🔨 构建目录: {build_dir}")
    
    # 检查MSYS2
    msys2_root = Path("C:/msys64")
    if not msys2_root.exists():
        print("❌ 未找到MSYS2，请先运行: python install_lagrit_windows.py")
        return False
    
    mingw64_bin = msys2_root / "mingw64" / "bin"
    
    # 检查必要文件
    if not (current_dir / "CMakeLists.txt").exists():
        print("❌ 未找到CMakeLists.txt，请确保在LaGriT项目根目录")
        return False
    
    print("✓ 环境检查通过")
    
    # 清理并重建build目录
    print("\n🧹 清理构建目录...")
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print("✓ 已清理旧的构建文件")
    
    build_dir.mkdir()
    print("✓ 已创建新的构建目录")
    
    try:
        # 设置环境变量
        env = os.environ.copy()
        env["PATH"] = f"{mingw64_bin};{msys2_root / 'usr/bin'};" + env.get("PATH", "")
        env["CC"] = str(mingw64_bin / "gcc.exe")
        env["CXX"] = str(mingw64_bin / "g++.exe")
        env["FC"] = str(mingw64_bin / "gfortran.exe")
        
        os.chdir(build_dir)
        
        # CMake配置
        print("\n⚙️  运行CMake配置...")
        cmake_cmd = [
            str(mingw64_bin / "cmake.exe"), "..",
            "-G", "MinGW Makefiles",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DLAGRIT_BUILD_STATIC=ON",
            "-DLAGRIT_BUILD_EXODUS=OFF"
        ]
        
        result = subprocess.run(cmake_cmd, env=env, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print("❌ CMake配置失败")
            print("错误信息:", result.stderr[-1000:])
            return False
        
        print("✓ CMake配置完成")
        
        # Make构建
        print("\n🔨 编译LaGriT...")
        make_cmd = [str(mingw64_bin / "mingw32-make.exe"), "-j4"]
        
        result = subprocess.run(make_cmd, env=env, capture_output=True, text=True, timeout=1800)
        
        if result.returncode != 0:
            print("❌ 编译失败")
            print("错误信息:", result.stderr[-1000:])
            
            # 检查是否是已知的metis_lg.c指针类型错误
            if "incompatible pointer type" in result.stderr and "metis_lg.c" in result.stderr:
                print("\n🔧 检测到metis_lg.c指针类型错误，正在修复...")
                if fix_metis_pointer_error(current_dir):
                    print("🔄 重新尝试编译...")
                    result = subprocess.run(make_cmd, env=env, capture_output=True, text=True, timeout=1800)
                    if result.returncode != 0:
                        print("❌ 修复后编译仍然失败")
                        print("错误信息:", result.stderr[-1000:])
                        return False
                else:
                    return False
            else:
                return False
        
        print("✓ 编译完成")
        
        # 检查生成的可执行文件
        lagrit_exe = build_dir / "lagrit.exe"
        if lagrit_exe.exists():
            print(f"\n✅ 重新编译成功！")
            print(f"📍 位置: {lagrit_exe}")
            print(f"📏 大小: {lagrit_exe.stat().st_size / 1024 / 1024:.1f} MB")
            
            # 简单测试
            print("\n🧪 快速测试...")
            try:
                test_result = subprocess.run([str(lagrit_exe)], 
                                           input="finish\n", 
                                           text=True, 
                                           capture_output=True, 
                                           timeout=30,
                                           env=env)
                if test_result.returncode == 0 or "LaGriT" in test_result.stdout:
                    print("✓ 测试通过")
                else:
                    print("⚠️  测试可能有问题")
            except Exception as e:
                print(f"⚠️  测试时出错: {e}")
            
            return True
        else:
            print("❌ 未生成lagrit.exe")
            return False
            
    except Exception as e:
        print(f"❌ 编译过程出错: {e}")
        return False
    finally:
        os.chdir(current_dir)

def fix_metis_pointer_error(project_dir):
    """修复metis_lg.c中的指针类型错误"""
    metis_file = project_dir / "src" / "metis_lg.c"
    
    if not metis_file.exists():
        print("⚠️  metis_lg.c 文件不存在")
        return False
    
    try:
        # 读取文件内容
        with open(metis_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经修复
        if "(void**)&" in content:
            print("✓ metis_lg.c 指针错误已经修复")
            return True
        
        # 修复指针类型转换错误
        fixes = [
            # 修复GKfree调用中的指针类型不匹配
            (r'GKfree\(&([^,\)]+),([^)]*)\);', r'GKfree((void**)&\1,\2);'),
            
            # 特殊处理一些复杂的调用
            (r'GKfree\(\(void\*\*\)\(void\*\*\)&([^,\)]+),([^)]*)\);', r'GKfree((void**)&\1,\2);'),
        ]
        
        original_content = content
        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(metis_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✓ 已修复 metis_lg.c 指针类型错误")
            return True
        else:
            print("⚠️  未找到需要修复的指针错误")
            return False
            
    except Exception as e:
        print(f"❌ 修复 metis_lg.c 时出错: {e}")
        return False

def main():
    """主函数"""
    print("LaGriT 重新编译工具")
    print("适用于修改源代码后重新构建")
    print("=" * 50)
    
    success = rebuild_lagrit()
    
    if success:
        print("\n🎉 重新编译完成！")
        print("\n现在可以使用:")
        print("- start_lagrit.bat (启动LaGriT)")
        print("- test_lagrit.bat (快速测试)")
    else:
        print("\n❌ 重新编译失败")
        print("如果问题持续，请运行完整安装:")
        print("python install_lagrit_windows.py")

if __name__ == "__main__":
    main() 