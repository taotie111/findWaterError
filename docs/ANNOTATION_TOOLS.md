# 标注工具使用指南

**最后更新**：2026-04-03

---

## 📋 目录

1. [LabelImg 使用指南](#1-labelimg-使用指南)
2. [LabelMe 使用指南](#2-labelme-使用指南)
3. [CVAT 使用指南](#3-cvat-使用指南)
4. [标注格式转换](#4-标注格式转换)

---

## 1. LabelImg 使用指南

### 1.1 安装

```bash
# 方法 1：pip 安装（推荐）
pip install labelImg
labelImg

# 方法 2：源码安装
git clone https://github.com/heartexlabs/labelImg.git
cd labelImg
pip install -r requirements.txt
python labelImg.py
```

### 1.2 快速开始

1. **启动 LabelImg**
   ```bash
   labelImg
   ```

2. **设置保存目录**
   - 点击左侧工具栏的 `Change Save Dir` 按钮
   - 选择标注文件保存路径（建议：`data/annotations/yolo_format/train`）

3. **加载图像**
   - 点击 `Open Dir` 打开图像文件夹
   - 或使用 `Open` 打开单张图像

4. **绘制边界框**
   - 点击 `Create RectBox` 或按 `W` 键
   - 在图像上拖动鼠标绘制边界框
   - 选择类别（从下拉列表）
   - 按 `Ctrl+S` 保存

5. **切换类别**
   - 使用右侧的类别列表
   - 或双击已绘制的边界框修改类别

6. **导航**
   - `D`：下一张图像
   - `A`：上一张图像
   - `Del`：删除选中的边界框

### 1.3 快捷键

| 快捷键 | 功能 |
|--------|------|
| `W` | 创建边界框 |
| `D` | 下一张图像 |
| `A` | 上一张图像 |
| `S` | 保存当前图像 |
| `Ctrl+S` | 保存 |
| `Del` | 删除选中的框 |
| `Ctrl+D` | 复制选中的框 |
| `Ctrl++` | 放大图像 |
| `Ctrl+-` | 缩小图像 |
| `↑` `↓` `←` `→` | 移动图像 |

### 1.4 配置 YOLO 格式

1. 打开 LabelImg
2. 点击左侧的 `PascalVOC` 按钮
3. 选择 `YOLO` 格式
4. 确保 `classes.txt` 文件在保存目录中

**classes.txt 内容**：
```
0 garbage
1 illegal_construction
2 illegal_discharge
3 floating_debris
4 bank_damage
5 other
```

### 1.5 导出格式

**YOLO 格式示例**（`.txt` 文件）：
```
# image1.txt
0 0.456 0.678 0.123 0.234
1 0.234 0.345 0.456 0.567
```

**格式说明**：
- 每行一个目标
- 格式：`<class_id> <x_center> <y_center> <width> <height>`
- 坐标已归一化到 [0, 1]

---

## 2. LabelMe 使用指南

### 2.1 安装

```bash
# pip 安装
pip install labelme
labelme

# 或创建独立环境
conda create -n labelme python=3.8
conda activate labelme
pip install labelme
```

### 2.2 快速开始

1. **启动 LabelMe**
   ```bash
   labelme
   ```

2. **创建新标注**
   - 点击 `File` → `Open Dir` 打开图像文件夹
   - 点击 `Create` → `Polygons` 创建多边形
   - 或点击 `Create` → `Rectangles` 创建矩形框

3. **选择类别**
   - 在弹出的对话框中输入类别名称
   - 或使用预定义的类别列表

4. **保存**
   - `File` → `Save` 保存标注
   - 或使用快捷键 `Ctrl+S`

### 2.3 导出为 YOLO 格式

LabelMe 默认保存为 JSON 格式，需要转换为 YOLO 格式：

```bash
# 使用转换脚本
python scripts/convert_labelme_to_yolo.py \
  --input data/annotations/labelme_jsons \
  --output data/annotations/yolo_format
```

---

## 3. CVAT 使用指南

### 3.1 在线版本

1. **访问**：https://app.cvat.ai/
2. **注册/登录**
3. **创建项目**
   - 项目名称：findWaterError
   - 任务类型：Object Detection
4. **创建任务**
   - 上传图像
   - 设置标签（6 个类别）
5. **开始标注**
   - 使用矩形框工具
   - 选择对应类别
6. **导出数据**
   - 选择 YOLO 格式
   - 下载标注文件

### 3.2 本地部署

```bash
# 使用 Docker 部署
docker-compose up -d

# 访问 http://localhost:8080
```

详细文档：https://docs.cvat.ai/

---

## 4. 标注格式转换

### 4.1 LabelMe JSON → YOLO

```python
# scripts/convert_labelme_to_yolo.py
import json
import os
from pathlib import Path

def convert_labelme_to_yolo(json_file, output_dir, img_size):
    """
    将 LabelMe JSON 格式转换为 YOLO 格式
    
    参数:
        json_file: LabelMe JSON 文件路径
        output_dir: 输出目录
        img_size: 图像尺寸 (width, height)
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    output_file = Path(output_dir) / Path(json_file).stem + '.txt'
    
    with open(output_file, 'w') as f:
        for shape in data['shapes']:
            label = shape['label']
            points = shape['points']
            
            # 将类别名称转换为 ID
            class_id = label_to_id(label)
            
            # 计算边界框（矩形框）
            x_min = min(p[0] for p in points)
            y_min = min(p[1] for p in points)
            x_max = max(p[0] for p in points)
            y_max = max(p[1] for p in points)
            
            # 转换为 YOLO 格式（归一化）
            x_center = (x_min + x_max) / 2 / img_size[0]
            y_center = (y_min + y_max) / 2 / img_size[1]
            width = (x_max - x_min) / img_size[0]
            height = (y_max - y_min) / img_size[1]
            
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

def label_to_id(label):
    """类别名称转 ID"""
    label_map = {
        'garbage': 0,
        'illegal_construction': 1,
        'illegal_discharge': 2,
        'floating_debris': 3,
        'bank_damage': 4,
        'other': 5
    }
    return label_map.get(label.lower(), 5)

# 使用示例
if __name__ == '__main__':
    convert_labelme_to_yolo(
        'data/annotations/labelme_jsons/image1.json',
        'data/annotations/yolo_format/train',
        (1920, 1080)
    )
```

### 4.2 VOC XML → YOLO

```python
# scripts/convert_voc_to_yolo.py
import xml.etree.ElementTree as ET
from pathlib import Path

def convert_voc_to_yolo(xml_file, output_dir, img_size):
    """将 VOC XML 格式转换为 YOLO 格式"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    output_file = Path(output_dir) / Path(xml_file).stem + '.txt'
    
    with open(output_file, 'w') as f:
        for obj in root.findall('object'):
            label = obj.find('name').text
            bbox = obj.find('bndbox')
            
            # 获取边界框坐标
            x_min = float(bbox.find('xmin').text)
            y_min = float(bbox.find('ymin').text)
            x_max = float(bbox.find('xmax').text)
            y_max = float(bbox.find('ymax').text)
            
            # 转换为 YOLO 格式
            class_id = label_to_id(label)
            x_center = (x_min + x_max) / 2 / img_size[0]
            y_center = (y_min + y_max) / 2 / img_size[1]
            width = (x_max - x_min) / img_size[0]
            height = (y_max - y_min) / img_size[1]
            
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
```

---

## 5. 标注项目管理

### 5.1 项目结构

```
annotation_project/
├── raw_images/              # 原始图像
├── annotations/
│   ├── yolo_format/        # YOLO 格式标注
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   ├── labelme_jsons/      # LabelMe JSON（备份）
│   └── voc_xml/            # VOC XML（备份）
├── classes.txt             # 类别文件
├── data.yaml              # 数据集配置
└── quality_checks/        # 质量检查记录
```

### 5.2 标注进度跟踪

使用 Excel 或在线表格跟踪：

| 图像名称 | 标注人员 | 标注日期 | 质检状态 | 备注 |
|---------|---------|---------|---------|------|
| image1.jpg | 张三 | 2026-04-01 | ✅ 通过 | |
| image2.jpg | 李四 | 2026-04-01 | ⚠️ 待修改 | 边界框过大 |
| image3.jpg | 张三 | 2026-04-02 | ✅ 通过 | |

---

## 6. 最佳实践

### 6.1 标注前准备

1. ✅ 熟悉标注类别定义
2. ✅ 检查图像质量
3. ✅ 准备标注工具
4. ✅ 加载正确的类别文件

### 6.2 标注中注意事项

1. ✅ 边界框紧密贴合目标
2. ✅ 类别选择准确
3. ✅ 不遗漏任何目标
4. ✅ 特殊情况添加备注

### 6.3 标注后检查

1. ✅ 自检：检查所有标注
2. ✅ 互检：交叉检查
3. ✅ 专检：质检员检查
4. ✅ 修改不合格标注

---

## 7. 常见问题

### Q1: LabelImg 无法保存 YOLO 格式？

**A**: 确保 `classes.txt` 文件在保存目录中，并且格式正确。

### Q2: 如何批量转换标注格式？

**A**: 使用提供的转换脚本，或使用在线转换工具。

### Q3: 标注文件打不开？

**A**: 检查文件编码，确保使用 UTF-8 编码。

---

**文档维护**：taotie111  
**反馈问题**：https://github.com/taotie111/findWaterError/issues
