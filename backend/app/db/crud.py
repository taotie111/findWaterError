#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库 CRUD 操作
"""

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import yaml
import json
from datetime import datetime
from typing import Optional, List, Dict

from app.db.database import engine, Base
from app.models.detection import DetectionRecord

# 创建 Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_detection_record(
    image_path: str,
    image_name: str,
    model_name: str,
    results: List[Dict]
) -> int:
    """
    创建检测记录
    
    Args:
        image_path: 图像路径
        image_name: 图像名称
        model_name: 模型名称
        results: 检测结果
        
    Returns:
        记录 ID
    """
    db = SessionLocal()
    
    try:
        # 统计信息
        total_objects = len(results)
        category_counts = {}
        
        for det in results:
            class_name = det['class_name']
            category_counts[class_name] = category_counts.get(class_name, 0) + 1
        
        # 创建记录
        record = DetectionRecord(
            image_path=image_path,
            image_name=image_name,
            model_name=model_name,
            results=results,
            total_objects=total_objects,
            category_counts=category_counts
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return record.id
        
    finally:
        db.close()


def get_detection_record(record_id: int) -> Optional[Dict]:
    """
    获取检测记录
    
    Args:
        record_id: 记录 ID
        
    Returns:
        记录字典
    """
    db = SessionLocal()
    
    try:
        record = db.query(DetectionRecord).filter(DetectionRecord.id == record_id).first()
        
        if record:
            return {
                'id': record.id,
                'image_path': record.image_path,
                'image_name': record.image_name,
                'model_name': record.model_name,
                'created_at': record.created_at.isoformat() if record.created_at else None,
                'results': record.results,
                'total_objects': record.total_objects,
                'category_counts': record.category_counts
            }
        
        return None
        
    finally:
        db.close()


def get_detection_history(
    limit: int = 100,
    offset: int = 0,
    model_name: Optional[str] = None
) -> List[Dict]:
    """
    获取检测历史
    
    Args:
        limit: 返回数量限制
        offset: 偏移量
        model_name: 模型名称筛选（可选）
        
    Returns:
        记录列表
    """
    db = SessionLocal()
    
    try:
        query = db.query(DetectionRecord)
        
        if model_name:
            query = query.filter(DetectionRecord.model_name == model_name)
        
        query = query.order_by(DetectionRecord.created_at.desc())
        query = query.offset(offset).limit(limit)
        
        records = query.all()
        
        return [
            {
                'id': r.id,
                'image_name': r.image_name,
                'model_name': r.model_name,
                'created_at': r.created_at.isoformat() if r.created_at else None,
                'total_objects': r.total_objects
            }
            for r in records
        ]
        
    finally:
        db.close()


def delete_detection_record(record_id: int) -> bool:
    """
    删除检测记录
    
    Args:
        record_id: 记录 ID
        
    Returns:
        是否删除成功
    """
    db = SessionLocal()
    
    try:
        record = db.query(DetectionRecord).filter(DetectionRecord.id == record_id).first()
        
        if record:
            db.delete(record)
            db.commit()
            return True
        
        return False
        
    finally:
        db.close()


def get_stats_summary() -> Dict:
    """获取统计摘要"""
    db = SessionLocal()
    
    try:
        # 总检测数
        total_detections = db.query(DetectionRecord).count()
        
        # 总目标数
        total_objects = db.query(DetectionRecord).with_entities(
            func.sum(DetectionRecord.total_objects)
        ).scalar() or 0
        
        # 按模型统计
        models_stats = db.query(
            DetectionRecord.model_name,
            func.count(DetectionRecord.id)
        ).group_by(DetectionRecord.model_name).all()
        
        return {
            'total_detections': total_detections,
            'total_objects': total_objects,
            'by_model': dict(models_stats)
        }
        
    finally:
        db.close()


# 导入 func
from sqlalchemy import func
