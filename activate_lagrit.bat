@echo off
chcp 65001 > nul
echo 激活 LaGriT 环境...

call setup_env.bat

call conda activate lagrit-env

set "PATH=C:\Project\LaGriT\build;%PATH%"

echo LaGriT 环境已激活
echo 可以运行以下命令:
echo   lagrit        - 启动 LaGriT
echo   python        - 启动 Python
echo.
cmd /k