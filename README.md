# DINOv2 水体问题识别 🌊

基于 DINOv2 的水利问题自动识别系统，支持 6 类水体问题检测。

## 📋 项目简介

本项目使用 DINOv2 视觉大模型进行微调，实现对以下 6 类水体问题的自动识别：

- 🗑️ **垃圾** - 水面漂浮垃圾
- 🏗️ **违建** - 违章建筑
- 🚰 **排污** - 违法排污
- 🌊 **漂浮物** - 水面漂浮物
- 🏞️ **岸坡破坏** - 岸坡植被破坏
- 📦 **其他** - 其他问题

## 🚀 快速开始

### 环境要求

- Python 3.8+
- PyTorch 2.0+
- CUDA 11.7+ (推荐)
- GPU: 8GB+ 显存 (RTX 3060 及以上)

### 安装依赖

```bash
pip install torch torchvision transformers scikit-learn matplotlib pillow
```

### 准备数据

将数据按以下结构组织：

```
data/
└── images/
    └── raw/
        ├── 垃圾/
        ├── 违建/
        ├── 排污/
        ├── 漂浮物/
        ├── 岸坡破坏/
        └── 其他/
```

### 开始训练

**方式 1：使用 Jupyter Notebook（推荐）**

打开 `dinov2_training_complete.ipynb`，逐格运行即可完成：
- 数据加载
- 模型训练
- 结果分析（含各类别准确率、混淆矩阵）

**方式 2：使用 Python 脚本**

```bash
python start_finetune.py
```

## 📊 训练结果

### 性能指标

| 指标 | 数值 |
|------|------|
| 最佳验证准确率 | 68.96% (第 3 轮) |
| 最终验证准确率 | 65.41% (第 20 轮) |
| 训练用时 | ~77 分钟/轮 (RTX 3060) |

### 各类别准确率

| 类别 | 准确率 | 样本数 |
|------|--------|--------|
| 垃圾 | ~75% | 50 |
| 违建 | ~70% | 37 |
| 排污 | ~43% | 7 |
| 漂浮物 | ~50% | 2 |
| 岸坡破坏 | 0% | 0 |
| 其他 | ~72% | 284 |

> ⚠️ **注意**：类别不平衡导致部分类别准确率低，建议增加稀缺类别样本。

## 📁 项目结构

```
findWaterError/
├── dinov2_training_complete.ipynb  # 完整训练 Notebook（含分类分析）
├── start_finetune.py                # 训练启动脚本
├── check_stats.py                   # 数据统计脚本
├── check_training_progress.py       # 进度检查脚本
├── extract_all_images_batch.py      # 批量图片提取
├── .gitignore                       # Git 忽略配置
├── README.md                        # 本文档
│
├── data/                            # 数据目录（已排除，需自行准备）
│   └── images/
│       └── raw/
│
├── excel/                           # Excel 原始文件（已排除）
│
└── runs/                            # 训练输出（已排除）
    └── finetune/
        ├── best_model.pth           # 最佳模型
        └── training_log.json        # 训练日志
```

## 📝 训练日志

训练历史已保存在 `runs/finetune/training_log.json`，包含：
- 每轮训练/验证损失
- 每轮训练/验证准确率
- **每个类别的准确率**
- 训练用时

## 📊 可视化输出

训练完成后自动生成：
- `training_curves.png` - 训练曲线图
- `per_class_accuracy.png` - 各类别准确率对比
- `confusion_matrix.png` - 混淆矩阵
- `classification_report.txt` - 详细分类报告

## 🔧 配置说明

在 `dinov2_training_complete.ipynb` 中修改配置：

```python
CONFIG = {
    'data_root': r'H:\code\01_image_center\data\images\raw',
    'model_name': 'dinov2-large',  # dinov2-small / dinov2-base / dinov2-large
    'frozen_layers': 20,
    'epochs': 20,
    'batch_size': 1,
    'accumulation_steps': 8,
    'learning_rate': 1e-5,
}
```

## 💡 优化建议

1. **增加数据量**：特别是稀缺类别（岸坡破坏、漂浮物、排污）
2. **数据增强**：已启用随机翻转、颜色抖动
3. **早停策略**：在验证准确率不再提升时停止
4. **类别平衡**：使用加权损失函数或过采样

## 📄 许可证

MIT License

## 📞 联系方式

- GitHub: [@taotie111](https://github.com/taotie111)
- 项目地址：https://github.com/taotie111/findWaterError

---

**最后更新**：2026-04-03
