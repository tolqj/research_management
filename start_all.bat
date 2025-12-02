@echo off
chcp 65001 >nul
echo.
echo ========================================
echo  科研管理系统 - 一键启动脚本
echo ========================================
echo.

echo 正在启动系统，请稍候...
echo.

:: 启动后端服务
echo [1/2] 启动后端服务...
cd backend
start "RMS Backend" cmd /k "python main.py"
cd ..
echo ✓ 后端服务已启动 (http://localhost:8000)
echo.

:: 等待 2 秒
timeout /t 2 /nobreak >nul

:: 启动前端服务
echo [2/2] 启动前端服务...
cd frontend
start "RMS Frontend" cmd /k "npm run dev"
cd ..
echo ✓ 前端服务已启动 (http://localhost:5173)
echo.

echo ========================================
echo  系统启动完成！
echo ========================================
echo.
echo 后端地址: http://localhost:8000
echo API文档: http://localhost:8000/api/docs
echo 前端地址: http://localhost:5173
echo.
echo 默认账号: admin / admin123
echo.
echo 提示: 两个窗口将保持运行，关闭窗口即停止服务
echo ========================================
echo.

pause
