#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
统一训练入口
==============
一键选择并训练模型

用法:
    python train.py --model yolov8    # 训练 YOLOv8
    python train.py --model dinov2    # 训练 DINOv2
    python train.py --list            # 列出所有可用模型
"""

import sys
import argparse
import subprocess
from pathlib import Path

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')


AVAILABLE_MODELS = {
    'yolov8': {
        'script': 'train_yolo.py',
        'description': 'YOLOv8 目标检测',
        'default_args': ['--model', 'yolov8m', '--epochs', '100']
    },
    'yolov10': {
        'script': 'train_yolo.py',
        'description': 'YOLOv10 目标检测（最新）',
        'default_args': ['--model', 'yolov10m', '--epochs', '100']
    },
    'dinov2': {
        'script': 'train_dinov2.py',
        'description': 'DINOv2 图像分类',
        'default_args': ['--model', 'dinov2-large', '--epochs', '20']
    }
}


def list_models():
    """列出所有可用模型"""
    print("=" * 80)
    print("可用模型列表")
    print("=" * 80)
    print()
    
    for model_id, info in AVAILABLE_MODELS.items():
        print(f"  {model_id:12} - {info['description']}")
        print(f"               默认参数：{' '.join(info['default_args'])}")
        print()
    
    print("=" * 80)
    print("使用示例:")
    print("  python train.py --model yolov8 --epochs 50")
    print("  python train.py --model dinov2 --data data/processed")
    print("=" * 80)


def train_model(model_id, extra_args):
    """训练指定模型"""
    if model_id not in AVAILABLE_MODELS:
        print(f"[错误] 未知模型：{model_id}")
        print(f"\n可用模型：{', '.join(AVAILABLE_MODELS.keys())}")
        print(f"\n使用 --list 查看所有模型")
        return
    
    # 获取模型配置
    model_info = AVAILABLE_MODELS[model_id]
    script = model_info['script']
    script_path = Path(__file__).parent / script
    
    if not script_path.exists():
        print(f"[错误] 训练脚本不存在：{script_path}")
        return
    
    # 构建命令
    cmd = [sys.executable, str(script_path)]
    
    # 添加默认参数
    cmd.extend(model_info['default_args'])
    
    # 添加额外参数
    if extra_args:
        cmd.extend(extra_args)
    
    print("=" * 80)
    print(f"训练 {model_id}")
    print("=" * 80)
    print(f"\n命令：{' '.join(cmd)}\n")
    
    # 执行训练
    try:
        subprocess.run(cmd, check=True)
        print("\n[OK] 训练完成!")
    except subprocess.CalledProcessError as e:
        print(f"\n[错误] 训练失败：{e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[中断] 训练已中断")
        sys.exit(0)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='统一训练入口',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python train.py --list                    # 列出所有模型
  python train.py --model yolov8            # 训练 YOLOv8
  python train.py --model yolov8 --epochs 50  # 训练 50 轮
  python train.py --model dinov2            # 训练 DINOv2
        """
    )
    
    parser.add_argument('--model', type=str,
                       help='模型名称 (yolov8/yolov10/dinov2)')
    parser.add_argument('--list', action='store_true',
                       help='列出所有可用模型')
    
    # 传递其他参数
    args, extra_args = parser.parse_known_args()
    
    return args, extra_args


def main():
    """主函数"""
    args, extra_args = parse_args()
    
    if args.list:
        list_models()
        return
    
    if not args.model:
        print("[错误] 请指定模型名称")
        print("\n使用 --list 查看所有模型")
        print("或使用 --help 查看帮助")
        return
    
    train_model(args.model, extra_args)


if __name__ == "__main__":
    main()
