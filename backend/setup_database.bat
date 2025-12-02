@echo off
chcp 65001 >nul
echo ========================================
echo 科研管理系统 - 数据库初始化脚本
echo ========================================
echo.

echo 正在初始化数据库，请稍候...
python setup_database.py

if %errorlevel% equ 0 (
    echo.
    echo 数据库初始化成功！
    echo 请运行 start_backend.bat 启动后端服务
) else (
    echo.
    echo 数据库初始化失败，请检查错误信息
)

echo.
pause
