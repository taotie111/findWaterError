# findWaterError - 多模型水体问题智能识别系统 🌊

**支持模型**：DINOv2 | YOLOv8 | YOLOv10 | YOLO-SE  
**当前环境**：Python 3.13.5 | PyTorch 2.6.0+cu124 | CUDA 13.1 | RTX 3060 (12GB)  
**平台**：✅ Web 检测平台 | ✅ 标注系统 | ✅ 训练代码 | ✅ 示例数据集

[![GitHub](https://img.shields.io/github/repo-size/taotie111/findWaterError)](https://github.com/taotie111/findWaterError)
[![License](https://img.shields.io/github/license/taotie111/findWaterError)](https://github.com/taotie111/findWaterError/blob/master/LICENSE)

---

## 🌟 核心功能

### 🤖 检测平台

- ✅ **Web 界面**：Vue 3 + Element Plus
- ✅ **单张检测**：上传图像实时检测
- ✅ **批量检测**：支持批量图像处理
- ✅ **结果可视化**：自动绘制检测框
- ✅ **历史记录**：数据库存储检测历史
- ✅ **统计分析**：检测数据多维分析
- ✅ **模型管理**：热切换检测模型

### 📝 标注系统

- ✅ **多工具支持**：LabelImg/LabelMe/CVAT
- ✅ **格式统一**：自动转换为 YOLO 格式
- ✅ **质量检查**：完善的质检流程
- ✅ **团队协作**：多人标注支持

### 🎯 训练系统

- ✅ **多模型训练**：DINOv2/YOLOv8/YOLOv10/YOLO-SE
- ✅ **完整流程**：数据加载→训练→验证→导出
- ✅ **可视化**：训练曲线、混淆矩阵、分类报告
- ✅ **类别分析**：每个类别的准确率统计

### 📊 数据集

- ✅ **示例数据**：100 张漂浮物图像（已包含）
- ✅ **完整数据**：1800+ 张漂浮物图像（本地）
- ✅ **6 类体系**：5 类水体问题 + 漂浮物

---

## 🚀 快速开始

### 方式 1：使用示例数据（推荐新手）

**无需准备数据，立即开始训练！**

```bash
# 1. 克隆仓库
git clone https://github.com/taotie111/findWaterError.git
cd findWaterError

# 2. 安装依赖
pip install -r requirements.txt
pip install ultralytics  # YOLO 训练

# 3. 使用示例数据训练 YOLOv8
cd sample_data
yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=10 imgsz=640
```

**训练结果**：
- ✅ 10 个 epoch 约 5-10 分钟
- ✅ 模型保存在 `runs/detect/train/weights/best.pt`
- ✅ 可立即看到训练曲线和评估结果

---

### 方式 2：使用完整数据（本地）

**使用完整的 1800+ 张图像数据**

```bash
# 1. 确保数据已迁移到项目目录
cd H:/code/01_image_center
python src/scripts/migrate_data.py

# 2. 训练 YOLOv8
yolo task=detect mode=train model=yolov8m.pt data=data/annotations/data.yaml epochs=100

# 3. 训练 DINOv2
python src/scripts/train_dinov2.py
```

---

### 方式 3：启动 Web 检测平台

**完整的 Web 界面，支持图像上传和实时检测**

```bash
# 终端 1 - 启动后端
cd backend
start.bat

# 终端 2 - 启动前端
cd frontend
npm install  # 首次运行
npm run dev

# 访问 http://localhost:5173
```

---

## 📊 类别体系

本项目支持 **6 类水体问题**检测：

| ID | 类别名称 | 中文名称 | 说明 | 数据来源 |
|----|---------|---------|------|---------|
| 0 | garbage | 垃圾 | 水面漂浮垃圾 | 需标注 |
| 1 | illegal_construction | 违建 | 违章建筑 | 需标注 |
| 2 | illegal_discharge | 排污 | 违法排污 | 需标注 |
| 3 | **floating_debris** | **漂浮物** | **塑料垃圾等** | ✅ 已有 1800+ 张 |
| 4 | bank_damage | 岸坡破坏 | 岸坡植被破坏 | 需标注 |
| 5 | other | 其他 | 其他问题 | 需标注 |

> **注意**：漂浮物类别已整合塑料垃圾数据，其他 5 类需要手动标注。

---

## 🎯 训练指南

### 方式 1：统一训练入口（最简单）

```bash
cd H:/code/01_image_center

# 列出所有可用模型
python src/scripts/train.py --list

# 训练 YOLOv8（100 轮）
python src/scripts/train.py --model yolov8 --epochs 100

# 训练 YOLOv10
python src/scripts/train.py --model yolov10

# 训练 DINOv2
python src/scripts/train.py --model dinov2
```

**支持参数**：
```bash
python src/scripts/train.py --model yolov8 \
  --epochs 100 \
  --data data/annotations/data.yaml \
  --imgsz 640 \
  --batch 16 \
  --device 0
```

---

### 方式 2：使用 YOLO 脚本

```bash
cd H:/code/01_image_center

# 快速测试（示例数据，10 轮）
python src/scripts/train_yolo.py --model yolov8n --epochs 10 --data sample_data/data.yaml

# 完整训练（完整数据，100 轮）
python src/scripts/train_yolo.py --model yolov8m --epochs 100 --data data/annotations/data.yaml

# 自定义配置
python src/scripts/train_yolo.py \
  --model yolov8m \
  --data data/annotations/data.yaml \
  --epochs 100 \
  --imgsz 640 \
  --batch 16 \
  --device 0 \
  --project runs/detect \
  --name custom_train
```

**支持参数**：
```bash
python src/scripts/train_yolo.py \
  --model yolov8n/s/m/l/x        # 模型版本
  --epochs 100                    # 训练轮数
  --imgsz 640                     # 图像尺寸
  --batch 16                      # 批次大小
  --device 0                      # GPU 设备
  --data data.yaml                # 数据集配置
  --optimizer SGD/Adam/AdamW      # 优化器
  --lr0 0.01                      # 初始学习率
  --mosaic 1.0                    # mosaic 增强
  --mixup 0.0                     # mixup 增强
```

---

### 方式 3：使用 DINOv2 脚本

```bash
cd H:/code/01_image_center

# 使用 Jupyter Notebook（推荐）
# 打开 notebooks/dinov2_training_complete.ipynb
# 逐格运行

# 或使用 Python 脚本
python src/scripts/train_dinov2.py \
  --model dinov2-large \
  --epochs 20 \
  --data data/processed \
  --batch-size 1 \
  --accumulation 8
```

**支持参数**：
```bash
python src/scripts/train_dinov2.py \
  --model dinov2-small/base/large   # 模型版本
  --epochs 20                        # 训练轮数
  --batch-size 1                     # 批次大小
  --accumulation 8                   # 梯度累积
  --lr 1e-5                          # 学习率
  --frozen-layers 20                 # 冻结层数
```

---

### 方式 4：使用 Ultralytics CLI

```bash
# YOLOv8 训练
yolo task=detect mode=train model=yolov8m.pt data=data/annotations/data.yaml epochs=100

# 自定义配置
yolo task=detect mode=train \
  model=yolov8m.pt \
  data=data/annotations/data.yaml \
  epochs=100 \
  imgsz=640 \
  batch=16 \
  device=0 \
  project=runs/detect \
  name=custom_train

# 验证
yolo task=detect mode=val model=runs/detect/train/weights/best.pt data=data.yaml

# 预测
yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source=data/images/test
```

---

## 📈 训练结果（2026-04-04）

### YOLOv10m 完整数据训练结果

**训练配置**：
| 参数 | 值 |
|------|-----|
| 模型 | YOLOv10m |
| 数据集 | 1801 张图像 |
| 训练轮数 | 50 epochs |
| 批次大小 | 16 |
| 图像尺寸 | 640 |
| 设备 | RTX 3060 (12GB) |

**最终性能**：

| 指标 | 值 |
|------|-----|
| mAP50 | **80.9%** |
| mAP50-95 | **46.7%** |
| Precision | 78.2% |
| Recall | 74.0% |

**性能对比**：

| 数据集 | mAP50 | mAP50-95 | 提升 |
|--------|-------|----------|------|
| 示例数据 (100 张) | 17.1% | 8.05% | - |
| 完整数据 (1801 张) | 80.9% | 46.7% | **4.7x / 5.8x** |

**最佳模型**：
```
runs/detect/runs/detect/yolov10_full_final/weights/best.pt (66.6MB)
```

**已训练模型存档**：
| 模型 | 路径 | 大小 |
|------|------|------|
| YOLOv10m (best) | `runs/detect/runs/detect/yolov10_full_final/weights/best.pt` | 66.6MB |
| YOLOv10m (last) | `runs/detect/runs/detect/yolov10_full_final/weights/last.pt` | 66.6MB |
| YOLOv10m (50ep) | `runs/detect/runs/detect/yolov10_full2/weights/best.pt` | 66.6MB |
| DINOv2 | `runs/dinov2/exp1/best_model.pth` | - |

---

## 📁 项目结构

```
findWaterError/
├── 📖 README.md                     # 项目说明（本文档）
├── 📄 LICENSE                       # MIT 许可证
├── 📦 requirements.txt              # Python 依赖
├── .gitignore                       # Git 忽略配置
│
├── 🌐 backend/                      # Python 后端（FastAPI）
│   ├── app/
│   │   ├── main.py                 # FastAPI 应用
│   │   ├── api/                    # API 路由
│   │   ├── core/                   # 模型管理器
│   │   └── ...
│   ├── config.yaml                 # 后端配置
│   └── start.bat                   # 启动脚本
│
├── 🎨 frontend/                     # Vue 3 前端
│   ├── src/
│   │   ├── views/                  # 页面视图
│   │   ├── api/                    # API 封装
│   │   └── router/                 # 路由
│   ├── package.json                # Node 依赖
│   └── start.bat                   # 启动脚本
│
├── 📊 sample_data/                  # 示例数据集（100 张）
│   ├── images/                     # 示例图像
│   ├── labels/                     # 示例标注
│   └── data.yaml                   # 数据集配置
│
├── 💾 data/                         # 完整数据集（本地）
│   ├── processed/                  # 完整图像（1800+ 张）
│   ├── annotations/                # 标注配置
│   └── README.md                   # 数据说明
│
├── 🐍 src/                          # 训练代码
│   ├── scripts/
│   │   ├── train.py                # 统一训练入口 ⭐
│   │   ├── train_yolo.py           # YOLO 训练脚本
│   │   ├── train_dinov2.py         # DINOv2 训练脚本
│   │   ├── migrate_data.py         # 数据迁移
│   │   └── ...
│   └── ...
│
├── 📝 configs/                      # 模型配置
│   ├── dinov2_config.yaml
│   ├── yolov8_config.yaml
│   ├── yolov10_config.yaml
│   └── yolo-se_config.yaml
│
├── 📓 notebooks/                    # Jupyter Notebooks
│   └── dinov2_training_complete.ipynb
│
└── 📖 docs/                         # 文档
    ├── PLATFORM_GUIDE.md           # 平台部署指南
    ├── USAGE_GUIDE.md              # 使用指南
    ├── ANNOTATION_GUIDE.md         # 标注指南
    └── ...
```

---

## 📖 文档索引

### 平台使用

| 文档 | 说明 |
|------|------|
| [使用指南](docs/USAGE_GUIDE.md) | 完整使用教程 |
| [部署指南](docs/PLATFORM_GUIDE.md) | 平台部署说明 |

### 标注系统

| 文档 | 说明 |
|------|------|
| [标注指南](docs/ANNOTATION_GUIDE.md) | 6 类水体问题定义 |
| [标注工具](docs/ANNOTATION_TOOLS.md) | LabelImg/LabelMe/CVAT 教程 |
| [多工具标注](docs/MULTI_TOOL_ANNOTATION.md) | 多工具协同指南 |

### 数据说明

| 文档 | 说明 |
|------|------|
| [数据集说明](data/README.md) | 数据来源和使用 |
| [环境配置](docs/ENVIRONMENT.md) | Python/CUDA/PyTorch 版本 |

---

## 🛠️ 技术栈

### 后端
- FastAPI 0.109.0
- PyTorch 2.6.0+cu124
- Ultralytics (YOLO)
- Transformers (DINOv2)
- SQLAlchemy

### 前端
- Vue 3.4
- Vite 5
- Element Plus
- Pinia
- Axios

### 标注工具
- LabelImg
- LabelMe
- CVAT

---

## 📄 许可证

MIT License

---

## 📞 联系方式

- **GitHub**: [@taotie111](https://github.com/taotie111)
- **项目地址**: https://github.com/taotie111/findWaterError
- **问题反馈**: [Issues](https://github.com/taotie111/findWaterError/issues)

---

## 🎉 快速测试

**5 分钟快速验证**：

```bash
# 1. 克隆
git clone https://github.com/taotie111/findWaterError.git
cd findWaterError/sample_data

# 2. 训练（10 个 epoch）
yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=10

# 3. 查看结果
# 打开 runs/detect/train/results.png
```

---

## 🔥 训练时间参考（RTX 3060）

| 模型 | 数据 | Epochs | 时间 |
|------|------|--------|------|
| YOLOv8n | 示例（100 张） | 10 | ~5 分钟 |
| YOLOv8m | 示例（100 张） | 10 | ~8 分钟 |
| YOLOv8m | 完整（1800 张） | 100 | ~3 小时 |
| DINOv2-large | 完整（1800 张） | 20 | ~12 小时 |

---

**最后更新**：2026-04-07  
**维护者**：taotie111
