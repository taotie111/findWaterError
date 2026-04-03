#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
标注转换脚本 - 将漂浮物/塑料垃圾标注统一为 floating_debris 类别
"""

from pathlib import Path
import os

# 数据目录
DATA_DIR = Path(r"H:/code/01_image_center/data/annotations/yolo_format")

# 类别映射
# 原类别 6 (plastic_waste) → 新类别 3 (floating_debris)
OLD_TO_NEW = {
    6: 3,  # plastic_waste → floating_debris
}


def convert_label_file(label_path):
    """转换单个标注文件"""
    with open(label_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    converted = False
    
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 5:
            class_id = int(parts[0])
            
            # 转换类别 ID
            if class_id in OLD_TO_NEW:
                parts[0] = str(OLD_TO_NEW[class_id])
                converted = True
            
            new_lines.append(' '.join(parts) + '\n')
    
    if converted:
        with open(label_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False


def convert_all_labels():
    """转换所有标注文件"""
    print("=" * 80)
    print("开始转换标注文件...")
    print("=" * 80)
    
    total_files = 0
    converted_files = 0
    
    for split in ['train', 'val', 'test']:
        split_dir = DATA_DIR / split
        if not split_dir.exists():
            continue
        
        print(f"\n处理 {split} 集...")
        label_files = list(split_dir.glob("*.txt"))
        
        for label_file in label_files:
            total_files += 1
            if convert_label_file(label_file):
                converted_files += 1
    
    print("\n" + "=" * 80)
    print(f"转换完成！")
    print(f"  总文件数：{total_files}")
    print(f"  转换文件数：{converted_files}")
    print("=" * 80)


if __name__ == "__main__":
    convert_all_labels()
