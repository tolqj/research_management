@echo off
chcp 65001 >nul
echo ========================================
echo 科研管理系统 - 后端服务启动脚本
echo ========================================
echo.

echo 正在启动后端服务...
echo 服务地址: http://localhost:8000
echo API文档: http://localhost:8000/api/docs
echo.

python main.py

pause
