# ============================================================
# 目录结构迁移脚本
# ============================================================
# 将现有文件迁移到新的模块化结构
# ============================================================

import os
import shutil
from pathlib import Path

# 根目录
ROOT = Path(r"H:\code\01_image_center")

# 需要创建的新目录
NEW_DIRS = [
    "configs",
    "src/data",
    "src/models",
    "src/training",
    "src/utils",
    "src/scripts",
    "notebooks",
    "data/raw/images",
    "data/raw/excel",
    "data/processed/train",
    "data/processed/val",
    "data/processed/test",
    "data/annotations/yolo_format",
    "data/annotations/coco_format",
    "runs/dinov2",
    "runs/yolov8",
    "runs/yolov10",
    "runs/yolo-se",
    "weights/dinov2",
    "weights/yolov8",
    "weights/yolov10",
    "weights/yolo-se",
    "docs",
    "tests",
]

print("=" * 80)
print("开始迁移目录结构")
print("=" * 80)

# 1. 创建新目录
print("\n[1/4] 创建新目录结构...")
for dir_name in NEW_DIRS:
    dir_path = ROOT / dir_name
    dir_path.mkdir(parents=True, exist_ok=True)
    print(f"  [OK] {dir_name}/")

# 2. 移动文件
print("\n[2/4] 移动文件到新位置...")

# 移动 Notebook 到 notebooks/
notebooks = list(ROOT.glob("*.ipynb"))
for nb in notebooks:
    dest = ROOT / "notebooks" / nb.name
    shutil.move(str(nb), str(dest))
    print(f"  [NB] {nb.name} -> notebooks/")

# 移动 Python 脚本到 src/scripts/
py_scripts = list(ROOT.glob("*.py"))
for script in py_scripts:
    if script.name not in ["__init__.py"]:  # 跳过可能的 init 文件
        dest = ROOT / "src" / "scripts" / script.name
        shutil.move(str(script), str(dest))
        print(f"  [PY] {script.name} -> src/scripts/")

# 移动文档到 docs/
md_files = [f for f in ROOT.glob("*.md") if f.name not in ["README.md"]]
for md in md_files:
    dest = ROOT / "docs" / md.name
    shutil.move(str(md), str(dest))
    print(f"  [MD] {md.name} -> docs/")

# 移动 batch 脚本到 src/scripts/
bat_files = list(ROOT.glob("*.bat"))
for bat in bat_files:
    dest = ROOT / "src" / "scripts" / bat.name
    shutil.move(str(bat), str(dest))
    print(f"  [BAT] {bat.name} -> src/scripts/")

# 3. 移动数据目录
print("\n[3/4] 重组数据目录...")

# 移动现有的 data/ 到 data/raw/
old_data = ROOT / "data"
if old_data.exists():
    # 移动 images
    old_images = old_data / "images"
    if old_images.exists():
        new_images = ROOT / "data" / "raw" / "images"
        if new_images.exists():
            shutil.rmtree(new_images)
        shutil.move(str(old_images), str(new_images))
        print(f"  [IMG] images/ -> data/raw/images/")
    
    # 移动 labels 到 annotations
    old_labels = old_data / "labels"
    if old_labels.exists():
        new_annotations = ROOT / "data" / "annotations" / "yolo_format"
        if new_annotations.exists():
            shutil.rmtree(new_annotations)
        shutil.move(str(old_labels), str(new_annotations))
        print(f"  [LBL] labels/ -> data/annotations/yolo_format/")
    
    # 移动 data.yaml 到 configs/
    data_yaml = old_data / "data.yaml"
    if data_yaml.exists():
        dest = ROOT / "configs" / "data.yaml"
        shutil.move(str(data_yaml), str(dest))
        print(f"  [CFG] data.yaml -> configs/")

# 移动 excel/ 到 data/raw/excel/
old_excel = ROOT / "excel"
if old_excel.exists():
    new_excel = ROOT / "data" / "raw" / "excel"
    if new_excel.exists():
        shutil.rmtree(new_excel)
    shutil.move(str(old_excel), str(new_excel))
    print(f"  [XLS] excel/ -> data/raw/excel/")

# 4. 重组 runs/ 目录
print("\n[4/4] 重组训练输出目录...")
old_runs = ROOT / "runs" / "finetune"
if old_runs.exists():
    new_runs = ROOT / "runs" / "dinov2" / "exp1"
    new_runs.mkdir(parents=True, exist_ok=True)
    
    # 移动文件
    for file in old_runs.iterdir():
        dest = new_runs / file.name
        shutil.move(str(file), str(dest))
        print(f"  [RUN] {file.name} -> runs/dinov2/exp1/")
    
    # 删除旧的 finetune 文件夹
    old_runs.rmdir()

# 5. 创建 __init__.py 文件
print("\n[5/5] 创建 Python 包结构...")
init_dirs = ["src", "src/data", "src/models", "src/training", "src/utils", "src/scripts", "tests"]
for dir_name in init_dirs:
    init_file = ROOT / dir_name / "__init__.py"
    init_file.write_text("")
    print(f"  [INIT] {dir_name}/__init__.py")

print("\n" + "=" * 80)
print("✅ 迁移完成！")
print("=" * 80)

print("\n新的目录结构:")
print("""
findWaterError/
├── configs/              # 配置文件
├── src/                  # 源代码
│   ├── data/            # 数据处理
│   ├── models/          # 模型定义
│   ├── training/        # 训练代码
│   ├── utils/           # 工具函数
│   └── scripts/         # 可执行脚本
├── notebooks/           # Jupyter Notebooks
├── data/                # 数据（已排除）
│   ├── raw/            # 原始数据
│   ├── processed/      # 处理后数据
│   └── annotations/    # 标注文件
├── runs/                # 训练输出（已排除）
│   ├── dinov2/
│   ├── yolov8/
│   ├── yolov10/
│   └── yolo-se/
├── docs/                # 文档
└── tests/               # 测试
""")

print("\n下一步:")
print("1. 更新 .gitignore 确保新结构被正确排除")
print("2. 重构代码以使用新的模块化结构")
print("3. 创建统一的训练入口脚本")
