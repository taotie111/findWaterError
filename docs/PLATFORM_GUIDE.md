# 水体问题智能检测平台 - 部署指南

**版本**：1.0.0  
**最后更新**：2026-04-03  
**维护者**：taotie111

---

## 📋 目录

1. [平台简介](#1-平台简介)
2. [快速开始](#2-快速开始)
3. [后端部署](#3-后端部署)
4. [前端部署](#4-前端部署 - 待实现)
5. [API 文档](#5-api 文档)
6. [常见问题](#6-常见问题)

---

## 1. 平台简介

### 功能特性

- ✅ **多模型支持**：DINOv2 / YOLOv8 / YOLOv10 / YOLO-SE
- ✅ **单张检测**：上传单张图像实时检测
- ✅ **批量检测**：支持批量图像检测
- ✅ **结果可视化**：自动绘制检测框
- ✅ **历史记录**：保存检测历史到数据库
- ✅ **统计分析**：检测数据统计
- ✅ **模型切换**：支持热切换模型

### 技术栈

**后端**：
- FastAPI 0.109.0
- PyTorch 2.6.0
- Ultralytics (YOLO)
- SQLAlchemy (数据库)
- SQLite / PostgreSQL

**前端**（待实现）：
- Vue 3.4+
- Element Plus
- Pinia

---

## 2. 快速开始

### 环境要求

- **Python**: 3.8+
- **GPU**: NVIDIA (8GB+ 显存推荐)
- **CUDA**: 12.4+
- **内存**: 8GB+

### 一键启动（后端）

```bash
cd backend

# Windows
start.bat

# Linux/Mac
bash start.sh
```

### 访问

- **API 文档**：http://localhost:8000/docs
- **服务地址**：http://localhost:8000

---

## 3. 后端部署

### 3.1 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3.2 配置文件

编辑 `backend/config.yaml`：

```yaml
server:
  host: "0.0.0.0"
  port: 8000

model:
  default_model: "yolov8"
  
inference:
  conf_threshold: 0.25
  iou_threshold: 0.45
```

### 3.3 启动服务

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3.4 测试 API

```bash
# 健康检查
curl http://localhost:8000/api/health

# 获取模型列表
curl http://localhost:8000/api/models

# 单张检测
curl -X POST "http://localhost:8000/api/detect/" \
  -F "image=@test.jpg" \
  -F "model_name=yolov8"
```

---

## 4. API 文档

### 核心接口

#### 4.1 检测接口

**单张检测**
```http
POST /api/detect/
Content-Type: multipart/form-data

image: <文件>
model_name: yolov8 (可选)
```

**响应示例**：
```json
{
  "success": true,
  "record_id": 1,
  "image_path": "uploads/xxx.jpg",
  "output_image": "outputs/result_xxx.jpg",
  "results": [
    {
      "class_id": 0,
      "class_name": "garbage",
      "confidence": 0.95,
      "bbox": {
        "x_min": 100,
        "y_min": 200,
        "x_max": 300,
        "y_max": 400
      }
    }
  ],
  "total_objects": 1
}
```

**批量检测**
```http
POST /api/detect/batch
Content-Type: multipart/form-data

images: <文件列表>
model_name: yolov8 (可选)
```

#### 4.2 模型管理

**获取模型列表**
```http
GET /api/models
```

**切换模型**
```http
POST /api/models/switch?model_name=yolov8
```

**获取模型状态**
```http
GET /api/models/status
```

#### 4.3 历史记录

**获取检测历史**
```http
GET /api/history?limit=10&offset=0
```

**获取详情**
```http
GET /api/history/{record_id}
```

**删除记录**
```http
DELETE /api/history/{record_id}
```

#### 4.4 统计接口

**统计摘要**
```http
GET /api/stats/summary
```

---

## 5. 数据库

### SQLite（开发环境）

数据库文件：`backend/detections.db`

### PostgreSQL（生产环境）

配置 `config.yaml`：
```yaml
database:
  url: "postgresql://user:password@localhost:5432/findwater"
```

### 数据表结构

```sql
CREATE TABLE detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT NOT NULL,
    image_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    results JSON,
    total_objects INTEGER,
    category_counts JSON
);
```

---

## 6. 常见问题

### Q1: 启动失败 "ModuleNotFoundError"

**A**: 确保已安装依赖：
```bash
pip install -r requirements.txt
```

### Q2: GPU 显存不足

**A**: 
1. 减小 `batch_size`（config.yaml）
2. 启用 `half_precision: true`
3. 卸载不用的模型

### Q3: 模型下载慢

**A**: 
- YOLO 模型会自动从 Ultralytics 下载
- 可以手动下载后放到 `backend/models/` 目录

### Q4: CORS 错误

**A**: 检查 `config.yaml` 中的 `cors.allow_origins` 配置

### Q5: 检测速度慢

**A**:
1. 使用更小的模型（yolov8n）
2. 减小 `img_size`
3. 启用半精度推理

---

## 7. 开发指南

### 添加新模型

1. 在 `config.yaml` 中添加模型配置
2. 在 `model_manager.py` 中实现加载逻辑
3. 重启服务

### 自定义 API

在 `backend/app/api/` 创建新的路由文件：

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/custom")
async def custom_endpoint():
    return {"message": "Hello"}
```

在 `main.py` 中注册路由。

---

## 8. 下一步

### Phase 2：前端开发（待实现）

- [ ] Vue 3 项目创建
- [ ] 图像上传组件
- [ ] 检测画布组件
- [ ] 结果展示
- [ ] 历史记录页面
- [ ] 统计图表

### Phase 3：功能完善（待实现）

- [ ] 批量检测优化
- [ ] 用户认证
- [ ] Docker 部署
- [ ] 性能优化

---

**相关文档**：
- [项目 README](../README.md)
- [环境配置](docs/ENVIRONMENT.md)
- [配置说明](docs/CONFIG_SUMMARY.md)

**维护者**：taotie111  
**GitHub**：https://github.com/taotie111/findWaterError
