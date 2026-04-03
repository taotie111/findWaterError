#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库初始化
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
import yaml
from loguru import logger

# 加载配置
config_path = Path(__file__).parent.parent.parent / "config.yaml"
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 创建数据库引擎
engine = create_engine(
    config['database']['url'],
    connect_args={"check_same_thread": False}  # SQLite 需要
)

Base = declarative_base()


def init_db():
    """初始化数据库"""
    from app.models.detection import DetectionRecord
    
    Base.metadata.create_all(bind=engine)
    logger.info(f"数据库已初始化：{config['database']['url']}")
