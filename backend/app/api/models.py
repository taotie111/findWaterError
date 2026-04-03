#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模型管理 API 路由
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.model_manager import model_manager

router = APIRouter()


@router.get("/")
async def get_models():
    """获取可用模型列表"""
    available_models = []
    
    for model in model_manager.config['model']['available_models']:
        available_models.append({
            'name': model['name'],
            'type': model['type'],
            'enabled': model.get('enabled', True),
            'loaded': model['name'] in model_manager.loaded_models,
            'is_active': model['name'] == model_manager.active_model
        })
    
    return JSONResponse(content={
        "success": True,
        "models": available_models,
        "active_model": model_manager.active_model
    })


@router.post("/switch")
async def switch_model(model_name: str):
    """
    切换活动模型
    
    Args:
        model_name: 模型名称
    """
    success = model_manager.switch_model(model_name)
    
    if not success:
        raise HTTPException(status_code=400, detail=f"切换模型失败：{model_name}")
    
    return JSONResponse(content={
        "success": True,
        "message": f"已切换到模型：{model_name}",
        "active_model": model_name
    })


@router.get("/status")
async def get_model_status():
    """获取模型状态"""
    status = model_manager.get_status()
    
    return JSONResponse(content={
        "success": True,
        "status": status
    })


@router.post("/load")
async def load_model(model_name: str):
    """
    加载模型
    
    Args:
        model_name: 模型名称
    """
    success = model_manager.load_model(model_name)
    
    if not success:
        raise HTTPException(status_code=400, detail=f"加载模型失败：{model_name}")
    
    return JSONResponse(content={
        "success": True,
        "message": f"模型 {model_name} 加载成功"
    })


@router.post("/unload")
async def unload_model(model_name: str):
    """
    卸载模型
    
    Args:
        model_name: 模型名称
    """
    success = model_manager.unload_model(model_name)
    
    if not success:
        raise HTTPException(status_code=400, detail=f"卸载模型失败：{model_name}")
    
    return JSONResponse(content={
        "success": True,
        "message": f"模型 {model_name} 卸载成功"
    })
