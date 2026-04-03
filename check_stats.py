from pathlib import Path

root = Path('H:/code/01_image_center/data/images/raw')
print('数据集统计:\n')

total = 0
for d in sorted(root.iterdir()):
    if d.is_dir():
        imgs = list(d.glob('*.png')) + list(d.glob('*.jpg'))
        print(f'  {d.name}: {len(imgs)} 张')
        total += len(imgs)

print(f'\n总计：{total} 张')
