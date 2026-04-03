@echo off
REM 水体问题检测平台 - 前端启动脚本

echo ============================================================
echo 水体问题智能检测平台 - 前端服务
echo ============================================================
echo.

REM 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)

echo [1/3] 检查依赖...
if not exist "node_modules" (
    echo [信息] 正在安装依赖...
    call npm install
) else (
    echo [OK] 依赖已安装
)

echo.
echo [2/3] 启动开发服务器...
echo ============================================================
echo 访问地址：http://localhost:5173
echo API 代理：http://localhost:8000
echo ============================================================
echo.

call npm run dev

pause
