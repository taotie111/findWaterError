#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据迁移脚本 - 将 H:/model 下的漂浮物数据集迁移到项目中
"""

import shutil
import random
from pathlib import Path
import os

# 源数据路径
EXTERNAL_DATA = Path(r"H:/model/LakeFloatingPlasticWasteDetectionDataset")

# 目标项目路径
PROJECT_ROOT = Path(r"H:/code/01_image_center")
PROJECT_DATA = PROJECT_ROOT / "data"

# 示例数据数量
SAMPLE_COUNT = 100


def copy_all_data():
    """复制所有数据到项目目录"""
    print("=" * 80)
    print("开始复制漂浮物数据集...")
    print("=" * 80)
    
    # 创建目标目录
    (PROJECT_DATA / "processed" / "train").mkdir(parents=True, exist_ok=True)
    (PROJECT_DATA / "processed" / "val").mkdir(parents=True, exist_ok=True)
    (PROJECT_DATA / "processed" / "test").mkdir(parents=True, exist_ok=True)
    
    (PROJECT_DATA / "annotations" / "yolo_format" / "train").mkdir(parents=True, exist_ok=True)
    (PROJECT_DATA / "annotations" / "yolo_format" / "val").mkdir(parents=True, exist_ok=True)
    (PROJECT_DATA / "annotations" / "yolo_format" / "test").mkdir(parents=True, exist_ok=True)
    
    # 复制图像
    print("\n[1/4] 复制图像...")
    
    # 训练集
    src_train_img = EXTERNAL_DATA / "YOLO_Dataset" / "images" / "train"
    dst_train_img = PROJECT_DATA / "processed" / "train"
    if src_train_img.exists():
        count = len(list(src_train_img.glob("*.jpg"))) + len(list(src_train_img.glob("*.png")))
        print(f"  训练集图像：{count} 张")
        shutil.copytree(src_train_img, dst_train_img, dirs_exist_ok=True)
    
    # 验证集
    src_val_img = EXTERNAL_DATA / "YOLO_Dataset" / "images" / "val"
    dst_val_img = PROJECT_DATA / "processed" / "val"
    if src_val_img.exists():
        count = len(list(src_val_img.glob("*.jpg"))) + len(list(src_val_img.glob("*.png")))
        print(f"  验证集图像：{count} 张")
        shutil.copytree(src_val_img, dst_val_img, dirs_exist_ok=True)
    
    # 复制标注
    print("\n[2/4] 复制标注...")
    
    # 训练集标注
    src_train_lbl = EXTERNAL_DATA / "YOLO_Dataset" / "labels" / "train"
    dst_train_lbl = PROJECT_DATA / "annotations" / "yolo_format" / "train"
    if src_train_lbl.exists():
        count = len(list(src_train_lbl.glob("*.txt")))
        print(f"  训练集标注：{count} 张")
        shutil.copytree(src_train_lbl, dst_train_lbl, dirs_exist_ok=True)
    
    # 验证集标注
    src_val_lbl = EXTERNAL_DATA / "YOLO_Dataset" / "labels" / "val"
    dst_val_lbl = PROJECT_DATA / "annotations" / "yolo_format" / "val"
    if src_val_lbl.exists():
        count = len(list(src_val_lbl.glob("*.txt")))
        print(f"  验证集标注：{count} 张")
        shutil.copytree(src_val_lbl, dst_val_lbl, dirs_exist_ok=True)
    
    print("\n[OK] 所有数据复制完成！")
    print(f"  图像位置：{PROJECT_DATA / 'processed'}")
    print(f"  标注位置：{PROJECT_DATA / 'annotations' / 'yolo_format'}")


def create_sample_dataset():
    """创建 100 张示例数据集（用于 Git 上传）"""
    print("\n" + "=" * 80)
    print("创建示例数据集（100 张）...")
    print("=" * 80)
    
    # 创建示例目录
    sample_dir = PROJECT_ROOT / "sample_data"
    (sample_dir / "images").mkdir(parents=True, exist_ok=True)
    (sample_dir / "labels").mkdir(parents=True, exist_ok=True)
    
    # 从训练集中随机选择 100 张
    train_images = PROJECT_DATA / "processed" / "train"
    train_labels = PROJECT_DATA / "annotations" / "yolo_format" / "train"
    
    if not train_images.exists():
        print("  ❌ 训练集图像不存在，请先运行 copy_all_data()")
        return
    
    # 获取所有图像文件
    image_files = list(train_images.glob("*.jpg")) + list(train_images.glob("*.png"))
    
    if len(image_files) < SAMPLE_COUNT:
        print(f"  ⚠️ 图像数量不足 {SAMPLE_COUNT} 张，使用全部 {len(image_files)} 张")
        sample_count = len(image_files)
    else:
        sample_count = SAMPLE_COUNT
    
    # 随机选择
    selected_images = random.sample(image_files, sample_count)
    
    print(f"\n  选择 {sample_count} 张图像作为示例...")
    
    # 复制图像和对应标注
    copied_count = 0
    for img_path in selected_images:
        # 复制图像
        dst_img = sample_dir / "images" / img_path.name
        shutil.copy2(img_path, dst_img)
        
        # 复制标注
        lbl_path = train_labels / img_path.stem
        if lbl_path.with_suffix(".txt").exists():
            dst_lbl = sample_dir / "labels" / lbl_path.name
            shutil.copy2(lbl_path.with_suffix(".txt"), dst_lbl)
            copied_count += 1
    
    print(f"  [OK] 示例数据集创建完成！")
    print(f"    位置：{sample_dir}")
    print(f"    图像：{sample_count} 张")
    print(f"    标注：{copied_count} 张")
    
    # 创建示例数据集的 data.yaml
    sample_yaml = sample_dir / "data.yaml"
    sample_yaml.write_text(f"""# 示例数据集配置
# 用于 Git 上的快速测试

train: {sample_dir}/images
val: {sample_dir}/images
test: {sample_dir}/images

# 类别配置
nc: 1
names:
  - floating_debris  # 漂浮物

# 注意：这是示例数据，仅包含 100 张漂浮物图像
# 完整数据请使用 data/processed/ 目录
""")
    
    print(f"    配置：{sample_yaml}")


def update_data_yaml():
    """更新项目 data.yaml 配置"""
    print("\n" + "=" * 80)
    print("更新 data.yaml 配置...")
    print("=" * 80)
    
    data_yaml = PROJECT_DATA / "annotations" / "data.yaml"
    
    # 统计各类别数量
    train_dir = PROJECT_DATA / "annotations" / "yolo_format" / "train"
    val_dir = PROJECT_DATA / "annotations" / "yolo_format" / "val"
    
    train_count = len(list(train_dir.glob("*.txt"))) if train_dir.exists() else 0
    val_count = len(list(val_dir.glob("*.txt"))) if val_dir.exists() else 0
    
    content = f"""# 水体问题数据集配置文件
# 最后更新：2026-04-03

# ============================================================
# 数据集路径
# ============================================================
# 训练集
train: H:/code/01_image_center/data/processed/train

# 验证集
val: H:/code/01_image_center/data/processed/val

# 测试集（可选）
test: H:/code/01_image_center/data/processed/test

# ============================================================
# 类别配置
# ============================================================
# 类别数量：7 类（6 类水体问题 + 1 类漂浮物）
nc: 7

# 类别名称（按 ID 顺序）
names:
  - garbage            # 0: 垃圾
  - illegal_construction  # 1: 违建
  - illegal_discharge     # 2: 排污
  - floating_debris       # 3: 漂浮物（来自 H:/model 数据集）
  - bank_damage           # 4: 岸坡破坏
  - other                 # 5: 其他
  - plastic_waste         # 6: 塑料垃圾（来自 H:/model 数据集）

# ============================================================
# 数据集统计
# ============================================================
# 总标注数：训练集 {train_count} 张 + 验证集 {val_count} 张
total_annotations:
  train: {train_count}
  val: {val_count}

# 类别分布（需要手动统计）
class_distribution:
  floating_debris: {train_count}  # 主要来自 H:/model 数据集
  plastic_waste: {train_count}    # 主要来自 H:/model 数据集
  # 其他类别需要手动标注

# ============================================================
# 数据来源说明
# ============================================================
# 1. 漂浮物/塑料垃圾数据来自：H:/model/LakeFloatingPlasticWasteDetectionDataset/
# 2. 其他 6 类水体问题数据需要手动标注
# 3. 示例数据（100 张）在：sample_data/ 目录，可用于 Git 测试

# ============================================================
# 标注格式
# ============================================================
annotation_format: yolo

# 标注文件位置
annotations:
  train: H:/code/01_image_center/data/annotations/yolo_format/train
  val: H:/code/01_image_center/data/annotations/yolo_format/val
  test: H:/code/01_image_center/data/annotations/yolo_format/test

# 类别文件
classes_file: H:/code/01_image_center/data/annotations/classes.txt
"""
    
    data_yaml.write_text(content, encoding='utf-8')
    print(f"  [OK] data.yaml 已更新：{data_yaml}")


def create_readme():
    """创建数据说明文档"""
    print("\n" + "=" * 80)
    print("创建数据说明文档...")
    print("=" * 80)
    
    readme = PROJECT_DATA / "README.md"
    
    content = """# 数据集说明

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
- ✅ 类别：漂浮物/塑料垃圾（单类别）
- ✅ 数量：约 1000+ 张图像
- ✅ 划分：train/val/test

### 数据位置

**完整数据**：
```
data/
├── processed/
│   ├── train/      # 训练图像（约 800+ 张）
│   ├── val/        # 验证图像（约 100+ 张）
│   └── test/       # 测试图像（约 100+ 张）
└── annotations/
    └── yolo_format/
        ├── train/  # 训练标注
        ├── val/    # 验证标注
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

> **注意**：这两个类别可以合并使用，取决于具体需求

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

```python
# 在项目根目录运行
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
- ✅ `data/annotations/` - 标注配置文件（不包含实际标注）
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
"""
    
    readme.write_text(content, encoding='utf-8')
    print(f"  [OK] 数据说明文档已创建：{readme}")


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("漂浮物数据集迁移工具")
    print("=" * 80)
    
    # 1. 复制所有数据
    copy_all_data()
    
    # 2. 创建示例数据集
    create_sample_dataset()
    
    # 3. 更新配置
    update_data_yaml()
    
    # 4. 创建说明文档
    create_readme()
    
    print("\n" + "=" * 80)
    print("✅ 数据迁移完成！")
    print("=" * 80)
    print("\n下一步:")
    print("1. 检查数据：data/processed/ 和 data/annotations/yolo_format/")
    print("2. 查看示例数据：sample_data/")
    print("3. 更新类别定义：data/annotations/classes.txt")
    print("4. 开始训练：使用 sample_data 或完整数据")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
