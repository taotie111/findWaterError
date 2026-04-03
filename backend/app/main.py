#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
水体问题智能检测平台 - FastAPI 应用入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
import yaml
from pathlib import Path

from app.api import detect, models, images, stats, health
from app.db.database import init_db

# 加载配置
def load_config():
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

config = load_config()

# 创建 FastAPI 应用
app = FastAPI(
    title="水体问题智能检测平台",
    description="基于深度学习的多模型水体问题检测系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config['cors']['allow_origins'],
    allow_credentials=config['cors']['allow_credentials'],
    allow_methods=config['cors']['allow_methods'],
    allow_headers=config['cors']['allow_headers'],
)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory=config['storage']['upload_dir']), name="uploads")
app.mount("/outputs", StaticFiles(directory=config['storage']['output_dir']), name="outputs")

# 注册路由
app.include_router(detect.router, prefix="/api/detect", tags=["检测"])
app.include_router(models.router, prefix="/api/models", tags=["模型管理"])
app.include_router(images.router, prefix="/api/images", tags=["图像管理"])
app.include_router(stats.router, prefix="/api/stats", tags=["统计分析"])
app.include_router(health.router, prefix="/api", tags=["健康检查"])

# 生命周期事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("=" * 80)
    logger.info("水体问题智能检测平台 启动中...")
    logger.info("=" * 80)
    
    # 初始化数据库
    init_db()
    logger.info("✅ 数据库初始化完成")
    
    # 创建必要的目录
    for dir_name in ['upload_dir', 'output_dir', 'models_dir']:
        dir_path = Path(config['storage'][dir_name])
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ 目录已创建：{dir_path}")
    
    logger.info("=" * 80)
    logger.info(f"🚀 服务启动成功！")
    logger.info(f"📍 访问地址：http://{config['server']['host']}:{config['server']['port']}")
    logger.info(f"📚 API 文档：http://{config['server']['host']}:{config['server']['port']}/docs")
    logger.info("=" * 80)

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    logger.info("👋 正在关闭服务...")

# 根路径
@app.get("/")
async def root():
    return {
        "message": "欢迎使用水体问题智能检测平台",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=config['server']['host'],
        port=config['server']['port'],
        workers=config['server']['workers'],
        reload=config['server']['reload']
    )
