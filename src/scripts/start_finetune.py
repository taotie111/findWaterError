#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DINOv2 轻量微调训练（RTX 3060 优化版）
======================================
预期时间：15-20 小时
预期准确率：85-88%
"""

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
from PIL import Image
import numpy as np
from datetime import datetime
import os

# 设置 UTF-8
import sys
sys.stdout.reconfigure(encoding='utf-8')

class WaterProblemDataset(Dataset):
    """水利问题数据集"""
    
    def __init__(self, root_dir, transform=None, max_samples=None):
        self.root_dir = Path(root_dir)
        self.transform = transform
        self.samples = []
        self.labels = []
        self.label_map = {}
        
        # 类别映射
        categories = ['垃圾', '违建', '排污', '漂浮物', '岸坡破坏', '其他']
        for idx, cat in enumerate(categories):
            self.label_map[cat] = idx
        
        # 收集所有样本
        print("加载数据集...")
        total = 0
        for cat_dir in self.root_dir.iterdir():
            if cat_dir.is_dir() and cat_dir.name in self.label_map:
                for img_path in cat_dir.glob('*.png'):
                    self.samples.append(img_path)
                    self.labels.append(self.label_map[cat_dir.name])
                    total += 1
                    if max_samples and total >= max_samples:
                        break
                if max_samples and total >= max_samples:
                    break
        
        print(f"  总样本数：{len(self.samples)}")
        print(f"  类别数：{len(self.label_map)}")
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path = self.samples[idx]
        label = self.labels[idx]
        
        try:
            image = Image.open(img_path).convert('RGB')
            
            # 简单的预处理
            image = image.resize((518, 518))
            image_array = np.array(image).astype(np.float32)
            
            # 归一化
            mean = np.array([0.485, 0.456, 0.406])
            std = np.array([0.229, 0.224, 0.225])
            image_array = (image_array / 255.0 - mean) / std
            
            # HWC -> CHW
            image_array = np.transpose(image_array, (2, 0, 1))
            
            return torch.tensor(image_array, dtype=torch.float32), label
            
        except Exception as e:
            # 返回空白图像
            blank = np.zeros((3, 518, 518), dtype=np.float32)
            return torch.tensor(blank), label

def main():
    """主训练函数"""
    print("=" * 80)
    print("DINOv2 轻量微调训练")
    print("=" * 80)
    print(f"\n开始时间：{datetime.now()}")
    
    # 配置
    DATA_ROOT = Path(r"H:\code\01_image_center\data\images\raw")
    OUTPUT_DIR = Path(r"H:\code\01_image_center\runs\finetune")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # RTX 3060 优化配置
    BATCH_SIZE = 1
    GRADIENT_ACCUMULATION = 8  # 等效 batch=8
    EPOCHS = 20
    LEARNING_RATE = 1e-5
    FROZEN_LAYERS = 20  # 冻结前 20 层
    
    print(f"\n[配置]")
    print(f"  数据路径：{DATA_ROOT}")
    print(f"  输出路径：{OUTPUT_DIR}")
    print(f"  批次大小：{BATCH_SIZE} (累积 {GRADIENT_ACCUMULATION} 步)")
    print(f"  训练轮数：{EPOCHS}")
    print(f"  学习率：{LEARNING_RATE}")
    print(f"  冻结层数：{FROZEN_LAYERS}")
    
    # 检查 GPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\n[设备] {device}")
    if torch.cuda.is_available():
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        print(f"  显存：{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    # 加载数据
    print(f"\n[1] 加载数据集...")
    dataset = WaterProblemDataset(DATA_ROOT)
    
    # 划分训练集和验证集
    from sklearn.model_selection import train_test_split
    train_indices, val_indices = train_test_split(
        range(len(dataset)),
        test_size=0.2,
        random_state=42,
        stratify=[dataset.labels[i] for i in range(len(dataset))]
    )
    
    train_dataset = torch.utils.data.Subset(dataset, train_indices)
    val_dataset = torch.utils.data.Subset(dataset, val_indices)
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)
    
    print(f"  训练集：{len(train_dataset)} 样本")
    print(f"  验证集：{len(val_dataset)} 样本")
    
    # 加载 DINOv2 模型
    print(f"\n[2] 加载 DINOv2 模型...")
    try:
        from transformers import Dinov2Model
        model = Dinov2Model.from_pretrained('facebook/dinov2-large')
        print(f"  ✅ 模型加载成功")
    except Exception as e:
        print(f"  ❌ 加载失败：{e}")
        return
    
    # 冻结前 N 层
    total_layers = len(model.encoder.layer)
    print(f"  总层数：{total_layers}")
    print(f"  冻结前 {FROZEN_LAYERS} 层")
    
    for i, layer in enumerate(model.encoder.layer):
        if i < FROZEN_LAYERS:
            for param in layer.parameters():
                param.requires_grad = False
        else:
            for param in layer.parameters():
                param.requires_grad = True
    
    # 添加分类头
    embed_dim = model.config.hidden_size
    num_classes = len(dataset.label_map)
    
    classifier = nn.Sequential(
        nn.Linear(embed_dim, 256),
        nn.GELU(),
        nn.Dropout(0.1),
        nn.Linear(256, num_classes)
    )
    
    model = model.to(device)
    classifier = classifier.to(device)
    
    # 优化器
    optimizer = torch.optim.AdamW([
        {'params': model.parameters(), 'lr': LEARNING_RATE},
        {'params': classifier.parameters(), 'lr': LEARNING_RATE * 10}
    ], weight_decay=0.05)
    
    # 损失函数
    criterion = nn.CrossEntropyLoss()
    
    # 训练循环
    print(f"\n[3] 开始训练...")
    print(f"  预计时间：15-20 小时")
    
    best_acc = 0
    train_log = []
    
    for epoch in range(1, EPOCHS + 1):
        epoch_start = datetime.now()
        
        # 训练
        model.train()
        classifier.train()
        
        total_loss = 0
        correct = 0
        total = 0
        
        optimizer.zero_grad()
        
        for batch_idx, (images, labels) in enumerate(train_loader):
            images = images.to(device)
            labels = labels.to(device)
            
            # 前向传播
            outputs = model(images)
            features = outputs.last_hidden_state[:, 0, :]  # CLS token
            logits = classifier(features)
            
            # 计算损失
            loss = criterion(logits, labels) / GRADIENT_ACCUMULATION
            loss.backward()
            
            # 更新权重
            if (batch_idx + 1) % GRADIENT_ACCUMULATION == 0:
                optimizer.step()
                optimizer.zero_grad()
            
            # 统计
            total_loss += loss.item() * GRADIENT_ACCUMULATION
            _, predicted = logits.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            # 进度
            if (batch_idx + 1) % 100 == 0:
                progress = (batch_idx + 1) / len(train_loader) * 100
                acc = 100. * correct / total
                print(f"  Epoch {epoch} [{progress:.1f}%] Loss: {total_loss/(batch_idx+1):.4f} Acc: {acc:.2f}%")
        
        # 验证
        model.eval()
        classifier.eval()
        
        val_loss = 0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                labels = labels.to(device)
                
                outputs = model(images)
                features = outputs.last_hidden_state[:, 0, :]
                logits = classifier(features)
                
                loss = criterion(logits, labels)
                val_loss += loss.item()
                
                _, predicted = logits.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()
        
        val_acc = 100. * val_correct / val_total
        epoch_time = (datetime.now() - epoch_start).total_seconds() / 60
        
        print(f"\n[Epoch {epoch}/{EPOCHS}]")
        print(f"  训练损失：{total_loss/len(train_loader):.4f}")
        print(f"  训练准确率：{100. * correct / total:.2f}%")
        print(f"  验证准确率：{val_acc:.2f}%")
        print(f"  用时：{epoch_time:.1f} 分钟")
        
        train_log.append({
            'epoch': epoch,
            'train_loss': total_loss/len(train_loader),
            'train_acc': 100. * correct / total,
            'val_acc': val_acc,
            'time': epoch_time
        })
        
        # 保存最佳模型
        if val_acc > best_acc:
            best_acc = val_acc
            print(f"  ✅ 新最佳模型！验证准确率：{best_acc:.2f}%")
            
            # 保存模型
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'classifier_state_dict': classifier.state_dict(),
                'val_acc': val_acc,
                'label_map': dataset.label_map
            }, OUTPUT_DIR / 'best_model.pth')
        
        # 保存训练日志
        import json
        with open(OUTPUT_DIR / 'training_log.json', 'w', encoding='utf-8') as f:
            json.dump(train_log, f, ensure_ascii=False, indent=2)
    
    # 训练完成
    print(f"\n{'='*80}")
    print("训练完成!")
    print(f"{'='*80}")
    print(f"\n最佳验证准确率：{best_acc:.2f}%")
    print(f"模型保存位置：{OUTPUT_DIR / 'best_model.pth'}")
    print(f"\n结束时间：{datetime.now()}")
    
    if best_acc >= 85:
        print(f"\n✅ 优秀！验证准确率 >= 85%")
        print(f"   建议：可以在 A6000 上进行完整训练")
    elif best_acc >= 75:
        print(f"\n⭕ 良好！验证准确率 >= 75%")
        print(f"   建议：可以继续优化或增加数据")
    else:
        print(f"\n❌ 一般！验证准确率 < 75%")
        print(f"   建议：检查数据质量或调整超参数")

if __name__ == "__main__":
    main()
