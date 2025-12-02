@echo off
chcp 65001 >nul
echo ========================================
echo 科研管理系统 - 前端构建脚本
echo ========================================
echo.

cd frontend

echo 正在构建前端项目...
call npm run build

if %errorlevel% equ 0 (
    echo.
    echo ✓ 构建成功！
    echo 输出目录: frontend/dist
) else (
    echo.
    echo ✗ 构建失败，请检查错误信息
)

echo.
pause
