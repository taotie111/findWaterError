#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
统计分析 API（简化版）
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.db.crud import get_stats_summary

router = APIRouter()


@router.get("/summary")
async def get_summary_stats():
    """获取统计摘要"""
    stats = get_stats_summary()
    
    return JSONResponse(content={
        "success": True,
        "stats": stats
    })


@router.get("/by-category")
async def get_category_stats():
    """按类别统计（简化版）"""
    return {"success": True, "message": "待实现"}


@router.get("/by-time")
async def get_time_stats():
    """按时间统计（简化版）"""
    return {"success": True, "message": "待实现"}
