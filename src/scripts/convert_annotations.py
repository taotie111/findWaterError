#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
标注格式转换工具
支持 LabelMe JSON、VOC XML、COCO JSON 转 YOLO 格式
"""

import json
import xml.etree.ElementTree as ET
import argparse
from pathlib import Path
from PIL import Image


def label_to_id(label):
    """类别名称转 ID"""
    label_map = {
        'garbage': 0,
        'illegal_construction': 1,
        'illegal_construction': 1,
        'illegal_discharge': 2,
        'floating_debris': 3,
        'bank_damage': 4,
        'other': 5
    }
    return label_map.get(label.lower().strip(), 5)


def convert_labelme_to_yolo(json_file, output_dir):
    """将 LabelMe JSON 转换为 YOLO 格式"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 获取图像尺寸
    img_width = data.get('imageWidth', 1920)
    img_height = data.get('imageHeight', 1080)
    
    output_file = Path(output_dir) / Path(json_file).stem + '.txt'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for shape in data.get('shapes', []):
            label = shape.get('label', 'other')
            shape_type = shape.get('shape_type', 'rectangle')
            points = shape.get('points', [])
            
            if len(points) == 0:
                continue
            
            class_id = label_to_id(label)
            
            if shape_type == 'rectangle' and len(points) == 2:
                # 矩形框
                x_min = min(points[0][0], points[1][0])
                y_min = min(points[0][1], points[1][1])
                x_max = max(points[0][0], points[1][0])
                y_max = max(points[0][1], points[1][1])
            else:
                # 多边形，计算边界框
                x_min = min(p[0] for p in points)
                y_min = min(p[1] for p in points)
                x_max = max(p[0] for p in points)
                y_max = max(p[1] for p in points)
            
            # 转换为 YOLO 格式（归一化）
            x_center = (x_min + x_max) / 2 / img_width
            y_center = (y_min + y_max) / 2 / img_height
            width = (x_max - x_min) / img_width
            height = (y_max - y_min) / img_height
            
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
    
    print(f"✓ 转换完成：{json_file.name} → {output_file.name}")


def convert_voc_to_yolo(xml_file, output_dir):
    """将 VOC XML 转换为 YOLO 格式"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # 获取图像尺寸
    size = root.find('size')
    img_width = int(size.find('width').text)
    img_height = int(size.find('height').text)
    
    output_file = Path(output_dir) / Path(xml_file).stem + '.txt'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for obj in root.findall('object'):
            label = obj.find('name').text
            bbox = obj.find('bndbox')
            
            x_min = float(bbox.find('xmin').text)
            y_min = float(bbox.find('ymin').text)
            x_max = float(bbox.find('xmax').text)
            y_max = float(bbox.find('ymax').text)
            
            class_id = label_to_id(label)
            
            x_center = (x_min + x_max) / 2 / img_width
            y_center = (y_min + y_max) / 2 / img_height
            width = (x_max - x_min) / img_width
            height = (y_max - y_min) / img_height
            
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
    
    print(f"✓ 转换完成：{xml_file.name} → {output_file.name}")


def convert_coco_to_yolo(json_file, output_dir):
    """将 COCO JSON 转换为 YOLO 格式"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 创建图像 ID 到文件名的映射
    img_id_to_file = {img['id']: img['file_name'] for img in data.get('images', [])}
    
    # 创建类别映射
    cat_id_to_name = {cat['id']: cat['name'] for cat in data.get('categories', [])}
    
    # 按图像分组标注
    img_annotations = {}
    for ann in data.get('annotations', []):
        img_id = ann['image_id']
        if img_id not in img_annotations:
            img_annotations[img_id] = []
        img_annotations[img_id].append(ann)
    
    # 转换每个图像的标注
    for img_id, annotations in img_annotations.items():
        img_file = img_id_to_file.get(img_id, f'{img_id}.jpg')
        
        # 获取图像尺寸
        img_info = next((img for img in data['images'] if img['id'] == img_id), None)
        if not img_info:
            continue
        
        img_width = img_info.get('width', 1920)
        img_height = img_info.get('height', 1080)
        
        output_file = Path(output_dir) / Path(img_file).stem + '.txt'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for ann in annotations:
                bbox = ann.get('bbox', [])
                if len(bbox) != 4:
                    continue
                
                # COCO bbox: [x_min, y_min, width, height]
                x_min, y_min, w, h = bbox
                
                cat_id = ann.get('category_id', 0)
                cat_name = cat_id_to_name.get(cat_id, 'other')
                class_id = label_to_id(cat_name)
                
                # 转换为 YOLO 格式
                x_center = (x_min + w / 2) / img_width
                y_center = (y_min + h / 2) / img_height
                width = w / img_width
                height = h / img_height
                
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        print(f"✓ 转换完成：{img_file}")


def batch_convert(input_dir, output_dir, format_type):
    """批量转换"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if format_type == 'labelme':
        files = list(input_path.glob('*.json'))
        convert_func = convert_labelme_to_yolo
    elif format_type == 'voc':
        files = list(input_path.glob('*.xml'))
        convert_func = convert_voc_to_yolo
    elif format_type == 'coco':
        files = [input_path]  # COCO 是单个 JSON 文件
        convert_func = lambda f, o: convert_coco_to_yolo(f, o)
    else:
        print(f"❌ 不支持的格式：{format_type}")
        return
    
    print(f"\n开始批量转换 {len(files)} 个文件...")
    for file in files:
        try:
            convert_func(file, output_path)
        except Exception as e:
            print(f"❌ 转换失败 {file.name}: {e}")
    
    print(f"\n✅ 批量转换完成！输出目录：{output_path}")


def main():
    parser = argparse.ArgumentParser(description='标注格式转换工具')
    parser.add_argument('--input', type=str, required=True, help='输入文件或目录')
    parser.add_argument('--output', type=str, required=True, help='输出目录')
    parser.add_argument('--format', type=str, choices=['labelme', 'voc', 'coco'], 
                       required=True, help='输入格式')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if input_path.is_dir():
        # 批量转换
        batch_convert(args.input, args.output, args.format)
    else:
        # 单个文件转换
        if args.format == 'labelme':
            convert_labelme_to_yolo(input_path, args.output)
        elif args.format == 'voc':
            convert_voc_to_yolo(input_path, args.output)
        elif args.format == 'coco':
            convert_coco_to_yolo(input_path, args.output)


if __name__ == '__main__':
    main()
