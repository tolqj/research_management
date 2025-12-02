@echo off
chcp 65001 >nul
echo ========================================
echo 科研管理系统 - 前端启动脚本
echo ========================================
echo.

cd frontend

echo 正在启动前端服务...
echo 服务地址: http://localhost:5173
echo.

npm run dev

pause
