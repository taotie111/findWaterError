# 水体问题智能检测平台 - 完整使用指南

**版本**：1.0.0  
**最后更新**：2026-04-03  
**维护者**：taotie111

---

## 📋 目录

1. [平台简介](#1-平台简介)
2. [快速开始](#2-快速开始)
3. [后端使用](#3-后端使用)
4. [前端使用](#4-前端使用)
5. [API 文档](#5-api 文档)
6. [常见问题](#6-常见问题)

---

## 1. 平台简介

### 功能特性

✅ **多模型支持**：DINOv2 / YOLOv8 / YOLOv10 / YOLO-SE  
✅ **单张检测**：上传单张图像实时检测  
✅ **批量检测**：支持批量图像检测  
✅ **结果可视化**：自动绘制检测框  
✅ **历史记录**：保存检测历史到数据库  
✅ **统计分析**：检测数据统计  
✅ **模型管理**：支持热切换模型  

### 技术架构

```
┌─────────────┐      HTTP/REST      ┌─────────────┐
│  Vue 3 前端  │◄──────────────────►│ Python 后端  │
│  Element+   │                     │   FastAPI   │
└─────────────┘                     └──────┬──────┘
                                           │
                                    ┌──────▼──────┐
                                    │  模型管理器  │
                                    │ YOLO/DINOv2 │
                                    └─────────────┘
```

---

## 2. 快速开始

### 环境要求

- **Python**: 3.8+
- **Node.js**: 18+
- **GPU**: NVIDIA (8GB+ 显存推荐)
- **CUDA**: 12.4+

### 一键启动

#### 方式 1：分别启动

```bash
# 终端 1 - 启动后端
cd backend
start.bat

# 终端 2 - 启动前端
cd frontend
start.bat
```

#### 方式 2：只使用后端 API

```bash
cd backend
start.bat

# 访问 API 文档：http://localhost:8000/docs
```

---

## 3. 后端使用

### 启动后端

```bash
cd backend
start.bat
```

### 测试 API

**浏览器访问**：http://localhost:8000/docs

**cURL 测试**：

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

### 配置文件

编辑 `backend/config.yaml`：

```yaml
server:
  port: 8000
  
model:
  default_model: "yolov8"
  
inference:
  conf_threshold: 0.25
  img_size: 640
```

---

## 4. 前端使用

### 安装依赖

```bash
cd frontend
npm install
```

### 启动前端

```bash
start.bat
# 或
npm run dev
```

访问：http://localhost:5173

### 使用流程

#### 4.1 单张检测

1. 访问 **图像检测** 页面
2. 拖拽或选择图像
3. 选择模型（YOLOv8/YOLOv10 等）
4. 点击"开始检测"
5. 查看检测结果

#### 4.2 批量检测

1. 访问 **批量检测** 页面
2. 上传多张图像
3. 点击"开始批量检测"
4. 查看批量结果

#### 4.3 查看历史

1. 访问 **历史记录** 页面
2. 浏览检测历史
3. 点击"查看详情"

#### 4.4 模型管理

1. 访问 **模型管理** 页面
2. 查看已加载模型
3. 切换/加载/卸载模型

---

## 5. API 文档

### 核心接口

#### 5.1 检测接口

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
```

#### 5.2 模型管理

**获取模型列表**
```http
GET /api/models
```

**切换模型**
```http
POST /api/models/switch?model_name=yolov8
```

#### 5.3 历史记录

**获取历史**
```http
GET /api/history?limit=10&offset=0
```

**获取详情**
```http
GET /api/detect/{record_id}
```

---

## 6. 常见问题

### Q1: 后端启动失败

**A**: 
```bash
# 检查 Python 版本
python --version

# 重新安装依赖
cd backend
pip install -r requirements.txt --force-reinstall
```

### Q2: 前端启动失败

**A**:
```bash
# 检查 Node.js 版本
node --version

# 重新安装依赖
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Q3: 检测速度慢

**A**:
1. 使用更小的模型（yolov8n）
2. 减小 `img_size`（config.yaml）
3. 启用半精度推理

### Q4: GPU 显存不足

**A**:
1. 减小 `batch_size`
2. 启用 `half_precision: true`
3. 卸载不用的模型

### Q5: 前端无法连接后端

**A**:
1. 确保后端运行在 http://localhost:8000
2. 检查 vite.config.js 代理配置
3. 查看浏览器控制台错误信息

---

## 7. 项目结构

```
findWaterError/
├── backend/                    # Python 后端
│   ├── app/
│   │   ├── api/               # API 路由
│   │   ├── core/              # 核心逻辑
│   │   ├── db/                # 数据库
│   │   └── utils/             # 工具函数
│   ├── config.yaml            # 配置文件
│   └── requirements.txt       # Python 依赖
│
├── frontend/                   # Vue 前端
│   ├── src/
│   │   ├── api/               # API 封装
│   │   ├── views/             # 页面视图
│   │   └── router/            # 路由配置
│   └── package.json           # Node 依赖
│
└── docs/                       # 文档
    ├── PLATFORM_GUIDE.md      # 平台部署指南
    └── USAGE_GUIDE.md         # 使用指南（本文档）
```

---

## 8. 下一步

### 待实现功能

- [ ] 统计图表（ECharts）
- [ ] 用户认证系统
- [ ] Docker 部署
- [ ] 移动端适配
- [ ] 实时视频检测

### 性能优化

- [ ] 模型推理优化（TensorRT）
- [ ] 批量检测并发优化
- [ ] 前端懒加载
- [ ] CDN 加速

---

**相关文档**：
- [项目 README](../README.md)
- [平台部署指南](PLATFORM_GUIDE.md)
- [环境配置](ENVIRONMENT.md)

**维护者**：taotie111  
**GitHub**：https://github.com/taotie111/findWaterError
