#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
健康检查和系统信息 API
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import torch
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/system/info")
async def get_system_info():
    """获取系统信息"""
    info = {
        "python_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
    }
    
    if torch.cuda.is_available():
        info["cuda_version"] = torch.version.cuda
        info["gpu_name"] = torch.cuda.get_device_name(0)
        info["gpu_memory_total"] = torch.cuda.get_device_properties(0).total_memory / 1024**3
        info["gpu_memory_allocated"] = torch.cuda.memory_allocated() / 1024**3
        info["gpu_memory_reserved"] = torch.cuda.memory_reserved() / 1024**3
    
    return JSONResponse(content={
        "success": True,
        "info": info
    })
