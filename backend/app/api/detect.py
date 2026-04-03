#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检测 API 路由
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from fastapi.responses import JSONResponse
from pathlib import Path
import uuid
import shutil
from typing import List, Optional
from loguru import logger

from app.core.model_manager import model_manager
from app.utils.image_processor import save_upload, draw_detections
from app.db.crud import create_detection_record

router = APIRouter()


@router.post("/")
async def detect_single(
    image: UploadFile = File(..., description="待检测图像"),
    model_name: Optional[str] = Body(None, description="模型名称（可选）")
):
    """
    单张图像检测
    
    Args:
        image: 上传的图像文件
        model_name: 模型名称（可选，默认使用活动模型）
        
    Returns:
        检测结果
    """
    try:
        # 验证文件类型
        if not image.content_type or not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="请上传图像文件")
        
        # 保存上传图像
        image_path = save_upload(image)
        logger.info(f"图像已保存：{image_path}")
        
        # 推理检测
        results = model_manager.predict(str(image_path), model_name)
        logger.info(f"检测完成，发现 {len(results)} 个目标")
        
        # 绘制检测结果
        output_path = draw_detections(str(image_path), results)
        logger.info(f"结果图像已保存：{output_path}")
        
        # 保存到数据库
        record_id = create_detection_record(
            image_path=str(image_path),
            image_name=image.filename,
            model_name=model_name or model_manager.active_model,
            results=results
        )
        
        return JSONResponse(content={
            "success": True,
            "record_id": record_id,
            "image_path": str(image_path),
            "output_image": str(output_path),
            "results": results,
            "total_objects": len(results),
            "model_used": model_name or model_manager.active_model
        })
        
    except Exception as e:
        logger.error(f"检测失败：{e}")
        raise HTTPException(status_code=500, detail=f"检测失败：{str(e)}")


@router.post("/batch")
async def detect_batch(
    images: List[UploadFile] = File(..., description="待检测图像列表"),
    model_name: Optional[str] = Body(None, description="模型名称（可选）")
):
    """
    批量图像检测
    
    Args:
        images: 上传的图像文件列表
        model_name: 模型名称（可选）
        
    Returns:
        批量检测结果
    """
    try:
        results_list = []
        total_objects = 0
        
        logger.info(f"开始批量检测，共 {len(images)} 张图像")
        
        for i, image in enumerate(images):
            try:
                # 验证文件类型
                if not image.content_type or not image.content_type.startswith('image/'):
                    logger.warning(f"跳过非图像文件：{image.filename}")
                    continue
                
                # 保存图像
                image_path = save_upload(image)
                
                # 推理检测
                results = model_manager.predict(str(image_path), model_name)
                
                # 绘制结果
                output_path = draw_detections(str(image_path), results)
                
                # 保存到数据库
                record_id = create_detection_record(
                    image_path=str(image_path),
                    image_name=image.filename,
                    model_name=model_name or model_manager.active_model,
                    results=results
                )
                
                results_list.append({
                    "index": i,
                    "filename": image.filename,
                    "image_path": str(image_path),
                    "output_image": str(output_path),
                    "results": results,
                    "record_id": record_id
                })
                
                total_objects += len(results)
                logger.info(f"[{i+1}/{len(images)}] {image.filename}: {len(results)} 个目标")
                
            except Exception as e:
                logger.error(f"处理图像 {image.filename} 失败：{e}")
                results_list.append({
                    "index": i,
                    "filename": image.filename,
                    "error": str(e)
                })
        
        return JSONResponse(content={
            "success": True,
            "total_images": len(images),
            "processed_images": len([r for r in results_list if 'error' not in r]),
            "total_objects": total_objects,
            "results": results_list,
            "model_used": model_name or model_manager.active_model
        })
        
    except Exception as e:
        logger.error(f"批量检测失败：{e}")
        raise HTTPException(status_code=500, detail=f"批量检测失败：{str(e)}")


@router.get("/{record_id}")
async def get_detection_result(record_id: int):
    """
    获取检测结果
    
    Args:
        record_id: 检测记录 ID
        
    Returns:
        检测结果详情
    """
    from app.db.crud import get_detection_record
    
    record = get_detection_record(record_id)
    
    if not record:
        raise HTTPException(status_code=404, detail="未找到检测记录")
    
    return {
        "success": True,
        "record": record
    }
