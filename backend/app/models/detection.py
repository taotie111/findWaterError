#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据模型 - 检测结果
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.db.database import Base


class DetectionRecord(Base):
    """检测结果记录表"""
    
    __tablename__ = "detections"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_path = Column(String, nullable=False, comment="图像路径")
    image_name = Column(String, nullable=False, comment="图像名称")
    model_name = Column(String, nullable=False, comment="使用的模型")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    
    # 检测结果（JSON 格式）
    results = Column(JSON, comment="检测结果")
    
    # 统计信息
    total_objects = Column(Integer, comment="目标总数")
    category_counts = Column(JSON, comment="各类别数量")
    
    def __repr__(self):
        return f"<DetectionRecord(id={self.id}, image={self.image_name})>"
