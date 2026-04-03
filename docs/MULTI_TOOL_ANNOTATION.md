# 多标注工具统一格式指南

**最后更新**：2026-04-03  
**维护者**：taotie111

---

## 📋 目录

1. [支持的标注工具](#1-支持的标注工具)
2. [统一格式标准](#2-统一格式标准)
3. [格式转换工具](#3-格式转换工具)
4. [最佳实践](#4-最佳实践)

---

## 1. 支持的标注工具

### ✅ 推荐工具组合

| 工具 | 适用场景 | 输出格式 | 推荐度 |
|------|---------|---------|--------|
| **LabelImg** | 快速矩形框标注 | YOLO/VOC | ⭐⭐⭐⭐⭐ |
| **LabelMe** | 多边形/精细标注 | JSON | ⭐⭐⭐⭐ |
| **CVAT** | 团队协作/视频标注 | COCO/YOLO/VOC | ⭐⭐⭐⭐⭐ |
| **Roboflow** | 在线标注+管理 | COCO/YOLO/VOC | ⭐⭐⭐⭐ |

### 工具选择建议

| 需求 | 推荐工具 | 理由 |
|------|---------|------|
| 快速标注 | LabelImg | 轻量、快速、易用 |
| 精细标注 | LabelMe | 支持多边形、语义分割 |
| 团队协作 | CVAT | 在线协作、任务分配 |
| 视频标注 | CVAT | 支持视频插值 |
| 数据管理 | Roboflow | 云端管理、版本控制 |

---

## 2. 统一格式标准

### 2.1 目标格式：YOLO

**为什么选择 YOLO 格式作为统一标准？**

1. ✅ 简洁：每行一个目标，文本格式
2. ✅ 通用：大多数检测框架支持
3. ✅ 高效：归一化坐标，与图像尺寸无关
4. ✅ 兼容：可轻松转换为其他格式

### 2.2 YOLO 格式规范

**文件格式**：`.txt`（与图像同名）

**每行格式**：
```
<class_id> <x_center> <y_center> <width> <height>
```

**说明**：
- `class_id`: 类别 ID（整数，从 0 开始）
- `x_center`: 边界框中心点 x 坐标（归一化到 0-1）
- `y_center`: 边界框中心点 y 坐标（归一化到 0-1）
- `width`: 边界框宽度（归一化到 0-1）
- `height`: 边界框高度（归一化到 0-1）

**示例**：
```
# image1.txt（对应 image1.jpg）
0 0.456 0.678 0.123 0.234  # garbage
1 0.234 0.345 0.456 0.567  # illegal_construction
3 0.789 0.123 0.089 0.156  # floating_debris
```

### 2.3 类别定义统一

**文件**：`data/annotations/classes.txt`

```
0 garbage
1 illegal_construction
2 illegal_discharge
3 floating_debris
4 bank_damage
5 other
```

**重要**：所有标注工具必须使用相同的类别定义！

---

## 3. 格式转换工具

### 3.1 统一转换脚本

**位置**：`src/scripts/convert_annotations.py`

**支持转换**：
- ✅ LabelMe JSON → YOLO
- ✅ VOC XML → YOLO
- ✅ COCO JSON → YOLO
- ✅ YOLO → VOC（反向转换）

### 3.2 使用方法

#### 批量转换 LabelMe 到 YOLO

```bash
python src/scripts/convert_annotations.py \
  --input data/annotations/labelme_jsons/train \
  --output data/annotations/yolo_format/train \
  --format labelme
```

#### 批量转换 VOC 到 YOLO

```bash
python src/scripts/convert_annotations.py \
  --input data/annotations/voc_xml/train \
  --output data/annotations/yolo_format/train \
  --format voc
```

#### COCO 格式转换

```bash
python src/scripts/convert_annotations.py \
  --input data/annotations/coco/annotations.json \
  --output data/annotations/yolo_format/train \
  --format coco
```

### 3.3 转换流程

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ LabelMe JSON│     │  转换脚本     │     │  YOLO txt   │
│ VOC XML     │────▶│              │────▶│             │
│ COCO JSON   │     │              │     │             │
└─────────────┘     └──────────────┘     └─────────────┘
      ↓                    ↓                    ↓
  原始标注            格式统一            统一输出
```

---

## 4. 最佳实践

### 4.1 团队协作标注

#### 场景：多人使用不同工具

```
标注员 A（LabelImg）──┐
                     │
标注员 B（LabelMe）───┼──▶ 转换脚本 ──▶ 统一 YOLO 格式
                     │
标注员 C（CVAT）─────┘
```

**步骤**：
1. 所有标注员使用相同的 `classes.txt`
2. 各自使用喜欢的工具标注
3. 定期运行转换脚本统一格式
4. 合并到统一的 YOLO 格式目录

### 4.2 质量控制

#### 转换后验证

```bash
# 检查转换后的文件
python src/scripts/verify_annotations.py \
  --input data/annotations/yolo_format/train \
  --images data/raw/images
```

**检查项**：
- ✅ 坐标是否在 [0, 1] 范围内
- ✅ 类别 ID 是否有效
- ✅ 标注文件是否与图像一一对应
- ✅ 是否有空标注文件

### 4.3 版本管理

#### Git 策略

```bash
# ✅ 上传：标注文档、工具、配置
git add data/annotations/README.md
git add data/annotations/classes.txt
git add data/annotations/data.yaml
git add src/scripts/convert_annotations.py

# ❌ 不上传：标注结果数据
# data/annotations/yolo_format/ 已在 .gitignore 中
```

#### 备份策略

```
标注数据备份：
├── 本地备份：H:/backup/annotations_20260403/
├── 云端备份：私有云/标注数据/
└── 移动硬盘：/annotations_backup/
```

### 4.4 常见问题解决

#### Q1: 不同工具标注的边界框有差异怎么办？

**A**: 
- 这是正常现象，不同工具的标注习惯不同
- 关键是使用统一的类别定义
- 转换脚本会处理坐标归一化

#### Q2: LabelMe 的多边形如何转换为矩形框？

**A**: 
- 转换脚本会自动计算多边形的最小外接矩形
- 使用 `convert_annotations.py` 的默认行为

#### Q3: 如何合并多个标注员的标注结果？

**A**: 
```bash
# 1. 各自标注完成后，转换到统一格式
python convert_annotations.py --input annotator_A/ --output merged/ --format labelme
python convert_annotations.py --input annotator_B/ --output merged/ --format labelme

# 2. 检查重复标注
python src/scripts/check_duplicates.py --input merged/

# 3. 手动检查冲突区域
```

#### Q4: 坐标系统不一致怎么办？

**A**: 
- LabelImg/YOLO：归一化坐标 (0-1)
- LabelMe：像素坐标
- VOC：像素坐标
- COCO：像素坐标 [x_min, y_min, width, height]

转换脚本会自动处理所有坐标系统！

---

## 5. 工具配置模板

### LabelImg 配置

**位置**：`data/annotations/classes.txt`

```
0 garbage
1 illegal_construction
2 illegal_discharge
3 floating_debris
4 bank_damage
5 other
```

**设置**：
1. 打开 LabelImg
2. `Change Save Dir` → `data/annotations/yolo_format/train`
3. 选择 `YOLO` 格式
4. 确保 `classes.txt` 在同一目录

### LabelMe 配置

**位置**：`data/annotations/labelme_classes.txt`

```json
{
  "garbage": 0,
  "illegal_construction": 1,
  "illegal_discharge": 2,
  "floating_debris": 3,
  "bank_damage": 4,
  "other": 5
}
```

### CVAT 配置

**标签文件**：`data/annotations/cvat_labels.xml`

```xml
<labels>
  <label name="garbage" color="#FF0000"/>
  <label name="illegal_construction" color="#00FF00"/>
  <label name="illegal_discharge" color="#0000FF"/>
  <label name="floating_debris" color="#FFFF00"/>
  <label name="bank_damage" color="#FF00FF"/>
  <label name="other" color="#00FFFF"/>
</labels>
```

---

## 6. 完整工作流程

### 6.1 单人标注流程

```
1. 准备阶段
   ↓
   加载 classes.txt
   ↓
2. 标注阶段
   ↓
   LabelImg 标注 → 保存为 YOLO 格式
   ↓
3. 检查阶段
   ↓
   自检 → 质量检查表
   ↓
4. 完成
   ↓
   data/annotations/yolo_format/train/
```

### 6.2 团队协作流程

```
1. 准备阶段
   ↓
   分发 classes.txt 给所有标注员
   ↓
2. 标注阶段（并行）
   ↓
   标注员 A（LabelImg）──┐
   标注员 B（LabelMe）───┼──▶ 定期合并
   标注员 C（CVAT）─────┘
   ↓
3. 转换阶段
   ↓
   运行 convert_annotations.py 统一格式
   ↓
4. 质检阶段
   ↓
   交叉检查 → 专检 → 修改
   ↓
5. 完成
   ↓
   data/annotations/yolo_format/train/
```

---

## 7. 总结

### ✅ 多工具协同的优势

1. **灵活性**：标注员可以选择喜欢的工具
2. **专业性**：不同场景使用最适合的工具
3. **效率**：发挥各工具的优势

### ✅ 格式统一的保障

1. **统一类别定义**：`classes.txt`
2. **自动转换工具**：`convert_annotations.py`
3. **质量检查**：验证脚本
4. **文档规范**：本指南

### ⚠️ 注意事项

1. 所有标注员必须使用相同的类别定义
2. 定期运行转换脚本统一格式
3. 转换后必须验证数据质量
4. 标注结果数据不上传到 GitHub

---

**相关文档**：
- [标注指南](ANNOTATION_GUIDE.md)
- [标注工具使用](ANNOTATION_TOOLS.md)
- [转换脚本使用](../../src/scripts/convert_annotations.py)

**维护者**：taotie111  
**最后更新**：2026-04-03
