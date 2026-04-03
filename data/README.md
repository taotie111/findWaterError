# 数据集说明

**最后更新**：2026-04-03

---

## 📊 数据集概述

本项目包含两类数据：

1. **漂浮物/塑料垃圾数据**（来自 H:/model）
2. **6 类水体问题数据**（需要标注）

---

## 1. 漂浮物/塑料垃圾数据集

### 数据来源

**原始位置**：`H:/model/LakeFloatingPlasticWasteDetectionDataset/`

**数据集特点**：
- ✅ 已标注：YOLO 格式
- ✅ 类别：漂浮物/塑料垃圾
- ✅ 数量：约 1800 张图像（train + val）
- ✅ 划分：train/val/test

### 数据位置

**完整数据**（不上传 Git）：
```
data/
├── processed/
│   ├── train/      # 训练图像 1601 张
│   ├── val/        # 验证图像 200 张
│   └── test/       # 测试图像
└── annotations/
    └── yolo_format/
        ├── train/  # 训练标注 1601 张
        ├── val/    # 验证标注 200 张
        └── test/   # 测试标注
```

**示例数据**（可上传 Git）：
```
sample_data/
├── images/         # 100 张示例图像
└── labels/         # 100 张示例标注
```

### 类别映射

| ID | 类别名称 | 说明 |
|----|---------|------|
| 3 | floating_debris | 漂浮物（水面漂浮的塑料垃圾等） |
| 6 | plastic_waste | 塑料垃圾（特指塑料制品） |

> **注意**：这两个类别可以根据需求合并使用

---

## 2. 6 类水体问题数据集

### 类别定义

| ID | 类别名称 | 中文名称 | 说明 |
|----|---------|---------|------|
| 0 | garbage | 垃圾 | 水面漂浮垃圾 |
| 1 | illegal_construction | 违建 | 违章建筑 |
| 2 | illegal_discharge | 排污 | 违法排污 |
| 4 | bank_damage | 岸坡破坏 | 岸坡植被破坏 |
| 5 | other | 其他 | 其他问题 |

### 标注状态

- ⚠️ **需要标注**：目前这 6 类数据需要手动标注
- 📝 **标注工具**：LabelImg / LabelMe / CVAT
- 📖 **标注指南**：[docs/ANNOTATION_GUIDE.md](../docs/ANNOTATION_GUIDE.md)

---

## 🚀 快速开始

### 使用示例数据（立即开始）

```bash
# 示例数据已包含在 Git 仓库中
# 可以直接用于测试和训练

# 使用示例数据训练 YOLOv8
yolo task=detect mode=train model=yolov8n.pt data=sample_data/data.yaml epochs=10
```

### 使用完整数据

```bash
# 使用完整数据集训练
yolo task=detect mode=train model=yolov8m.pt data=data/annotations/data.yaml epochs=100
```

---

## 📝 数据迁移

如果数据不在项目目录中，运行迁移脚本：

```bash
cd H:\code\01_image_center
python src/scripts/migrate_data.py
```

这将：
1. ✅ 复制所有数据到 `data/processed/`
2. ✅ 复制标注到 `data/annotations/yolo_format/`
3. ✅ 创建 100 张示例数据到 `sample_data/`
4. ✅ 更新 `data.yaml` 配置

---

## ⚠️ Git 注意事项

### 可上传的文件

- ✅ `sample_data/` - 100 张示例数据
- ✅ `data/annotations/classes.txt` - 类别定义
- ✅ `data/annotations/data.yaml` - 数据集配置
- ✅ `data/README.md` - 本说明文档

### 不上传的文件

- ❌ `data/processed/` - 完整图像数据（太大）
- ❌ `data/annotations/yolo_format/` - 完整标注数据
- ❌ `data/raw/` - 原始数据

详见 `.gitignore` 配置。

---

## 📞 相关文档

- [标注指南](../docs/ANNOTATION_GUIDE.md)
- [标注工具使用](../docs/ANNOTATION_TOOLS.md)
- [多工具标注](../docs/MULTI_TOOL_ANNOTATION.md)

---

**维护者**：taotie111  
**数据来源**：H:/model/LakeFloatingPlasticWasteDetectionDataset/
