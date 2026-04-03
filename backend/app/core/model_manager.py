#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模型管理器 - 负责模型的加载、推理和管理
"""

import torch
from pathlib import Path
from typing import List, Dict, Any
from loguru import logger
import yaml

try:
    from ultralytics import YOLO
except ImportError:
    logger.warning("Ultralytics 未安装，YOLO 模型将不可用")

try:
    from transformers import Dinov2Model
except ImportError:
    logger.warning("Transformers 未安装，DINOv2 模型将不可用")


class ModelManager:
    """模型管理器"""
    
    def __init__(self, config_path: str = None):
        """
        初始化模型管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or Path(__file__).parent.parent / "config.yaml"
        self.config = self._load_config()
        
        # 已加载的模型
        self.loaded_models: Dict[str, Any] = {}
        
        # 当前活动模型
        self.active_model = self.config['model']['default_model']
        
        # 设备
        self.device = torch.device(f'cuda:{self.config["inference"]["gpu_id"]}' 
                                   if torch.cuda.is_available() else 'cpu')
        
        logger.info(f"🚀 模型管理器初始化完成")
        logger.info(f"💻 使用设备：{self.device}")
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def load_model(self, model_name: str) -> bool:
        """
        加载模型
        
        Args:
            model_name: 模型名称
            
        Returns:
            是否加载成功
        """
        if model_name in self.loaded_models:
            logger.info(f"模型 {model_name} 已加载")
            return True
        
        # 查找模型配置
        model_config = None
        for model in self.config['model']['available_models']:
            if model['name'] == model_name:
                model_config = model
                break
        
        if not model_config:
            logger.error(f"未找到模型配置：{model_name}")
            return False
        
        if not model_config.get('enabled', True):
            logger.warning(f"模型 {model_name} 已禁用")
            return False
        
        try:
            logger.info(f"正在加载模型：{model_name}...")
            
            if model_name.startswith('yolo'):
                # 加载 YOLO 模型
                model = YOLO(model_config['weights'])
                model.to(self.device)
                
            elif model_name == 'dinov2':
                # 加载 DINOv2 模型
                model = Dinov2Model.from_pretrained('facebook/dinov2-large')
                model.to(self.device)
                model.eval()
                
            else:
                logger.error(f"不支持的模型类型：{model_name}")
                return False
            
            self.loaded_models[model_name] = model
            logger.info(f"✅ 模型 {model_name} 加载成功")
            
            return True
            
        except Exception as e:
            logger.error(f"加载模型失败：{e}")
            return False
    
    def unload_model(self, model_name: str) -> bool:
        """
        卸载模型
        
        Args:
            model_name: 模型名称
            
        Returns:
            是否卸载成功
        """
        if model_name not in self.loaded_models:
            logger.warning(f"模型 {model_name} 未加载")
            return False
        
        try:
            # 清理 GPU 缓存
            if self.device.type == 'cuda':
                del self.loaded_models[model_name]
                torch.cuda.empty_cache()
            
            self.loaded_models.pop(model_name)
            logger.info(f"✅ 模型 {model_name} 已卸载")
            
            return True
            
        except Exception as e:
            logger.error(f"卸载模型失败：{e}")
            return False
    
    def switch_model(self, model_name: str) -> bool:
        """
        切换活动模型
        
        Args:
            model_name: 模型名称
            
        Returns:
            是否切换成功
        """
        if model_name not in self.loaded_models:
            logger.info(f"模型 {model_name} 未加载，尝试加载...")
            if not self.load_model(model_name):
                return False
        
        self.active_model = model_name
        logger.info(f"🔄 已切换到模型：{model_name}")
        
        return True
    
    def predict(self, image_path: str, model_name: str = None) -> List[Dict]:
        """
        推理预测
        
        Args:
            image_path: 图像路径
            model_name: 模型名称（可选，默认使用活动模型）
            
        Returns:
            检测结果列表
        """
        if model_name is None:
            model_name = self.active_model
        
        if model_name not in self.loaded_models:
            if not self.load_model(model_name):
                return []
        
        model = self.loaded_models[model_name]
        
        try:
            logger.debug(f"正在推理：{image_path}")
            
            if model_name.startswith('yolo'):
                # YOLO 模型推理
                results = model.predict(
                    image_path,
                    conf=self.config['inference']['conf_threshold'],
                    iou=self.config['inference']['iou_threshold'],
                    max_det=self.config['inference']['max_detections'],
                    imgsz=self.config['inference']['img_size'],
                    half=self.config['inference']['half_precision'] and self.device.type == 'cuda',
                    device=self.device,
                    verbose=False
                )
                
                # 解析结果
                return self._parse_yolo_results(results[0])
            
            elif model_name == 'dinov2':
                # DINOv2 推理（分类）
                return self._predict_dinov2(image_path, model)
            
            else:
                logger.error(f"不支持的模型：{model_name}")
                return []
                
        except Exception as e:
            logger.error(f"推理失败：{e}")
            return []
    
    def _parse_yolo_results(self, result) -> List[Dict]:
        """
        解析 YOLO 检测结果
        
        Args:
            result: YOLO 结果对象
            
        Returns:
            解析后的结果列表
        """
        detections = []
        
        boxes = result.boxes
        if boxes is None:
            return detections
        
        for i in range(len(boxes)):
            detection = {
                'class_id': int(boxes.cls[i]),
                'class_name': result.names[int(boxes.cls[i])],
                'confidence': float(boxes.conf[i]),
                'bbox': {
                    'x_min': float(boxes.xyxy[i][0]),
                    'y_min': float(boxes.xyxy[i][1]),
                    'x_max': float(boxes.xyxy[i][2]),
                    'y_max': float(boxes.xyxy[i][3])
                }
            }
            detections.append(detection)
        
        return detections
    
    def _predict_dinov2(self, image_path: str, model) -> List[Dict]:
        """
        DINOv2 推理（分类）
        
        Args:
            image_path: 图像路径
            model: DINOv2 模型
            
        Returns:
            分类结果
        """
        # TODO: 实现 DINOv2 分类逻辑
        # 这里需要加载分类头和类别映射
        logger.warning("DINOv2 推理尚未完全实现")
        return []
    
    def get_status(self) -> Dict:
        """
        获取模型状态
        
        Returns:
            状态信息
        """
        return {
            'active_model': self.active_model,
            'loaded_models': list(self.loaded_models.keys()),
            'device': str(self.device),
            'gpu_memory': self._get_gpu_memory() if self.device.type == 'cuda' else None
        }
    
    def _get_gpu_memory(self) -> Dict:
        """获取 GPU 显存使用情况"""
        if self.device.type != 'cuda':
            return None
        
        return {
            'allocated': torch.cuda.memory_allocated() / 1024**3,
            'reserved': torch.cuda.memory_reserved() / 1024**3,
            'total': torch.cuda.get_device_properties(0).total_memory / 1024**3
        }


# 全局模型管理器实例
model_manager = ModelManager()
