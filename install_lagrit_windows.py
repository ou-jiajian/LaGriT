#!/usr/bin/env python3
"""
LaGriT Windows 完整一键安装脚本
自动安装和配置LaGriT在Windows系统上的完整运行环境

功能：
- 自动检测和安装MSYS2
- 安装必要的编译工具链
- 修复源代码兼容性问题
- 构建LaGriT可执行文件
- 创建conda环境
- 生成激活脚本

支持的系统：Windows 10/11
依赖：Anaconda 或 Miniconda
"""

import os
import sys
import subprocess
import platform
import urllib.request
from pathlib import Path
import time
import re

class LaGriTInstaller:
    def __init__(self):
        self.project_root = Path.cwd()
        self.env_name = "lagrit-env"
        self.conda_exe = self.find_conda()
        self.msys2_root = Path("C:/msys64")
        self.build_dir = self.project_root / "build"
        self.source_fixed = False
        
    def find_conda(self):
        """查找conda可执行文件"""
        conda_paths = [
            "conda",
            "conda.exe", 
            str(Path.home() / "anaconda3/Scripts/conda.exe"),
            str(Path.home() / "miniconda3/Scripts/conda.exe"),
            "C:/ProgramData/anaconda3/Scripts/conda.exe",
            "C:/ProgramData/miniconda3/Scripts/conda.exe"
        ]
        
        for conda_path in conda_paths:
            try:
                result = subprocess.run([conda_path, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✓ 找到 conda: {conda_path}")
                    return conda_path
            except (subprocess.SubprocessError, FileNotFoundError):
                continue
        
        raise RuntimeError("❌ 未找到 conda。请确保已安装 Anaconda 或 Miniconda")
    
    def check_platform(self):
        """检查系统平台"""
        if platform.system() != "Windows":
            raise RuntimeError("❌ 此脚本只支持 Windows 系统")
        
        print(f"✓ 系统平台: {platform.system()} {platform.release()}")
        print(f"✓ 架构: {platform.machine()}")
    
    def install_msys2(self):
        """安装 MSYS2 (如果未安装)"""
        if self.msys2_root.exists():
            print("✓ MSYS2 已存在")
            return
        
        print("📥 下载并安装 MSYS2...")
        msys2_url = "https://github.com/msys2/msys2-installer/releases/latest/download/msys2-x86_64-latest.exe"
        installer_path = Path("msys2-installer.exe")
        
        try:
            urllib.request.urlretrieve(msys2_url, installer_path)
            print("✓ MSYS2 下载完成")
            
            # 静默安装
            subprocess.run([str(installer_path), "--confirm-command", "install", 
                          "--accept-messages", "--root", str(self.msys2_root)], 
                         check=True)
            print("✓ MSYS2 安装完成")
            
        except Exception as e:
            print(f"❌ MSYS2 安装失败: {e}")
            print("请手动下载安装 MSYS2: https://www.msys2.org/")
            sys.exit(1)
        finally:
            if installer_path.exists():
                installer_path.unlink()
    
    def setup_msys2_packages(self):
        """在 MSYS2 中安装必要的包"""
        print("📦 安装 MSYS2 包...")

        msys2_cmd = str(self.msys2_root / "usr/bin/bash.exe")
        # 修正包名，移除不存在的包
        packages = [
            "gcc", "gcc-fortran", "gcc-libs",
            "make", "cmake", "wget", "curl",
            "zlib", "pkg-config"
        ]

        # 更新 pacman 数据库
        try:
            subprocess.run([msys2_cmd, "-lc", "pacman -Sy --noconfirm"], check=True)
        except subprocess.CalledProcessError:
            print("⚠️  更新pacman数据库失败，继续...")

        # 安装包
        for package in packages:
            try:
                subprocess.run([msys2_cmd, "-lc", f"pacman -S --noconfirm mingw-w64-x86_64-{package}"],
                             check=True)
                print(f"✓ 安装了 {package}")
            except subprocess.CalledProcessError:
                print(f"⚠️  安装 {package} 失败，继续...")

        # 尝试安装git（使用不同的包名）
        try:
            subprocess.run([msys2_cmd, "-lc", "pacman -S --noconfirm git"], check=True)
            print("✓ 安装了 git")
        except subprocess.CalledProcessError:
            print("⚠️  安装 git 失败，继续...")
    
    def create_conda_env(self):
        """创建 conda 环境"""
        print(f"🐍 创建 conda 环境: {self.env_name}")
        
        # 检查环境是否已存在
        try:
            result = subprocess.run([self.conda_exe, "env", "list"], 
                                  capture_output=True, text=True, check=True)
            if self.env_name in result.stdout:
                print(f"✓ conda 环境 {self.env_name} 已存在")
                return
        except subprocess.CalledProcessError:
            pass
        
        # 创建环境
        subprocess.run([
            self.conda_exe, "create", "-n", self.env_name, "-y",
            "python=3.9", "cmake", "numpy", "pexpect"
        ], check=True)
        print(f"✓ conda 环境 {self.env_name} 创建完成")
    
    def setup_environment_variables(self):
        """设置环境变量"""
        print("🔧 设置环境变量...")
        
        # 检查MSYS2是否安装成功
        if not self.msys2_root.exists():
            raise RuntimeError(f"MSYS2目录不存在: {self.msys2_root}")
        
        mingw64_bin = self.msys2_root / "mingw64" / "bin"
        if not mingw64_bin.exists():
            raise RuntimeError(f"MSYS2 MinGW64目录不存在: {mingw64_bin}")
        
        env_vars = {
            "CC": str(mingw64_bin / "gcc.exe"),
            "CXX": str(mingw64_bin / "g++.exe"),
            "FC": str(mingw64_bin / "gfortran.exe"),
            "CMAKE_C_COMPILER": str(mingw64_bin / "gcc.exe"),
            "CMAKE_CXX_COMPILER": str(mingw64_bin / "g++.exe"),
            "CMAKE_Fortran_COMPILER": str(mingw64_bin / "gfortran.exe"),
        }
        
        # 检查编译器文件是否存在
        for name, path in env_vars.items():
            if not Path(path).exists():
                print(f"⚠️  警告: {name} 编译器不存在: {path}")
        
        # 创建环境变量脚本
        env_script = self.project_root / "setup_env.bat"
        with open(env_script, "w", encoding="utf-8") as f:
            f.write("@echo off\n")
            f.write("REM LaGriT 环境变量设置\n\n")
            
            # 添加 MSYS2 到 PATH
            f.write(f'set "PATH={mingw64_bin};%PATH%"\n')
            f.write(f'set "PATH={self.msys2_root / "usr" / "bin"};%PATH%"\n\n')
            
            for var, value in env_vars.items():
                f.write(f'set "{var}={value}"\n')
                os.environ[var] = str(value)
            
            f.write("\necho ✓ LaGriT 环境变量已设置\n")
        
        print(f"✓ 环境变量脚本已创建: {env_script}")

    def fix_source_code(self):
        """修复源代码兼容性问题"""
        if self.source_fixed:
            return

        print("🔧 修复源代码兼容性问题...")

        # 修复 matrix_values_compress.c 中的函数指针类型问题
        matrix_file = self.project_root / "src" / "matrix_values_compress.c"
        if matrix_file.exists():
            try:
                with open(matrix_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 修复各种函数指针类型不匹配问题
                fixes = [
                    # 添加time.h头文件，移除错误的time()声明
                    (r'#include <math\.h>\s*\n\s*/\* function declaration \*/\s*\ntime\(\);',
                     '#include <math.h>\n#include <time.h>'),

                    # 修复SkipList结构体中的函数指针类型
                    (r'int_ptrsize\s+\(\*compare\)\(\);', 'int_ptrsize (*compare)(void *, void *);'),
                    (r'void\s+\(\*freeitem\)\(\);', 'void (*freeitem)(void *);'),

                    # 修复函数声明
                    (r'SkipList\s+NewSL\(int_ptrsize\s+\(\*compare\)\(\),\s*void\s+\(\*freeitem\)\(\),\s*int_ptrsize\s+flags\);',
                     'SkipList NewSL(int_ptrsize (*compare)(void *, void *), void (*freeitem)(void *), int_ptrsize flags);'),

                    (r'void\s+DoForSL\(SkipList\s+l,\s*int_ptrsize\s+\(\*function\)\(\),\s*void\s+\*arg\);',
                     'void DoForSL(SkipList l, int_ptrsize (*function)(void *, void *), void *arg);'),

                    # 修复函数实现
                    (r'SkipList\s+NewSL\(int_ptrsize\s+\(\*compare\)\(\),\s*void\s+\(\*freeitem\)\(\),\s*int_ptrsize\s+flags\)',
                     'SkipList NewSL(int_ptrsize (*compare)(void *, void *), void (*freeitem)(void *), int_ptrsize flags)'),

                    (r'void\s+DoForSL\(SkipList\s+l,\s*int_ptrsize\s+\(\*function\)\(\),\s*void\s+\*arg\)',
                     'void DoForSL(SkipList l, int_ptrsize (*function)(void *, void *), void *arg)'),

                    # 修复函数签名
                    (r'int_ptrsize\s+entryCompare\(entry\s+\*i,\s*entry\s+\*j\)',
                     'int_ptrsize entryCompare(void *i, void *j)'),

                    (r'void\s+entryFree\(entry\s+\*i\)',
                     'void entryFree(void *i)'),

                    (r'int_ptrsize\s+assignEntryNum\(entry\s+\*ec\)',
                     'int_ptrsize assignEntryNum(void *key, void *arg)'),

                    (r'int_ptrsize\s+populateX3dMatrixInfo\(entry\s+\*ec\)',
                     'int_ptrsize populateX3dMatrixInfo(void *key, void *arg)'),
                ]

                # 应用修复
                for pattern, replacement in fixes:
                    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

                # 修复函数体内的类型转换
                function_body_fixes = [
                    # entryCompare函数体
                    (r'(int_ptrsize\s+entryCompare\(void\s+\*i,\s*void\s+\*j\)[\s\S]*?{\s*)(int_ptrsize\s+i1,i2;)',
                     r'\1entry *ei = (entry *)i;\n   entry *ej = (entry *)j;\n   \2'),

                    (r'\bi->value\[', 'ei->value['),
                    (r'\bj->value\[', 'ej->value['),

                    # entryFree函数体
                    (r'(void\s+entryFree\(void\s+\*i\)[\s\S]*?{\s*)(free\(i->value\);)',
                     r'\1entry *e = (entry *)i;\n   free(e->value);\n   free(e);'),

                    # assignEntryNum函数体
                    (r'(int_ptrsize\s+assignEntryNum\(void\s+\*key,\s*void\s+\*arg\)[\s\S]*?{\s*)(entryNumber\+\+;)',
                     r'\1entry *ec = (entry *)key;\n  \2'),

                    # populateX3dMatrixInfo函数体
                    (r'(int_ptrsize\s+populateX3dMatrixInfo\(void\s+\*key,\s*void\s+\*arg\)[\s\S]*?{\s*)(int_ptrsize\s+k;)',
                     r'\1entry *ec = (entry *)key;\n  \2'),
                ]

                for pattern, replacement in function_body_fixes:
                    content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

                # 修复局部变量声明
                local_var_fixes = [
                    (r'int_ptrsize\s+\(\*compare\)\(\)\s*=\s*l->compare;',
                     'int_ptrsize (*compare)(void *, void *) = l->compare;'),

                    (r'void\s+\(\*freeitem\)\(\)\s*=\s*l->freeitem;',
                     'void (*freeitem)(void *) = l->freeitem;'),
                ]

                for pattern, replacement in local_var_fixes:
                    content = re.sub(pattern, replacement, content)

                # 写回文件
                with open(matrix_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                print("✓ 修复了 matrix_values_compress.c")

            except Exception as e:
                print(f"⚠️  修复 matrix_values_compress.c 失败: {e}")

        # 修复 metis_lg.c 中的指针类型问题
        metis_file = self.project_root / "src" / "metis_lg.c"
        if metis_file.exists():
            try:
                with open(metis_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 修复GKfree函数调用中的指针类型不匹配问题
                # 添加显式类型转换
                metis_fixes = [
                    (r'GKfree\(&kpwgts,\s*&padjncy,\s*&padjwgt,\s*&padjcut,\s*LTERM\);',
                     'GKfree((void**)&kpwgts, (void**)&padjncy, (void**)&padjwgt, (void**)&padjcut, LTERM);'),

                    (r'GKfree\(&cand,\s*&cand2,\s*LTERM\);',
                     'GKfree((void**)&cand, (void**)&cand2, LTERM);'),
                ]

                for pattern, replacement in metis_fixes:
                    content = re.sub(pattern, replacement, content)

                with open(metis_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                print("✓ 修复了 metis_lg.c")

            except Exception as e:
                print(f"⚠️  修复 metis_lg.c 失败: {e}")

        # 修复 sparseMatrix.c 中的fabs函数声明问题
        sparse_file = self.project_root / "src" / "sparseMatrix.c"
        if sparse_file.exists():
            try:
                with open(sparse_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 移除错误的fabs函数声明
                sparse_fixes = [
                    (r'extern double fabs\(\);\s*\n', ''),
                ]

                for pattern, replacement in sparse_fixes:
                    content = re.sub(pattern, replacement, content)

                with open(sparse_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                print("✓ 修复了 sparseMatrix.c")

            except Exception as e:
                print(f"⚠️  修复 sparseMatrix.c 失败: {e}")

        # 修复 Fortran 编译器标志配置
        fortran_cmake = self.project_root / "cmake" / "CompilerFlags-Fortran.cmake"
        if fortran_cmake.exists():
            try:
                with open(fortran_cmake, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 添加Windows MinGW特殊处理
                if "Windows MinGW" not in content:
                    new_content = content.replace(
                        "include(CheckFortranCompilerFlag)",
                        """include(CheckFortranCompilerFlag)

# Windows MSYS2/MinGW特殊处理
if(WIN32 AND MINGW)
  message(STATUS "  Fortran compiler: Windows MinGW GFORTRAN")
  # 在Windows MinGW环境下，先不设置复杂的标志，让编译器识别成功
  if(NOT CMAKE_Fortran_FLAGS)
    set(CMAKE_Fortran_FLAGS "")
  endif()
  # 在配置完成后再添加必要的标志
  set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -fcray-pointer -fdefault-integer-8 -std=legacy -fno-sign-zero -fno-range-check")

# set known compiler flags
el"""
                    )

                    with open(fortran_cmake, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    print("✓ 修复了 Fortran 编译器配置")

            except Exception as e:
                print(f"⚠️  修复 Fortran 配置失败: {e}")

        self.source_fixed = True
        print("✓ 源代码兼容性修复完成")

    def build_lagrit(self):
        """构建 LaGriT"""
        print("🔨 构建 LaGriT...")

        # 先修复源代码
        self.fix_source_code()

        # 清理并创建构建目录
        if self.build_dir.exists():
            import shutil
            shutil.rmtree(self.build_dir)
            print("✓ 清理了旧的构建目录")

        self.build_dir.mkdir(exist_ok=True)
        os.chdir(self.build_dir)

        try:
            # 设置环境变量
            build_env = os.environ.copy()

            # 添加MSYS2路径到环境变量
            msys2_mingw_path = str(self.msys2_root / "mingw64" / "bin")
            msys2_usr_path = str(self.msys2_root / "usr" / "bin")

            if "PATH" in build_env:
                build_env["PATH"] = f"{msys2_mingw_path};{msys2_usr_path};{build_env['PATH']}"
            else:
                build_env["PATH"] = f"{msys2_mingw_path};{msys2_usr_path}"

            # 设置编译器环境变量
            build_env["CC"] = str(self.msys2_root / "mingw64" / "bin" / "gcc.exe")
            build_env["CXX"] = str(self.msys2_root / "mingw64" / "bin" / "g++.exe")
            build_env["FC"] = str(self.msys2_root / "mingw64" / "bin" / "gfortran.exe")

            print(f"🔧 设置编译器路径:")
            print(f"   CC: {build_env['CC']}")
            print(f"   CXX: {build_env['CXX']}")
            print(f"   FC: {build_env['FC']}")

            # 检查编译器是否存在
            compilers = [
                ("C编译器", build_env['CC']),
                ("C++编译器", build_env['CXX']),
                ("Fortran编译器", build_env['FC'])
            ]

            for name, path in compilers:
                if not Path(path).exists():
                    raise RuntimeError(f"{name}不存在: {path}")

            # 配置 cmake - 使用完整路径
            mingw64_bin = self.msys2_root / "mingw64" / "bin"
            cmake_exe = mingw64_bin / "cmake.exe"
            make_exe = mingw64_bin / "mingw32-make.exe"  # 使用正确的make程序名

            # 检查构建工具是否存在
            build_tools = [
                ("CMake", cmake_exe),
                ("Make", make_exe)
            ]

            for name, path in build_tools:
                if not path.exists():
                    raise RuntimeError(f"{name}不存在: {path}")

            cmake_cmd = [
                str(cmake_exe), "..",
                "-G", "MinGW Makefiles",
                "-DCMAKE_BUILD_TYPE=Release",
                "-DLAGRIT_BUILD_STATIC=ON",
                "-DLAGRIT_BUILD_EXODUS=OFF",  # 禁用 Exodus
                "-DLAGRIT_BUILD_GMV=OFF",     # 禁用 GMV
                f"-DCMAKE_C_COMPILER={build_env['CC']}",
                f"-DCMAKE_CXX_COMPILER={build_env['CXX']}",
                f"-DCMAKE_Fortran_COMPILER={build_env['FC']}",
                "-DCMAKE_C_FLAGS=-w -Wno-implicit-function-declaration -Wno-implicit-int -Wno-incompatible-pointer-types",
                "-DCMAKE_CXX_FLAGS=-w",
                # 让CMake自动检测Fortran标志
                "-DCMAKE_Fortran_FLAGS="
            ]

            print("🔧 运行 cmake 配置...")
            print(f"🔧 cmake路径: {cmake_exe}")
            print(f"🔧 工作目录: {self.build_dir}")

            result = subprocess.run(cmake_cmd, cwd=self.build_dir, env=build_env,
                                  capture_output=True, text=True)

            if result.returncode != 0:
                print("❌ CMake 配置失败")
                print("STDOUT:", result.stdout[-1000:])
                print("STDERR:", result.stderr[-1000:])
                raise RuntimeError("CMake配置失败")

            print("✓ cmake 配置完成")

            # 构建
            print("🔨 编译 LaGriT...")
            print(f"🔧 make路径: {make_exe}")

            result = subprocess.run([str(make_exe), "-j2"], cwd=self.build_dir, env=build_env,
                                  capture_output=True, text=True)

            if result.returncode != 0:
                print("❌ 编译失败")
                print("STDOUT:", result.stdout[-2000:])
                print("STDERR:", result.stderr[-2000:])
                raise RuntimeError("编译失败")

            print("✓ LaGriT 编译完成")

            # 检查生成的可执行文件
            lagrit_exe = self.build_dir / "lagrit.exe"
            if not lagrit_exe.exists():
                raise RuntimeError("lagrit.exe 未生成")

            print(f"✓ 生成了可执行文件: {lagrit_exe}")

        except Exception as e:
            print(f"❌ 构建失败: {e}")
            print("\n请检查:")
            print("1. MSYS2是否正确安装")
            print("2. 所有依赖包是否安装完整")
            print("3. 网络连接是否正常")
            raise
        finally:
            os.chdir(self.project_root)
    
    def setup_pylagrit(self):
        """设置 PyLaGriT"""
        print("🐍 设置 PyLaGriT...")
        
        pylagrit_dir = self.project_root / "PyLaGriT"
        if not pylagrit_dir.exists():
            print("⚠️  PyLaGriT 目录不存在，跳过")
            return
        
        # 激活环境并安装
        try:
            # 注意：PyLaGriT 需要 pexpect，但在 Windows 上可能有问题
            print("⚠️  注意：PyLaGriT 在 Windows 上可能不完全兼容")
            print("   建议在 WSL 或 Linux 环境中使用 PyLaGriT")
            
            # 可以尝试安装，但用户需要知道限制
            response = input("是否仍要尝试安装 PyLaGriT? (y/N): ")
            if response.lower() == 'y':
                os.chdir(pylagrit_dir)
                subprocess.run([
                    self.conda_exe, "run", "-n", self.env_name,
                    "pip", "install", "-e", "."
                ], check=True)
                print("✓ PyLaGriT 安装完成（可能需要 WSL 才能正常工作）")
                
        except subprocess.CalledProcessError as e:
            print(f"⚠️  PyLaGriT 安装失败: {e}")
        finally:
            os.chdir(self.project_root)
    
    def test_installation(self):
        """测试安装"""
        print("🧪 测试 LaGriT 安装...")
        
        lagrit_exe = self.build_dir / "lagrit.exe"
        if not lagrit_exe.exists():
            print("❌ lagrit.exe 未找到")
            return False
        
        try:
            # 运行简单测试
            result = subprocess.run([str(lagrit_exe)], 
                                  input="test\nfinish\n", 
                                  text=True, capture_output=True, timeout=30)
            
            if "LaGriT successfully completed" in result.stdout:
                print("✓ LaGriT 测试通过")
                return True
            else:
                print("⚠️  LaGriT 测试可能有问题")
                print(f"输出: {result.stdout}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️  LaGriT 测试超时")
            return False
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False
    
    def create_activation_script(self):
        """创建激活脚本"""
        print("📝 创建激活脚本...")
        
        activate_script = self.project_root / "activate_lagrit.bat"
        with open(activate_script, "w", encoding="utf-8") as f:
            f.write("@echo off\n")
            f.write("echo 激活 LaGriT 环境...\n\n")
            
            # 调用环境变量设置
            f.write("call setup_env.bat\n\n")
            
            # 激活 conda 环境
            f.write(f"call {self.conda_exe} activate {self.env_name}\n\n")
            
            # 添加构建目录到 PATH
            f.write(f'set "PATH={self.build_dir};%PATH%"\n\n')
            
            f.write("echo ✓ LaGriT 环境已激活\n")
            f.write("echo 可以运行以下命令:\n")
            f.write("echo   lagrit        - 启动 LaGriT\n")
            f.write("echo   python        - 启动 Python (如果安装了 PyLaGriT)\n")
            f.write("echo.\n")
            f.write("cmd /k\n")  # 保持命令行开启
        
        print(f"✓ 激活脚本已创建: {activate_script}")
    
    def create_usage_guide(self):
        """创建使用指南"""
        guide_path = self.project_root / "WINDOWS_USAGE_GUIDE.md"
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write("# LaGriT Windows 使用指南\n\n")
            f.write("## 快速开始\n\n")
            f.write("1. 双击运行 `activate_lagrit.bat` 激活环境\n")
            f.write("2. 在打开的命令行中输入 `lagrit` 启动程序\n")
            f.write("3. 在 LaGriT 中输入 `test` 运行测试\n")
            f.write("4. 输入 `finish` 退出程序\n\n")
            
            f.write("## 文件说明\n\n")
            f.write("- `lagrit.exe`: LaGriT 主程序\n")
            f.write("- `activate_lagrit.bat`: 环境激活脚本\n")
            f.write("- `setup_env.bat`: 环境变量设置脚本\n")
            f.write("- `build/`: 构建输出目录\n\n")
            
            f.write("## 故障排除\n\n")
            f.write("### 如果遇到编译错误:\n")
            f.write("1. 确保 MSYS2 正确安装\n")
            f.write("2. 检查编译器是否在 PATH 中\n")
            f.write("3. 重新运行安装脚本\n\n")
            
            f.write("### 如果 LaGriT 无法启动:\n")
            f.write("1. 检查 `lagrit.exe` 是否存在\n")
            f.write("2. 确保所有 DLL 依赖项可用\n")
            f.write("3. 在 MSYS2 环境中测试\n\n")
            
            f.write("### PyLaGriT 使用注意:\n")
            f.write("- PyLaGriT 在 Windows 上支持有限\n")
            f.write("- 建议在 WSL 或 Linux 环境中使用\n")
            f.write("- 如需在 Windows 使用，可考虑使用 Docker\n\n")
            
            f.write("## 更多资源\n\n")
            f.write("- [LaGriT 官方文档](https://lanl.github.io/LaGriT/)\n")
            f.write("- [GitHub 仓库](https://github.com/lanl/LaGriT)\n")
            f.write("- [问题报告](https://github.com/lanl/LaGriT/issues)\n")
        
        print(f"✓ 使用指南已创建: {guide_path}")
    
    def run_installation(self):
        """执行完整安装"""
        print("🚀 LaGriT Windows 完整一键安装")
        print("=" * 60)
        print("此脚本将自动完成以下步骤:")
        print("1. 检查系统环境")
        print("2. 安装/配置 MSYS2 和编译工具")
        print("3. 修复源代码兼容性问题")
        print("4. 创建 conda 环境")
        print("5. 构建 LaGriT 可执行文件")
        print("6. 生成激活脚本和使用指南")
        print("=" * 60)

        start_time = time.time()

        try:
            # 步骤1: 检查系统
            print("\n📋 步骤 1/6: 检查系统环境")
            self.check_platform()

            # 步骤2: 安装和配置 MSYS2
            print("\n🔧 步骤 2/6: 安装和配置编译环境")
            self.install_msys2()
            self.setup_msys2_packages()

            # 步骤3: 创建 conda 环境
            print("\n🐍 步骤 3/6: 创建 conda 环境")
            self.create_conda_env()

            # 步骤4: 设置环境变量
            print("\n⚙️  步骤 4/6: 配置环境变量")
            self.setup_environment_variables()

            # 步骤5: 构建 LaGriT (包含源代码修复)
            print("\n🔨 步骤 5/6: 构建 LaGriT")
            self.build_lagrit()

            # 步骤6: 测试和创建脚本
            print("\n📝 步骤 6/6: 生成脚本和文档")
            success = self.test_installation()
            self.create_activation_script()
            self.create_usage_guide()

            # 可选: 设置 PyLaGriT
            print("\n🐍 可选: PyLaGriT 设置")
            try:
                self.setup_pylagrit()
            except Exception as e:
                print(f"⚠️  PyLaGriT 设置跳过: {e}")

            elapsed_time = time.time() - start_time

            print("\n" + "=" * 60)
            if success:
                print("🎉 LaGriT 完整安装成功！")
                print(f"⏱️  总耗时: {elapsed_time:.1f} 秒")
            else:
                print("⚠️  LaGriT 安装完成，但测试可能有问题")

            print("\n🚀 快速开始:")
            print("1. 双击运行 'activate_lagrit.bat' 激活环境")
            print("2. 在打开的命令行中输入 'lagrit' 启动程序")
            print("3. 在 LaGriT 中输入 'test' 运行测试")
            print("4. 输入 'finish' 退出程序")

            print("\n📚 更多信息:")
            print("- 查看 'WINDOWS_USAGE_GUIDE.md' 了解详细使用方法")
            print("- LaGriT 可执行文件位置:", self.build_dir / "lagrit.exe")
            print("- 环境激活脚本:", self.project_root / "activate_lagrit.bat")

            return True

        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"\n❌ 安装失败 (耗时: {elapsed_time:.1f} 秒)")
            print(f"错误信息: {e}")
            print("\n🔍 故障排除:")
            print("1. 确保网络连接正常")
            print("2. 以管理员权限运行此脚本")
            print("3. 确保有足够的磁盘空间 (至少2GB)")
            print("4. 检查防火墙/杀毒软件是否阻止下载")
            print("5. 如果问题持续，请查看详细错误信息")
            return False

def main():
    """主函数"""
    print("LaGriT Windows 完整一键安装程序")
    print("=" * 50)
    print("版本: 2.0 - 完整自动化安装")
    print("支持: Windows 10/11 + MSYS2 + Conda")
    print("=" * 50)

    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要 Python 3.7 或更高版本")
        sys.exit(1)

    # 检查是否在正确的目录
    if not Path("CMakeLists.txt").exists():
        print("❌ 请在 LaGriT 项目根目录下运行此脚本")
        print("   (应该包含 CMakeLists.txt 文件)")
        sys.exit(1)

    try:
        installer = LaGriTInstaller()
        success = installer.run_installation()
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n⚠️  安装被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 安装过程中发生未预期的错误: {e}")
        print("请将此错误信息报告给开发者")
        sys.exit(1)

if __name__ == "__main__":
    main()