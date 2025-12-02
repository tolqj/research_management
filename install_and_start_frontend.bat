@echo off
chcp 65001 >nul
echo ========================================
echo 科研管理系统 - 前端安装并启动
echo ========================================
echo.

cd /d "e:\qoder\科研管理系统\frontend"

echo [1/2] 检查并安装依赖...
if not exist "node_modules" (
    echo 正在安装 npm 依赖...
    call npm install
) else (
    echo 依赖已安装，跳过安装步骤
)

echo.
echo [2/2] 启动前端服务...
echo 服务地址: http://localhost:5173
echo.

call npm run dev

pause
