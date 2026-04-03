@echo off
REM 水体问题检测平台 - 后端启动脚本

echo ============================================================
echo 水体问题智能检测平台 - 后端服务
echo ============================================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [1/3] 检查依赖...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [信息] 正在安装依赖...
    pip install -r requirements.txt
) else (
    echo [OK] 依赖已安装
)

echo.
echo [2/3] 创建必要目录...
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs
if not exist "models" mkdir models
echo [OK] 目录已创建

echo.
echo [3/3] 启动服务...
echo ============================================================
echo 访问地址：http://localhost:8000
echo API 文档：http://localhost:8000/docs
echo ============================================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
