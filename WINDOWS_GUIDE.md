# LaGriT Windows 使用指南

## 快速开始

1. 双击运行 `activate_lagrit.bat` 激活环境
2. 在打开的命令行中输入 `lagrit` 启动程序
3. 在 LaGriT 中输入 `test` 运行测试
4. 输入 `finish` 退出程序

## 如何重新编译

当您修改了 `src/` 目录中的源代码后，可以按照以下步骤快速重新编译，而无需完整地重新安装。

1.  **激活编译环境**: 双击运行项目根目录下的 `activate_lagrit.bat` 文件。
2.  **执行编译命令**: 在新打开的命令行窗口中，直接运行以下命令即可：
    ```bash
    mingw32-make -C build
    ```
    该命令会自动检测代码变更并仅编译被修改的部分，非常高效。

## 文件说明

- `lagrit.exe`: LaGriT 主程序
- `activate_lagrit.bat`: 环境激活脚本
- `setup_env.bat`: 环境变量设置脚本
- `build/`: 构建输出目录

## 故障排除

### 如果遇到编译错误:
1. 确保 MSYS2 正确安装
2. 检查编译器是否在 PATH 中
3. 重新运行安装脚本

### 如果 LaGriT 无法启动:
1. 检查 `lagrit.exe` 是否存在
2. 确保所有 DLL 依赖项可用
3. 在 MSYS2 环境中测试

### PyLaGriT 使用注意:
- PyLaGriT 在 Windows 上支持有限
- 建议在 WSL 或 Linux 环境中使用
- 如需在 Windows 使用，可考虑使用 Docker

## 更多资源

- [LaGriT 官方文档](https://lanl.github.io/LaGriT/)
- [GitHub 仓库](https://github.com/lanl/LaGriT)
- [问题报告](https://github.com/lanl/LaGriT/issues)