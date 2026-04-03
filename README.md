# findWaterError - 多模型水体问题识别系统 🌊

**支持模型**：DINOv2 | YOLOv8 | YOLOv10 | YOLO-SE  
**当前环境**：Python 3.13.5 | PyTorch 2.6.0+cu124 | CUDA 13.1 | RTX 3060 (12GB)

[![GitHub](https://img.shields.io/github/repo-size/taotie111/findWaterError)](https://github.com/taotie111/findWaterError)
[![License](https://img.shields.io/github/license/taotie111/findWaterError)](https://github.com/taotie111/findWaterError/blob/master/LICENSE)

---

## 📋 项目简介

本项目是一个**多模型支持**的水利问题自动识别系统，支持以下 4 种主流检测模型：

- **DINOv2** - Vision Transformer，适合细粒度分类
- **YOLOv8** - 实时目标检测，速度快精度高
- **YOLOv10** - 最新 YOLO 版本，支持无 NMS 推理
- **YOLO-SE** - 集成 SE 注意力机制的 YOLO 变体

实现对以下 6 类水体问题的自动识别：

- 🗑️ **垃圾** - 水面漂浮垃圾
- 🏗️ **违建** - 违章建筑
- 🚰 **排污** - 违法排污
- 🌊 **漂浮物** - 水面漂浮物
- 🏞️ **岸坡破坏** - 岸坡植被破坏
- 📦 **其他** - 其他问题

---

## 🚀 快速开始

### 1. 环境要求

- **Python**: 3.13+
- **PyTorch**: 2.6.0+cu124
- **CUDA**: 12.4+ (系统 CUDA 13.1 兼容)
- **GPU**: 8GB+ 显存 (推荐 RTX 3060 及以上)

### 2. 安装依赖

```bash
# 克隆仓库
git clone https://github.com/taotie111/findWaterError.git
cd findWaterError

# 安装依赖
pip install -r requirements.txt
```

**国内镜像源**：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 验证安装

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
```

**预期输出**：
```
PyTorch: 2.6.0+cu124
```

### 4. 准备数据

数据目录结构：
```
data/
└── raw/
    └── images/
        ├── 垃圾/
        ├── 违建/
        ├── 排污/
        ├── 漂浮物/
        ├── 岸坡破坏/
        └── 其他/
```

---

## 📊 模型性能对比

### DINOv2 (当前最佳)

| 指标 | 数值 | 备注 |
|------|------|------|
| **最佳验证准确率** | **68.96%** | 第 3 轮 |
| 最终验证准确率 | 65.41% | 第 20 轮 |
| 训练用时 | ~77 分钟/轮 | RTX 3060 |
| 显存占用 | ~11 GB | batch_size=1 |

### 各类别性能

| 类别 | 准确率 | 样本数 | 状态 |
|------|--------|--------|------|
| 垃圾 | ~75% | 50 | ✅ 良好 |
| 其他 | ~72% | 284 | ✅ 良好 |
| 违建 | ~70% | 37 | ✅ 良好 |
| 漂浮物 | ~50% | 2 | ⚠️ 样本不足 |
| 排污 | ~43% | 7 | ⚠️ 样本不足 |
| 岸坡破坏 | 0% | 0 | ❌ 无样本 |

> ⚠️ **注意**：类别不平衡导致部分类别准确率低，建议增加稀缺类别样本。

---

## 📁 项目结构

```
findWaterError/
│
├── README.md                          # 项目总览
├── requirements.txt                   # Python 依赖
├── .gitignore                         # Git 忽略配置
│
├── configs/                           # 📋 配置文件
│   ├── dinov2_config.yaml             # DINOv2 配置
│   ├── yolov8_config.yaml             # YOLOv8 配置
│   ├── yolov10_config.yaml            # YOLOv10 配置
│   └── yolo-se_config.yaml            # YOLO-SE 配置
│
├── src/                               # 🐍 源代码
│   ├── data/                          # 数据处理
│   ├── models/                        # 模型定义
│   ├── training/                      # 训练代码
│   ├── utils/                         # 工具函数
│   └── scripts/                       # 可执行脚本
│
├── notebooks/                         # 📓 Jupyter Notebooks
│   └── dinov2_training_complete.ipynb # DINOv2 完整训练
│
├── docs/                              # 📖 文档
│   ├── ENVIRONMENT.md                 # 环境配置说明
│   ├── DIRECTORY_STRUCTURE.md         # 目录结构说明
│   └── CONFIG_SUMMARY.md              # 配置总结
│
├── data/                              # 💾 数据目录（已排除）
│   ├── raw/                           # 原始数据
│   ├── processed/                     # 处理后数据
│   └── annotations/                   # 标注文件
│
└── runs/                              # 🚀 训练输出（已排除）
    ├── dinov2/
    ├── yolov8/
    ├── yolov10/
    └── yolo-se/
```

---

## 🎯 训练指南

### DINOv2 训练

**方式 1：Jupyter Notebook（推荐）**
```bash
# 打开 Notebook
jupyter notebook notebooks/dinov2_training_complete.ipynb
```

**方式 2：Python 脚本**
```bash
python src/scripts/start_finetune.py
```

**关键配置**（在 `configs/dinov2_config.yaml` 中修改）：
```yaml
model:
  backbone: "facebook/dinov2-large"
  frozen_layers: 20
  
training:
  epochs: 20
  batch_size: 1
  accumulation_steps: 8
  learning_rate: 1.0e-5
```

### YOLOv8 训练

```bash
# 使用 Ultralytics CLI
yolo task=detect mode=train model=yolov8m.pt data=configs/yolov8_config.yaml epochs=100

# 或使用 Python
python src/scripts/train.py --model yolov8 --config configs/yolov8_config.yaml
```

### YOLOv10 训练

```bash
yolo task=detect mode=train model=yolov10m.pt data=configs/yolov10_config.yaml epochs=100
```

### YOLO-SE 训练

```bash
yolo task=detect mode=train model=yolov8m.pt data=configs/yolo-se_config.yaml epochs=100
```

---

## 📊 可视化输出

训练完成后自动生成：

| 文件 | 说明 |
|------|------|
| `training_curves.png` | 训练曲线图（损失 + 准确率） |
| `per_class_accuracy.png` | 各类别准确率对比 |
| `confusion_matrix.png` | 混淆矩阵热力图 |
| `classification_report.txt` | 详细分类报告 |
| `training_log.json` | 完整训练历史 |

---

## 🔧 配置说明

### 修改模型配置

所有配置文件位于 `configs/` 目录：

```yaml
# configs/dinov2_config.yaml
model:
  name: "dinov2"
  backbone: "facebook/dinov2-large"  # 可选：small/base/large
  frozen_layers: 20

training:
  epochs: 20
  batch_size: 1
  learning_rate: 1.0e-5
```

### 修改数据路径

```yaml
# configs/dinov2_config.yaml
data:
  data_root: "data/raw/images"
  val_ratio: 0.2
```

---

## 💡 优化建议

### 1. 数据层面
- ✅ **增加稀缺类别样本**：岸坡破坏、漂浮物、排污
- ✅ **数据增强**：已启用随机翻转、颜色抖动
- ✅ **类别平衡**：使用加权损失函数或过采样

### 2. 训练层面
- ✅ **早停策略**：验证准确率不再提升时停止
- ✅ **学习率调整**：使用 warmup + cosine 调度器
- ✅ **梯度累积**：在显存有限时模拟大批次

### 3. 模型层面
- ✅ **尝试不同模型**：DINOv2 / YOLOv8 / YOLOv10
- ✅ **模型集成**：多个模型投票提升性能
- ✅ **注意力机制**：SE / CBAM / ECA

---

## 📄 许可证

MIT License

---

## 📞 联系方式

- **GitHub**: [@taotie111](https://github.com/taotie111)
- **项目地址**: https://github.com/taotie111/findWaterError
- **问题反馈**: [Issues](https://github.com/taotie111/findWaterError/issues)

---

## 📝 更新日志

### 2026-04-03
- ✅ 添加多模型支持（DINOv2 | YOLOv8 | YOLOv10 | YOLO-SE）
- ✅ 重构为模块化目录结构
- ✅ 创建完整的配置文件
- ✅ 添加环境配置文档
- ✅ 更新 requirements.txt

### 2026-03-XX
- ✅ 完成 DINOv2 微调训练
- ✅ 实现类别准确率分析
- ✅ 添加可视化输出

---

**最后更新**：2026-04-03  
**维护者**：taotie111
