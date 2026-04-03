# 系统环境配置说明

**最后更新**：2026-04-03  
**维护者**：taotie111

---

## 🖥️ 硬件配置

### GPU
- **型号**：NVIDIA GeForce RTX 3060
- **显存**：12 GB GDDR6
- **CUDA 核心数**：3584
- **GPU ID**：0

### 系统
- **操作系统**：Windows 10/11 (64 位)
- **CPU**：Intel/AMD (多核)
- **内存**：建议 16GB+

---

## 🔧 软件环境

### NVIDIA 驱动
- **驱动版本**：591.86
- **CUDA 版本**：13.1

### Python
- **版本**：3.13.5
- **发行版**：Anaconda, Inc.
- **架构**：64 位 (AMD64)

### PyTorch
- **版本**：2.6.0+cu124
- **CUDA 编译版本**：12.4
- **Torchvision**：0.21.0+cu124
- **Torchaudio**：2.6.0+cu124

> ⚠️ **注意**：PyTorch 使用 CUDA 12.4 编译，与系统 CUDA 13.1 向后兼容

---

## 📦 核心依赖包

### 深度学习框架
```
torch==2.6.0+cu124
torchvision==0.21.0+cu124
torchaudio==2.6.0+cu124
```

### Transformers (DINOv2)
```
transformers==4.48.0
huggingface-hub>=0.20.0
tokenizers>=0.15.0
safetensors>=0.4.0
```

### 数据处理
```
numpy>=2.0.0
pandas>=2.2.3
pillow>=11.1.0
matplotlib>=3.10.0
seaborn>=0.13.0
scikit-learn>=1.6.1
scikit-image>=0.25.0
```

### YOLO 系列
```
ultralytics>=8.3.0  # YOLOv8/YOLOv10
```

### 工具库
```
tqdm>=4.66.0
pyyaml>=6.0
tensorboard>=2.15.0
wandb>=0.16.0  # 可选
```

### Jupyter
```
jupyter>=1.0.0
jupyterlab>=4.0.0
notebook>=7.0.0
ipykernel>=6.0.0
```

---

## 🚀 安装步骤

### 1. 创建虚拟环境（推荐）

```bash
# 使用 conda
conda create -n findwater python=3.13
conda activate findwater

# 或使用 venv
python -m venv findwater_env
findwater_env\Scripts\activate
```

### 2. 安装 PyTorch（GPU 版本）

```bash
# 官方源（推荐）
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124

# 或使用 requirements.txt
pip install -r requirements.txt
```

### 3. 安装其他依赖

```bash
pip install -r requirements.txt
```

### 4. 国内镜像源（可选）

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## ✅ 验证安装

### 检查 PyTorch
```python
import torch
print(f"PyTorch: {torch.__version__}")
print(f"CUDA 可用：{torch.cuda.is_available()}")
print(f"CUDA 版本：{torch.version.cuda}")
print(f"GPU: {torch.cuda.get_device_name(0)}")
```

**预期输出**：
```
PyTorch: 2.6.0+cu124
CUDA 可用：True
CUDA 版本：12.4
GPU: NVIDIA GeForce RTX 3060
```

### 检查 Transformers
```python
import transformers
print(f"Transformers: {transformers.__version__}")
```

### 检查 Ultralytics (YOLO)
```python
import ultralytics
print(f"Ultralytics: {ultralytics.__version__}")
```

---

## 📊 显存使用参考

### DINOv2 微调
| 批次大小 | 显存占用 | 备注 |
|---------|---------|------|
| 1 | ~11 GB | 推荐 (RTX 3060) |
| 2 | ~15 GB | 需要梯度累积 |

### YOLOv8 训练
| 批次大小 | 显存占用 | 备注 |
|---------|---------|------|
| 8 | ~6 GB | 推荐 |
| 16 | ~8 GB | 可用 |
| 32 | ~10 GB | 接近上限 |

---

## ⚠️ 常见问题

### Q1: CUDA 版本不匹配
**问题**：系统 CUDA 13.1，PyTorch 使用 CUDA 12.4  
**解决**：向后兼容，无需担心，可以正常使用

### Q2: 显存不足
**解决方法**：
1. 减小 `batch_size`
2. 使用梯度累积 (`accumulation_steps`)
3. 启用混合精度训练 (`amp: true`)
4. 使用更小的模型变体

### Q3: 导入错误
```python
# 错误：No module named 'xxx'
# 解决：
pip install xxx

# 或重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### Q4: CUDA out of memory
**解决方法**：
```python
# 清理缓存
import torch
torch.cuda.empty_cache()

# 检查显存使用
print(f"已用：{torch.cuda.memory_allocated()/1024**3:.1f} GB")
print(f"缓存：{torch.cuda.memory_reserved()/1024**3:.1f} GB")
```

---

## 🔗 参考链接

- [PyTorch 官方](https://pytorch.org/)
- [Transformers 文档](https://huggingface.co/docs/transformers)
- [Ultralytics YOLO 文档](https://docs.ultralytics.com/)
- [DINOv2 论文](https://arxiv.org/abs/2304.07193)

---

## 📝 更新日志

| 日期 | 更新内容 |
|------|---------|
| 2026-04-03 | 初始版本，记录完整环境配置 |

---

**维护者**：taotie111  
**联系方式**：GitHub @taotie111
