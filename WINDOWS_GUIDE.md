# LaGriT Windows 安装和使用指南

## 📋 总览

LaGriT是一个用于网格生成和操作的工具。本指南提供Windows系统下的完整安装和使用说明。

## 🚀 快速开始

### 1. 一键安装（首次安装）

```bash
python install_lagrit_windows.py
```

这个脚本会自动完成：
- 安装MSYS2和编译工具
- 创建conda环境
- 编译LaGriT
- 生成启动脚本

### 2. 修复和诊断问题

如果安装后无法正常启动，运行修复工具：

```bash
python universal_fix_lagrit.py
```

这会创建3个无乱码的启动脚本：
- `start_lagrit.bat` - 主启动脚本
- `test_lagrit.bat` - 快速测试脚本  
- `diagnose.bat` - 诊断工具

### 3. 启动LaGriT

安装完成后，使用以下方式启动：

```bash
# 方法1: 直接双击
start_lagrit.bat

# 方法2: 命令行运行
start_lagrit.bat
```

## 📁 重要脚本说明

### Python脚本（.py文件）

| 脚本名称 | 用途 | 何时使用 |
|---------|------|----------|
| `install_lagrit_windows.py` | 完整一键安装 | 首次安装LaGriT |
| `universal_fix_lagrit.py` | 修复安装问题 | 安装后无法启动时 |
| `rebuild_lagrit.py` | 重新编译 | 修改源代码后 |

### 批处理脚本（.bat文件）

| 脚本名称 | 用途 | 何时使用 |
|---------|------|----------|
| `start_lagrit.bat` | 启动LaGriT | 日常使用LaGriT |
| `test_lagrit.bat` | 快速测试 | 验证LaGriT功能 |
| `diagnose.bat` | 诊断问题 | 排查启动问题 |
| `setup_env.bat` | 设置环境变量 | 由其他脚本调用 |

## 🔄 常见使用场景

### 场景1: 首次安装
```bash
# 1. 运行一键安装
python install_lagrit_windows.py

# 2. 如果有问题，运行修复
python universal_fix_lagrit.py

# 3. 启动LaGriT
start_lagrit.bat
```

### 场景2: 修改源代码后重新编译
```bash
# 1. 修改src/目录下的源文件
# 2. 重新编译
python rebuild_lagrit.py

# 3. 启动新版本
start_lagrit.bat
```

### 场景3: 启动有问题
```bash
# 1. 运行诊断
diagnose.bat

# 2. 如果诊断发现问题，运行修复
python universal_fix_lagrit.py

# 3. 重新启动
start_lagrit.bat
```

## 🐍 Conda环境管理

### 激活LaGriT环境
```bash
# 激活conda环境
conda activate lagrit-env

# 检查环境
conda list
```

### 手动设置环境（如果需要）
```bash
# 如果conda环境有问题，可以手动创建
conda create -n lagrit-env python=3.9
conda activate lagrit-env
conda install cmake numpy
```

## 🔧 故障排除

### 问题1: 'lagrit' is not recognized
**解决方案**: 
```bash
# 运行修复脚本
python universal_fix_lagrit.py

# 或直接使用生成的启动脚本
start_lagrit.bat
```

### 问题2: DLL缺失错误
**解决方案**: 
```bash
# universal_fix_lagrit.py会自动检查和修复DLL依赖
python universal_fix_lagrit.py
```

### 问题3: 乱码显示
**解决方案**: 
- 不要使用旧的bat文件
- 使用universal_fix_lagrit.py生成的新脚本

### 问题4: 编译错误
**解决方案**: 
```bash
# 重新运行完整安装
python install_lagrit_windows.py
```

## 📝 LaGriT基本使用

启动LaGriT后，可以使用以下基本命令：

```
# LaGriT命令行中：
test              # 运行内置测试
help              # 显示帮助
quality           # 网格质量分析
dump/avs filename # 导出AVS格式
finish            # 退出LaGriT
```

## 🗂️ 文件结构

```
LaGriT/
├── install_lagrit_windows.py     # 一键安装脚本
├── universal_fix_lagrit.py       # 通用修复脚本
├── rebuild_lagrit.py             # 重新编译脚本
├── start_lagrit.bat              # 主启动脚本
├── test_lagrit.bat               # 测试脚本
├── diagnose.bat                  # 诊断脚本
├── setup_env.bat                 # 环境变量设置
├── build/                        # 构建目录
│   └── lagrit.exe               # LaGriT可执行文件
├── src/                          # 源代码目录
└── WINDOWS_GUIDE.md              # 本指南
```

## 📚 更多资源

- [LaGriT官方文档](https://lanl.github.io/LaGriT/)
- [GitHub仓库](https://github.com/lanl/LaGriT)
- [问题报告](https://github.com/lanl/LaGriT/issues)

## ⚠️ 重要提示

1. **统一使用Python脚本**: 避免混用不同类型的脚本
2. **conda环境**: 确保在lagrit-env环境中运行
3. **MSYS2依赖**: 不要删除C:/msys64目录
4. **路径问题**: 确保在LaGriT项目根目录下运行脚本