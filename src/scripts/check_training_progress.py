#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
查看训练进度
"""

import json
from pathlib import Path
from datetime import datetime

log_file = Path(r"H:\code\01_image_center\runs\finetune\training_log.json")

print("=" * 80)
print("训练进度监控")
print("=" * 80)
print(f"\n检查时间：{datetime.now()}")

if not log_file.exists():
    print(f"\n[WAIT] 训练日志文件不存在")
    print(f"   可能还在第一轮次训练中...")
    print(f"   文件位置：{log_file}")
    print(f"\n预计每轮时间：45-60 分钟")
    print(f"开始时间：17:37")
    print(f"预计 Epoch 1 完成：18:22-18:37")
else:
    print(f"\n[OK] 找到日志文件：{log_file}")
    
    with open(log_file, 'r', encoding='utf-8') as f:
        logs = json.load(f)
    
    print(f"\n已完成轮次：{len(logs)} / 20")
    
    if logs:
        latest = logs[-1]
        print(f"\n[最新轮次] Epoch {latest['epoch']}")
        print(f"  训练损失：{latest['train_loss']:.4f}")
        print(f"  训练准确率：{latest['train_acc']:.2f}%")
        print(f"  验证准确率：{latest['val_acc']:.2f}%")
        print(f"  用时：{latest['time']:.1f} 分钟")
        
        # 显示进度
        progress = len(logs) / 20 * 100
        print(f"\n进度：{progress:.1f}% ({len(logs)}/20)")
        
        # 估算剩余时间
        avg_time = sum(log['time'] for log in logs) / len(logs)
        remaining = (20 - len(logs)) * avg_time
        print(f"平均每轮：{avg_time:.1f} 分钟")
        print(f"预计剩余：{remaining:.1f} 分钟 ({remaining/60:.1f} 小时)")
        
        # 显示所有轮次
        print(f"\n{'='*80}")
        print("所有轮次详情:")
        print(f"{'='*80}")
        print(f"{'Epoch':<8} {'训练损失':<12} {'训练准确率':<12} {'验证准确率':<12} {'用时 (分钟)'}")
        print("-" * 80)
        for log in logs:
            print(f"{log['epoch']:<8} {log['train_loss']:<12.4f} {log['train_acc']:<12.2f}% {log['val_acc']:<12.2f}% {log['time']:<12.1f}")

print(f"\n{'='*80}")
print("模型文件位置：H:\\code\\01_image_center\\runs\\finetune\\best_model.pth")
print(f"{'='*80}")
