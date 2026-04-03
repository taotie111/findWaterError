# 标注系统完整指南

**创建时间**：2026-04-03  
**状态**：✅ 完成

---

## ✅ 已创建的文件和文件夹

### 📖 文档类

| 文件 | 位置 | 说明 |
|------|------|------|
| **标注指南** | `docs/ANNOTATION_GUIDE.md` | 6 类水体问题详细定义、标注规范、质量检查标准 |
| **标注工具使用** | `docs/ANNOTATION_TOOLS.md` | LabelImg、LabelMe、CVAT 使用教程 |
| **标注目录说明** | `data/annotations/README.md` | 标注文件夹结构说明 |

### 📁 标注文件夹结构

```
data/annotations/
├── README.md                      ✅ 目录说明
├── classes.txt                    ✅ 类别文件（6 类）
├── data.yaml                      ✅ 数据集配置
├── annotation_template.md         ✅ 标注模板
├── quality_checklist.md           ✅ 质量检查表
│
├── yolo_format/                   ✅ YOLO 格式标注
│   ├── train/                     ✅ 训练集
│   ├── val/                       ✅ 验证集
│   └── test/                      ✅ 测试集
│
├── labelme_jsons/                 ✅ LabelMe 备份
│   ├── train/
│   ├── val/
│   └── test/
│
└── voc_xml/                       ✅ VOC 备份
    ├── train/
    ├── val/
    └── test/
```

### 🛠️ 工具脚本

| 脚本 | 位置 | 功能 |
|------|------|------|
| **格式转换工具** | `src/scripts/convert_annotations.py` | LabelMe/VOC/COCO → YOLO |

---

## 📊 6 类水体问题

| ID | 类别名称 | 中文名称 | 说明 |
|----|---------|---------|------|
| 0 | garbage | 垃圾 | 水面漂浮垃圾 |
| 1 | illegal_construction | 违建 | 违章建筑 |
| 2 | illegal_discharge | 排污 | 违法排污 |
| 3 | floating_debris | 漂浮物 | 水面漂浮物 |
| 4 | bank_damage | 岸坡破坏 | 岸坡植被破坏 |
| 5 | other | 其他 | 其他问题 |

---

## 🚀 快速开始标注

### 步骤 1：准备标注工具

```bash
# 安装 LabelImg
pip install labelImg
labelImg
```

### 步骤 2：加载类别文件

在 LabelImg 中：
1. 点击 `Change Save Dir` → 选择 `data/annotations/yolo_format/train`
2. 确保 `classes.txt` 文件存在
3. 选择 YOLO 格式

### 步骤 3：开始标注

1. 点击 `Open Dir` 打开图像文件夹
2. 按 `W` 创建边界框
3. 选择类别
4. 按 `Ctrl+S` 保存
5. 按 `D` 下一张图像

### 步骤 4：质量检查

使用 `quality_checklist.md`：
- 自检
- 互检
- 专检

---

## 📝 标注规范要点

### ✅ 正确做法

1. **边界框紧密贴合目标**
2. **类别选择准确**
3. **不遗漏任何目标**
4. **特殊情况添加备注**

### ❌ 错误做法

1. 边界框过大（包含过多背景）
2. 边界框过小（未包含完整目标）
3. 类别选择错误
4. 遗漏目标

---

## 🔄 标注格式转换

### LabelMe JSON → YOLO

```bash
python src/scripts/convert_annotations.py \
  --input data/annotations/labelme_jsons \
  --output data/annotations/yolo_format/train \
  --format labelme
```

### VOC XML → YOLO

```bash
python src/scripts/convert_annotations.py \
  --input data/annotations/voc_xml \
  --output data/annotations/yolo_format/train \
  --format voc
```

### COCO JSON → YOLO

```bash
python src/scripts/convert_annotations.py \
  --input data/annotations/coco/annotations.json \
  --output data/annotations/yolo_format/train \
  --format coco
```

---

## 📋 质量检查标准

| 指标 | 目标值 | 检查方法 |
|------|--------|---------|
| 标注准确率 | ≥95% | 正确标注数 / 总标注数 |
| 漏检率 | ≤5% | 漏检目标数 / 实际目标数 |
| 误检率 | ≤3% | 误检目标数 / 总标注数 |
| 类别准确率 | ≥98% | 正确类别数 / 总标注数 |

---

## 💡 最佳实践

### 标注前

1. ✅ 熟悉标注类别定义
2. ✅ 检查图像质量
3. ✅ 准备标注工具
4. ✅ 加载正确的类别文件

### 标注中

1. ✅ 边界框紧密贴合
2. ✅ 类别选择准确
3. ✅ 不遗漏目标
4. ✅ 特殊情况添加备注

### 标注后

1. ✅ 自检
2. ✅ 互检
3. ✅ 专检
4. ✅ 修改不合格标注

---

## ⚠️ 重要提示

### 数据安全

- ❌ **不要上传标注数据到 GitHub**（已在 `.gitignore` 中排除）
- ✅ 定期备份到外部硬盘或私有云
- ✅ 敏感信息需要脱敏处理

### 版本控制

- ✅ 标注文档上传到 GitHub
- ❌ 标注数据不上传
- ✅ 使用标签管理标注版本

---

## 🔗 相关文档

### 标注相关
- [标注指南](ANNOTATION_GUIDE.md) - 详细标注规范
- [标注工具使用](ANNOTATION_TOOLS.md) - 工具教程
- [标注目录说明](../data/annotations/README.md) - 文件夹结构

### 其他文档
- [环境配置](ENVIRONMENT.md) - 环境说明
- [目录结构](DIRECTORY_STRUCTURE.md) - 项目结构
- [配置总结](CONFIG_SUMMARY.md) - 配置说明

---

## 📞 联系方式

- **GitHub**: [@taotie111](https://github.com/taotie111)
- **问题反馈**: [Issues](https://github.com/taotie111/findWaterError/issues)

---

**维护者**：taotie111  
**最后更新**：2026-04-03
