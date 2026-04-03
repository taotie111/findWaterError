@echo off
chcp 65001 >nul
echo ========================================
echo 查看训练进度
echo ========================================
echo.

cd /d H:\code\01_image_center\runs\finetune

if exist training_log.json (
    echo 训练日志文件：training_log.json
    echo.
    type training_log.json | findstr /c:"epoch" /c:"val_acc"
    echo.
    echo ========================================
    echo 最新轮次信息：
    powershell -Command "Get-Content training_log.json -Tail 20"
) else (
    echo 训练日志文件不存在
    echo 可能还在第一轮次训练中...
)

echo.
echo ========================================
echo 模型文件：
dir *.pth 2>nul || echo 暂无模型文件

echo.
pause
