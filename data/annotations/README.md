# 标注数据目录说明

**重要提示**：此目录包含原始标注数据，已在 `.gitignore` 中排除，不会上传到 GitHub。

---

## 📁 目录结构

```
data/
└── annotations/
    ├── README.md                      # 本说明文件
    ├── classes.txt                    # 类别文件（LabelImg 使用）
    ├── data.yaml                      # 数据集配置文件
    ├── annotation_template.md         # 标注模板
    ├── quality_checklist.md           # 质量检查表
    │
    ├── yolo_format/                   # YOLO 格式标注
    │   ├── train/                     # 训练集标注
    │   ├── val/                       # 验证集标注
    │   └── test/                      # 测试集标注
    │
    ├── labelme_jsons/                 # LabelMe JSON（备份）
    │   ├── train/
    │   ├── val/
    │   └── test/
    │
    └── voc_xml/                       # VOC XML（备份）
        ├── train/
        ├── val/
        └── test/
```

---

## 📋 文件说明

### 核心文件

| 文件 | 用途 | 是否上传 |
|------|------|---------|
| `classes.txt` | 类别定义文件 | ❌ 不上传 |
| `data.yaml` | 数据集配置 | ❌ 不上传 |
| `annotation_template.md` | 标注模板 | ❌ 不上传 |
| `quality_checklist.md` | 质量检查表 | ❌ 不上传 |

### 标注文件

| 目录 | 格式 | 内容 | 是否上传 |
|------|------|------|---------|
| `yolo_format/train/` | `.txt` | 训练集标注 | ❌ 不上传 |
| `yolo_format/val/` | `.txt` | 验证集标注 | ❌ 不上传 |
| `yolo_format/test/` | `.txt` | 测试集标注 | ❌ 不上传 |

---

## 🚀 使用指南

### 1. 开始标注

参考文档：
- [标注指南](../../docs/ANNOTATION_GUIDE.md)
- [标注工具使用](../../docs/ANNOTATION_TOOLS.md)

### 2. 标注流程

```bash
# 1. 使用 LabelImg 进行标注
labelImg

# 2. 设置保存目录为 data/annotations/yolo_format/train

# 3. 加载类别文件 classes.txt

# 4. 开始标注
```

### 3. 格式转换

如果有其他格式的标注文件，使用转换工具：

```bash
# LabelMe JSON 转 YOLO
python src/scripts/convert_annotations.py \
  --input data/annotations/labelme_jsons \
  --output data/annotations/yolo_format/train \
  --format labelme

# VOC XML 转 YOLO
python src/scripts/convert_annotations.py \
  --input data/annotations/voc_xml \
  --output data/annotations/yolo_format/train \
  --format voc
```

### 4. 质量检查

使用质量检查表：
- 打开 `quality_checklist.md`
- 逐项检查标注质量
- 记录问题并修改

---

## 📊 数据集配置

编辑 `data.yaml` 配置数据集：

```yaml
# 数据集路径
train: H:/code/01_image_center/data/processed/train
val: H:/code/01_image_center/data/processed/val
test: H:/code/01_image_center/data/processed/test

# 类别配置
nc: 6
names:
  - garbage
  - illegal_construction
  - illegal_discharge
  - floating_debris
  - bank_damage
  - other
```

---

## ⚠️ 注意事项

1. **不要上传标注数据到 GitHub**
   - 标注数据已添加到 `.gitignore`
   - 数据量较大，不适合版本控制
   - 可能包含敏感信息

2. **定期备份标注数据**
   - 使用外部硬盘备份
   - 或使用私有云存储

3. **统一标注标准**
   - 所有标注人员使用相同的类别定义
   - 定期进行质量检查
   - 及时更新标注规范

---

## 🔗 相关文档

- [标注指南](../../docs/ANNOTATION_GUIDE.md) - 详细的标注规范
- [标注工具使用](../../docs/ANNOTATION_TOOLS.md) - 工具教程
- [环境配置](../../docs/ENVIRONMENT.md) - 环境说明

---

**维护者**：taotie111  
**最后更新**：2026-04-03
