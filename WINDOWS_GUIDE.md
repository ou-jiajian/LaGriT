# LaGriT Windows 使用指南

## 一键安装环境

### 系统要求
- Windows 10/11 (64位)
- 至少 4GB 可用磁盘空间
- 管理员权限（用于安装 MSYS2）

### 安装步骤
1. **克隆或下载项目**
   ```powershell
   git clone https://github.com/lanl/LaGriT.git C:\Project\LaGriT
   cd C:\Project\LaGriT
   ```

2. **运行一键安装脚本**
   ```powershell
   python install_lagrit_windows.py
   ```

   脚本将自动完成：
   - 检查系统环境
   - 安装/配置 MSYS2 和编译工具
   - 创建 conda 环境
   - 修复源代码兼容性问题
   - 编译 LaGriT 可执行文件
   - 安装 PyLaGriT
   - 生成激活脚本

3. **验证安装**
   ```powershell
   .\test.ps1
   ```

## 安装状态
- **LaGriT 版本**: V3.3.4 Windows
- **安装位置**: `C:\Project\LaGriT\build\lagrit.exe`
- **Conda 环境**: `lagrit-env`
- **PyLaGriT**: 已安装

## 快速启动

### 方法1: PowerShell 脚本（推荐）
```powershell
.\activate_lagrit.ps1
```

### 方法2: 手动设置
```powershell
# 激活环境
conda activate lagrit-env
$env:PATH = "C:\msys64\mingw64\bin;C:\Project\LaGriT\build;$env:PATH"
$env:MSYS2_PATH_TYPE = "inherit"

# 启动 LaGriT
lagrit
```

### 方法3: 直接运行
```powershell
conda activate lagrit-env
$env:PATH = "C:\msys64\mingw64\bin;$env:PATH"
$env:MSYS2_PATH_TYPE = "inherit"
C:\Project\LaGriT\build\lagrit.exe
```

## 项目目录结构

```
C:\Project\LaGriT\
├── 📁 核心文件
│   ├── install_lagrit_windows.py    # 主安装脚本
│   ├── activate_lagrit.ps1          # 环境激活脚本
│   ├── test.ps1                     # 安装测试脚本
│   └── WINDOWS_GUIDE.md             # 本使用指南
│
├── 📁 文档说明
│   ├── README.md                    # 英文说明文档
│   ├── README_CN.md                 # 中文说明文档
│   ├── CONTRIBUTING.md              # 贡献指南
│   └── LICENSE.md                   # 许可证
│
├── 📁 构建输出
│   └── build/
│       ├── lagrit.exe               # LaGriT 可执行文件
│       ├── liblagrit.a              # 静态库文件
│       └── *.mod                    # Fortran 模块文件
│
├── 📁 源代码
│   ├── src/                         # LaGriT 源代码
│   │   ├── lagrit_main.f            # 主程序
│   │   ├── *.f, *.c, *.cpp          # 源文件
│   │   └── *.h                      # 头文件
│   └── lg_util/                     # 工具库
│       └── src/                     # 工具源代码
│
├── 📁 Python 集成
│   └── PyLaGriT/                    # Python 接口
│       ├── pylagrit/                # Python 包
│       ├── examples/                # 示例代码
│       ├── tests/                   # 测试文件
│       └── setup.py                 # 安装脚本
│
├── 📁 测试和示例
│   ├── test/                        # 测试套件
│   │   ├── level01/                 # 基础测试
│   │   ├── level02/                 # 中级测试
│   │   └── level03/                 # 高级测试
│   └── examples/                    # 使用示例
│
├── 📁 构建配置
│   ├── CMakeLists.txt               # CMake 配置
│   ├── cmake/                       # CMake 模块
│   ├── environment-windows.yml     # Conda 环境配置
│   └── Makefile                     # Make 配置
│
└── 📁 文档和资源
    ├── docs/                        # 在线文档
    ├── documentation/               # 详细文档
    └── screenshots/                 # 截图资源
```

## 基本操作

### LaGriT 常用命令
| 命令 | 说明 | 示例 |
|------|------|------|
| `help` | 显示帮助 | `help` |
| `test` | 运行测试 | `test` |
| `cmo/create` | 创建网格对象 | `cmo/create/quad` |
| `createpts` | 创建点 | `createpts/xyz/5,5,1/0.,0.,0./1.,1.,0.` |
| `connect` | 连接生成网格 | `connect` |
| `dump` | 保存文件 | `dump/gmv/test.gmv` |
| `read` | 读取文件 | `read/avs/input.inp` |
| `finish` | 退出程序 | `finish` |

### 快速示例
```
# 在 LaGriT 中依次输入：
cmo/create/quad
createpts/xyz/5,5,1/0.,0.,0./1.,1.,0.
connect
dump/gmv/test.gmv
finish
```

## Python 集成

激活环境后可使用 PyLaGriT：
```python
import pylagrit
# 使用 PyLaGriT 功能
```

## 故障排除

### 常见问题
1. **找不到 lagrit 命令**: 确保设置了正确的 PATH
2. **缺少动态库**: 确保 MSYS2 路径在 PATH 中
3. **conda 环境问题**: 重新激活 `lagrit-env`

### 重新安装
```powershell
python install_lagrit_windows.py
```

## 更多资源

- **官方文档**: https://lagrit.lanl.gov
- **GitHub**: https://github.com/lanl/LaGriT
- **在线手册**: https://lagrit.lanl.gov/manual/

---
🎉 **LaGriT 已成功安装，开始您的网格生成之旅！**
