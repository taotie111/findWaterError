# 多模型训练目录结构说明

**最后更新**：2026-04-03

---

## 📁 完整目录结构

```
findWaterError/
│
├── README.md                          # 项目总览
├── requirements.txt                   # Python 依赖
├── .gitignore                         # Git 忽略配置
│
├── configs/                           # 📋 配置文件
│   ├── data.yaml                      # 数据集配置
│   ├── dinov2_config.yaml             # DINOv2 配置
│   ├── yolov8_config.yaml             # YOLOv8 配置
│   ├── yolov10_config.yaml            # YOLOv10 配置
│   └── yolo-se_config.yaml            # YOLO-SE 配置
│
├── src/                               # 🐍 源代码
│   ├── data/                          # 数据处理
│   │   ├── dataset.py                 # 数据集类
│   │   ├── dataloader.py              # 数据加载器
│   │   └── transforms.py              # 数据增强
│   │
│   ├── models/                        # 🤖 模型定义
│   │   ├── dinov2_model.py            # DINOv2 模型
│   │   ├── yolov8_model.py            # YOLOv8 模型
│   │   ├── yolov10_model.py           # YOLOv10 模型
│   │   └── yolo-se_model.py           # YOLO-SE 模型
│   │
│   ├── training/                      # 🎯 训练代码
│   │   ├── trainer.py                 # 训练器基类
│   │   ├── dinov2_trainer.py          # DINOv2 训练器
│   │   ├── yolo_trainer.py            # YOLO 训练器
│   │   └── metrics.py                 # 评估指标
│   │
│   ├── utils/                         # 🛠️ 工具函数
│   │   ├── logger.py                  # 日志工具
│   │   ├── visualize.py               # 可视化工具
│   │   └── config.py                  # 配置加载
│   │
│   └── scripts/                       # 📜 可执行脚本
│       ├── train.py                   # 统一训练入口
│       ├── evaluate.py                # 评估脚本
│       ├── predict.py                 # 预测脚本
│       └── [其他工具脚本]
│
├── notebooks/                         # 📓 Jupyter Notebooks
│   ├── 01_data_exploration.ipynb      # 数据探索
│   ├── 02_dinov2_training.ipynb       # DINOv2 训练
│   ├── 03_yolov8_training.ipynb       # YOLOv8 训练
│   ├── 04_model_comparison.ipynb      # 模型对比
│   └── 05_error_analysis.ipynb        # 错误分析
│
├── data/                              # 💾 数据目录（已排除）
│   ├── raw/                           # 原始数据
│   │   ├── images/                    # 原始图片
│   │   └── excel/                     # Excel 文件
│   │
│   ├── processed/                     # 处理后数据
│   │   ├── train/                     # 训练集
│   │   ├── val/                       # 验证集
│   │   └── test/                      # 测试集
│   │
│   └── annotations/                   # 标注文件
│       ├── yolo_format/               # YOLO 格式
│       └── coco_format/               # COCO 格式
│
├── runs/                              # 🚀 实验输出（已排除）
│   ├── dinov2/
│   │   ├── exp1/                      # 实验 1
│   │   │   ├── best_model.pth
│   │   │   ├── training_log.json
│   │   │   └── plots/
│   │   └── exp2/                      # 实验 2
│   │
│   ├── yolov8/
│   │   └── exp1/
│   │
│   ├── yolov10/
│   │   └── exp1/
│   │
│   └── yolo-se/
│       └── exp1/
│
├── weights/                           # ⚖️ 预训练权重（已排除）
│   ├── dinov2/
│   ├── yolov8/
│   ├── yolov10/
│   └── yolo-se/
│
├── docs/                              # 📖 文档
│   ├── installation.md                # 安装指南
│   ├── training_guide.md              # 训练指南
│   ├── model_zoo.md                   # 模型库
│   └── [其他文档]
│
└── tests/                             # ✅ 单元测试
    ├── test_dataset.py
    ├── test_models.py
    └── test_training.py
```

---

## 🎯 设计理念

### 1. **模型隔离**
每个模型有独立的配置、代码和输出目录：
```
configs/dinov2_config.yaml
src/models/dinov2_model.py
src/training/dinov2_trainer.py
runs/dinov2/exp1/
```

### 2. **代码复用**
通用功能放在共享模块：
- `src/data/` - 数据加载和增强
- `src/utils/` - 工具函数
- `src/training/metrics.py` - 评估指标

### 3. **统一接口**
所有模型使用相同的训练接口：
```python
from src.training import get_trainer

# DINOv2
trainer = get_trainer('dinov2', config)
trainer.train()

# YOLOv8
trainer = get_trainer('yolov8', config)
trainer.train()
```

### 4. **清晰的实验管理**
```
runs/
├── dinov2/exp1/     # DINOv2 实验 1
├── dinov2/exp2/     # DINOv2 实验 2
├── yolov8/exp1/     # YOLOv8 实验 1
└── yolov10/exp1/    # YOLOv10 实验 1
```

---

## 📊 当前状态

### ✅ 已完成
- [x] 基础目录结构创建
- [x] 代码迁移到 `src/scripts/`
- [x] 文档迁移到 `docs/`
- [x] Notebook 迁移到 `notebooks/`
- [x] 数据目录重组
- [x] `.gitignore` 更新

### 🔄 待完成
- [ ] 创建统一的训练入口 `src/scripts/train.py`
- [ ] 创建模型配置文件
- [ ] 添加 YOLOv8 训练代码
- [ ] 添加 YOLOv10 训练代码
- [ ] 添加 YOLO-SE 训练代码
- [ ] 编写 `requirements.txt`
- [ ] 添加单元测试

---

## 🚀 快速开始

### 训练 DINOv2
```bash
# 方式 1：使用 Notebook
# 打开 notebooks/dinov2_training_complete.ipynb

# 方式 2：使用脚本（待创建）
python src/scripts/train.py --model dinov2 --config configs/dinov2_config.yaml
```

### 训练 YOLOv8（待实现）
```bash
python src/scripts/train.py --model yolov8 --config configs/yolov8_config.yaml
```

---

## 📝 添加新模型的步骤

1. **创建配置文件**
   ```bash
   configs/yolo-new_config.yaml
   ```

2. **创建模型定义**
   ```bash
   src/models/yolo-new_model.py
   ```

3. **创建训练器**
   ```bash
   src/training/yolo-new_trainer.py
   ```

4. **创建 Notebook（可选）**
   ```bash
   notebooks/06_yolo-new_training.ipynb
   ```

5. **更新文档**
   ```bash
   docs/model_zoo.md  # 添加新模型说明
   ```

---

## 💡 最佳实践

### 1. **实验命名**
```
runs/{model}/{model}_{date}_{description}/
例如：runs/yolov8/yolov8_20260403_baseline/
```

### 2. **配置管理**
- 所有超参数放在 `configs/`
- 使用 YAML 格式
- 为每个实验创建独立配置

### 3. **代码组织**
- 通用代码放在共享模块
- 模型特定代码放在对应文件
- 保持接口一致

### 4. **版本控制**
- ✅ 提交代码、配置、文档
- ❌ 不提交数据、模型权重、训练输出

---

## 📞 常见问题

**Q: 如何比较不同模型的性能？**

A: 使用 `notebooks/04_model_comparison.ipynb`，它会自动读取所有 `runs/` 中的日志并生成对比图表。

**Q: 如何添加新的数据集？**

A: 
1. 将数据放在 `data/raw/`
2. 更新 `configs/data.yaml`
3. 运行数据预处理脚本

**Q: 如何恢复训练？**

A: 每个实验目录都有 `training_log.json` 和 `best_model.pth`，可以在训练脚本中指定 `--resume` 参数。

---

**维护者**：taotie111  
**最后更新**：2026-04-03
