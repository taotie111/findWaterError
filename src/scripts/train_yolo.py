#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
YOLOv8 训练脚本
================
支持 YOLOv8/v10/SE 等多种 YOLO 模型训练

用法:
    python train_yolo.py --model yolov8m --epochs 100 --data data/annotations/data.yaml
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='YOLO 训练脚本')
    
    # 模型配置
    parser.add_argument('--model', type=str, default='yolov8m',
                       choices=['yolov8n', 'yolov8s', 'yolov8m', 'yolov8l', 'yolov8x',
                               'yolov10n', 'yolov10s', 'yolov10m', 'yolov10l', 'yolov10x'],
                       help='模型版本')
    
    # 训练配置
    parser.add_argument('--epochs', type=int, default=100, help='训练轮数')
    parser.add_argument('--imgsz', type=int, default=640, help='图像尺寸')
    parser.add_argument('--batch', type=int, default=16, help='批次大小')
    parser.add_argument('--device', type=str, default='0', help='GPU 设备')
    
    # 数据配置
    parser.add_argument('--data', type=str, default='data/annotations/data.yaml',
                       help='数据集配置文件')
    
    # 输出配置
    parser.add_argument('--project', type=str, default='runs/detect',
                       help='输出目录')
    parser.add_argument('--name', type=str, default='train',
                       help='实验名称')
    parser.add_argument('--exist-ok', action='store_true',
                       help='覆盖已有实验')
    
    # 优化配置
    parser.add_argument('--workers', type=int, default=8, help='数据加载线程数')
    parser.add_argument('--optimizer', type=str, default='SGD',
                       choices=['SGD', 'Adam', 'AdamW'],
                       help='优化器')
    parser.add_argument('--lr0', type=float, default=0.01, help='初始学习率')
    parser.add_argument('--lrf', type=float, default=0.01, help='最终学习率')
    
    # 增强配置
    parser.add_argument('--augment', action='store_true', default=True,
                       help='启用数据增强')
    parser.add_argument('--mosaic', type=float, default=1.0,
                       help='mosaic 增强概率')
    parser.add_argument('--mixup', type=float, default=0.0,
                       help='mixup 增强概率')
    
    # 其他
    parser.add_argument('--resume', type=str, default=None,
                       help='恢复训练的权重路径')
    parser.add_argument('--pretrained', action='store_true', default=True,
                       help='使用预训练权重')
    
    return parser.parse_args()


def train(args):
    """训练函数"""
    print("=" * 80)
    print("YOLO 训练开始")
    print("=" * 80)
    print(f"\n[时间] {datetime.now()}")
    
    # 打印配置
    print(f"\n[配置]")
    print(f"  模型：{args.model}")
    print(f"  数据集：{args.data}")
    print(f"  训练轮数：{args.epochs}")
    print(f"  图像尺寸：{args.imgsz}")
    print(f"  批次大小：{args.batch}")
    print(f"  设备：{args.device}")
    print(f"  输出目录：{args.project}/{args.name}")
    print(f"  学习率：{args.lr0} -> {args.lrf}")
    print(f"  优化器：{args.optimizer}")
    print(f"  数据增强：mosaic={args.mosaic}, mixup={args.mixup}")
    print(f"  预训练权重：{'是' if args.pretrained else '否'}")
    
    # 检查数据文件
    data_path = Path(args.data)
    if not data_path.exists():
        print(f"\n[错误] 数据配置文件不存在：{data_path}")
        print(f"\n提示:")
        print(f"  1. 使用示例数据：sample_data/data.yaml")
        print(f"  2. 使用完整数据：data/annotations/data.yaml")
        print(f"  3. 运行数据迁移：python src/scripts/migrate_data.py")
        return
    
    print(f"\n[OK] 数据配置文件：{data_path}")
    
    # 加载模型
    print(f"\n[1/3] 加载模型...")
    if args.resume:
        print(f"  恢复训练：{args.resume}")
        model = YOLO(args.resume)
    else:
        model_name = f"{args.model}.pt" if not args.model.endswith('.pt') else args.model
        print(f"  模型：{model_name}")
        model = YOLO(model_name)
    
    # 开始训练
    print(f"\n[2/3] 开始训练...")
    print(f"  预计时间：{args.epochs * 0.5:.1f} 分钟 (RTX 3060)")
    
    results = model.train(
        # 数据配置
        data=args.data,
        
        # 训练配置
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        
        # 设备配置
        device=args.device,
        workers=args.workers,
        
        # 优化器配置
        optimizer=args.optimizer,
        lr0=args.lr0,
        lrf=args.lrf,
        
        # 输出配置
        project=args.project,
        name=args.name,
        exist_ok=args.exist_ok,
        
        # 数据增强
        augment=args.augment,
        mosaic=args.mosaic,
        mixup=args.mixup,
        
        # 其他
        pretrained=args.pretrained,
        verbose=True,
        save=True,
        save_period=-1,  # 只保存最后和最佳
    )
    
    # 训练完成
    print(f"\n[3/3] 训练完成!")
    print(f"\n[结果]")
    print(f"  最佳模型：{results.best}")
    print(f"  最后模型：{results.last}")
    print(f"  训练目录：{results.save_dir}")
    
    # 打印性能指标
    if hasattr(results, 'results_dict') and results.results_dict:
        print(f"\n[性能指标]")
        metrics = results.results_dict
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")
    
    print(f"\n{'='*80}")
    print("训练完成!")
    print(f"{'='*80}")
    
    return results


def main():
    """主函数"""
    args = parse_args()
    train(args)


if __name__ == "__main__":
    main()
