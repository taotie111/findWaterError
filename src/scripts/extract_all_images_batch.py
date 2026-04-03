#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量提取所有 Excel 中的图片 + 复制模型数据集
============================================
目标：提取 10000+ 张图片
"""

import openpyxl
from pathlib import Path
import shutil
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

def simplify_category(category_name):
    """简化类别名称"""
    if not isinstance(category_name, str):
        return '其他'
    
    mappings = {
        '垃圾': '垃圾',
        '建筑垃圾': '垃圾',
        '生活垃圾': '垃圾',
        '违建': '违建',
        '乱堆乱搭': '违建',
        '违章建筑': '违建',
        '排污': '排污',
        '污水': '排污',
        '漂浮': '漂浮物',
        '漂浮物': '漂浮物',
        '岸坡': '岸坡破坏',
        '堤防': '岸坡破坏',
    }
    
    for keyword, category in mappings.items():
        if keyword in category_name:
            return category
    
    return '其他'

def extract_from_excel(excel_files, output_root, max_total=10000):
    """从 Excel 文件中批量提取图片"""
    
    print("=" * 80)
    print("批量 Excel 图片提取")
    print("=" * 80)
    print(f"\n[时间] {datetime.now()}")
    print(f"Excel 文件数：{len(excel_files)}")
    print(f"目标提取：{max_total} 张\n")
    
    # 创建类别文件夹
    categories = ['垃圾', '违建', '排污', '漂浮物', '岸坡破坏', '其他']
    for cat in categories:
        (output_root / cat).mkdir(parents=True, exist_ok=True)
    
    stats = {
        'files_processed': 0,
        'images_extracted': 0,
        'by_category': {cat: 0 for cat in categories}
    }
    
    # 处理每个 Excel 文件
    for idx, excel_file in enumerate(excel_files, 1):
        if stats['images_extracted'] >= max_total:
            print(f"\n[INFO] 已达到目标数量：{max_total}")
            break
        
        print(f"\n[{idx}/{len(excel_files)}] {excel_file.name}")
        
        try:
            wb = openpyxl.load_workbook(excel_file, data_only=True)
            sheet = wb.active
            
            # 提取图片
            if hasattr(sheet, '_images'):
                images = sheet._images
                print(f"  找到 {len(images)} 个图片")
                
                for img_idx, img_obj in enumerate(images):
                    if stats['images_extracted'] >= max_total:
                        break
                    
                    try:
                        img_data = img_obj._data()
                        if not img_data:
                            continue
                        
                        # 获取对应行的问题类型
                        row_num = img_idx + 2
                        cell = sheet.cell(row=row_num, column=9)
                        category_raw = str(cell.value) if cell.value else '其他'
                        category = simplify_category(category_raw)
                        
                        # 保存图片
                        filename = f"img_{stats['images_extracted']+1:06d}.png"
                        output_path = output_root / category / filename
                        
                        with open(output_path, 'wb') as f:
                            f.write(img_data)
                        
                        stats['images_extracted'] += 1
                        stats['by_category'][category] += 1
                        
                        if stats['images_extracted'] % 500 == 1:
                            print(f"    ✅ 已提取 {stats['images_extracted']} 张")
                    
                    except Exception as e:
                        continue
                
                stats['files_processed'] += 1
                
        except Exception as e:
            print(f"  ❌ 错误：{e}")
            continue
    
    return stats

def copy_model_dataset(model_path, output_root, max_copy=5000):
    """复制模型数据集的图片"""
    
    print("\n" + "=" * 80)
    print("复制湖面无塑检测数据集")
    print("=" * 80)
    
    model_path = Path(model_path)
    
    if not model_path.exists():
        print(f"❌ 路径不存在：{model_path}")
        return {'copied': 0}
    
    # 找到所有图片
    img_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    img_files = []
    
    for ext in img_extensions:
        img_files.extend(model_path.glob(f'*{ext}'))
        img_files.extend(model_path.glob(f'*{ext.upper()}'))
    
    print(f"\n找到图片：{len(img_files)} 张")
    
    # 复制到"漂浮物"类别（因为是湖面漂浮物）
    target_dir = output_root / '漂浮物'
    target_dir.mkdir(parents=True, exist_ok=True)
    
    stats = {'copied': 0}
    
    for idx, img_file in enumerate(img_files[:max_copy]):
        try:
            # 生成新文件名
            new_name = f"lake_{img_file.stem}.jpg"
            target_path = target_dir / new_name
            
            # 复制文件
            shutil.copy2(img_file, target_path)
            stats['copied'] += 1
            
            if stats['copied'] % 500 == 1:
                print(f"  已复制 {stats['copied']} 张")
        
        except Exception as e:
            continue
    
    print(f"\n✅ 复制完成：{stats['copied']} 张")
    
    return stats

def main():
    """主函数"""
    
    # 配置
    excel_root = Path(r"H:\code\01_image_center\excel")
    output_root = Path(r"H:\code\01_image_center\data\images\raw")
    model_dataset = r"H:\model\LakeFloatingPlasticWasteDetectionDataset\Raw_Images"
    
    # 收集所有 Excel 文件
    print("搜索 Excel 文件...")
    excel_files = []
    for subdir in excel_root.iterdir():
        if subdir.is_dir():
            for file in subdir.iterdir():
                if file.suffix == '.xlsx' and not file.name.startswith('~$'):
                    excel_files.append(file)
    
    excel_files.sort(key=lambda x: x.name)
    print(f"找到 {len(excel_files)} 个 Excel 文件\n")
    
    # 步骤 1：从 Excel 提取图片
    excel_stats = extract_from_excel(excel_files, output_root, max_total=10000)
    
    # 步骤 2：复制模型数据集
    model_stats = copy_model_dataset(model_dataset, output_root, max_copy=5000)
    
    # 步骤 3：统计结果
    print("\n" + "=" * 80)
    print("提取完成统计")
    print("=" * 80)
    
    print(f"\nExcel 提取:")
    print(f"  处理文件：{excel_stats['files_processed']} 个")
    print(f"  提取图片：{excel_stats['images_extracted']} 张")
    
    print(f"\n模型数据集复制:")
    print(f"  复制图片：{model_stats['copied']} 张")
    
    total = excel_stats['images_extracted'] + model_stats['copied']
    print(f"\n总计：{total} 张")
    
    # 显示类别分布
    print(f"\n类别分布:")
    categories = ['垃圾', '违建', '排污', '漂浮物', '岸坡破坏', '其他']
    for cat in categories:
        cat_dir = output_root / cat
        if cat_dir.exists():
            imgs = list(cat_dir.glob('*.png')) + list(cat_dir.glob('*.jpg'))
            print(f"  {cat}: {len(imgs)} 张")
    
    print(f"\n输出位置：{output_root}")
    print(f"\n[DONE] 完成!")

if __name__ == "__main__":
    main()
