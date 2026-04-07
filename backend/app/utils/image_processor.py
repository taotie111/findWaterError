#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图像处理工具函数
"""

import aiofiles
from pathlib import Path
from typing import List, Dict
from loguru import logger
import uuid
from PIL import Image, ImageDraw, ImageFont
import yaml


def get_config():
    """获取配置文件"""
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


async def save_upload(file) -> Path:
    """
    保存上传的文件
    
    Args:
        file: FastAPI UploadFile
        
    Returns:
        保存的文件路径
    """
    config = get_config()
    
    # 创建上传目录
    upload_dir = Path(config['storage']['upload_dir'])
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成唯一文件名
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = upload_dir / unique_filename
    
    # 保存文件
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    logger.info(f"文件已保存：{file_path}")
    return file_path


def draw_detections(image_path: str, detections: List[Dict], output_path: str = None) -> Path:
    """
    绘制检测结果
    
    Args:
        image_path: 原始图像路径
        detections: 检测结果列表
        output_path: 输出路径（可选）
        
    Returns:
        输出图像路径
    """
    # 打开图像
    image = Image.open(image_path).convert('RGB')
    draw = ImageDraw.Draw(image)
    
    # 颜色映射（6 类水体问题）
    colors = {
        'garbage': (255, 0, 0),        # 红色
        'illegal_construction': (0, 255, 0),  # 绿色
        'illegal_discharge': (0, 0, 255),     # 蓝色
        'floating_debris': (255, 255, 0),     # 黄色
        'bank_damage': (255, 0, 255),         # 品红
        'other': (0, 255, 255)                # 青色
    }
    
    # 绘制每个检测框
    for det in detections:
        bbox = det['bbox']
        class_name = det['class_name']
        confidence = det['confidence']
        
        # 获取颜色
        color = colors.get(class_name, (255, 0, 0))  # 默认红色
        
        # 绘制边界框
        x_min, y_min = bbox['x_min'], bbox['y_min']
        x_max, y_max = bbox['x_max'], bbox['y_max']
        
        draw.rectangle([x_min, y_min, x_max, y_max], outline=color, width=2)
        
        # 绘制标签
        label = f"{class_name}: {confidence:.2f}"
        draw.text((x_min, y_min - 10), label, fill=color)
    
    # 保存结果
    if output_path is None:
        config = get_config()
        output_dir = Path(config['storage']['output_dir'])
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"result_{Path(image_path).stem}.jpg"
    else:
        output_path = Path(output_path)
    
    image.save(output_path, quality=95)
    logger.info(f"结果图像已保存：{output_path}")
    
    return output_path
