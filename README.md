# findWaterError - 多模型水体问题智能识别系统 🌊

**支持模型**：DINOv2 | YOLOv8 | YOLOv10 | YOLO-SE  
**当前环境**：Python 3.13.5 | PyTorch 2.6.0+cu124 | CUDA 13.1 | RTX 3060 (12GB)  
**平台**：✅ Web 检测平台 | ✅ 标注系统 | ✅ 训练代码

[![GitHub](https://img.shields.io/github/repo-size/taotie111/findWaterError)](https://github.com/taotie111/findWaterError)
[![License](https://img.shields.io/github/license/taotie111/findWaterError)](https://github.com/taotie111/findWaterError/blob/master/LICENSE)

---

## 🌟 核心功能

### 检测平台

- ✅ **Web 界面**：Vue 3 + Element Plus
- ✅ **单张检测**：上传图像实时检测
- ✅ **批量检测**：支持批量图像处理
- ✅ **结果可视化**：自动绘制检测框
- ✅ **历史记录**：数据库存储检测历史
- ✅ **统计分析**：检测数据多维分析
- ✅ **模型管理**：热切换检测模型

### 训练系统

- ✅ **多模型训练**：DINOv2/YOLOv8/YOLOv10/YOLO-SE
- ✅ **完整流程**：数据加载→训练→验证→导出
- ✅ **可视化**：训练曲线、混淆矩阵、分类报告
- ✅ **类别分析**：每个类别的准确率统计

### 标注系统

- ✅ **多工具支持**：LabelImg/LabelMe/CVAT
- ✅ **格式统一**：自动转换为 YOLO 格式
- ✅ **质量检查**：完善的质检流程
- ✅ **团队协作**：多人标注支持

---

## 🚀 快速开始

### 🌐 检测平台（推荐）

**一键启动完整平台**：

```bash
# 终端 1 - 启动后端
cd backend
start.bat

# 终端 2 - 启动前端
cd frontend
npm install  # 首次运行
start.bat
```

访问：
- **前端**：http://localhost:5173
- **API 文档**：http://localhost:8000/docs

### 1. 环境要求

- **Python**: 3.13+
- **Node.js**: 18+
- **PyTorch**: 2.6.0+cu124
- **CUDA**: 12.4+ (系统 CUDA 13.1 兼容)
- **GPU**: 8GB+ 显存 (推荐 RTX 3060 及以上)

### 2. 安装依赖

```bash
# 克隆仓库
git clone https://github.com/taotie111/findWaterError.git
cd findWaterError

# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd ../frontend
npm install
```

### 3. 验证安装

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
```

---

## 📊 模型性能

### DINOv2 (当前最佳)

| 指标 | 数值 | 备注 |
|------|------|------|
| **最佳验证准确率** | **68.96%** | 第 3 轮 |
| 最终验证准确率 | 65.41% | 第 20 轮 |
| 训练用时 | ~77 分钟/轮 | RTX 3060 |

### 各类别性能

| 类别 | 准确率 | 样本数 | 状态 |
|------|--------|--------|------|
| 垃圾 | ~75% | 50 | ✅ 良好 |
| 其他 | ~72% | 284 | ✅ 良好 |
| 违建 | ~70% | 37 | ✅ 良好 |
| 漂浮物 | ~50% | 2 | ⚠️ 样本不足 |
| 排污 | ~43% | 7 | ⚠️ 样本不足 |

---

## 📁 项目结构

```
findWaterError/
├── backend/                           # 🐍 Python 后端（FastAPI）
│   ├── app/
│   │   ├── main.py                   # FastAPI 应用
│   │   ├── api/                      # API 路由
│   │   ├── core/                     # 模型管理器
│   │   ├── db/                       # 数据库
│   │   └── utils/                    # 工具函数
│   ├── config.yaml                   # 配置
│   └── start.bat                     # 启动脚本
│
├── frontend/                          # 🎨 Vue 3 前端
│   ├── src/
│   │   ├── views/                    # 6 个页面
│   │   ├── api/                      # API 封装
│   │   └── router/                   # 路由
│   └── start.bat                     # 启动脚本
│
├── configs/                           # 📋 模型配置
├── src/                               # 🐍 训练代码
├── data/annotations/                  # 📝 标注系统
├── notebooks/                         # 📓 Jupyter
└── docs/                              # 📖 文档
```

---

## 📖 文档

### 平台使用

- [**使用指南**](docs/USAGE_GUIDE.md) - 完整使用教程
- [**部署指南**](docs/PLATFORM_GUIDE.md) - 平台部署说明

### 标注系统

- [**标注指南**](docs/ANNOTATION_GUIDE.md) - 6 类水体问题定义
- [**多工具标注**](docs/MULTI_TOOL_ANNOTATION.md) - LabelImg/LabelMe/CVAT
- [**标注工具使用**](docs/ANNOTATION_TOOLS.md) - 工具教程

### 环境配置

- [**环境说明**](docs/ENVIRONMENT.md) - Python/CUDA/PyTorch 版本
- [**配置总结**](docs/CONFIG_SUMMARY.md) - 配置文件说明

---

## 🛠️ 技术栈

### 后端
- FastAPI 0.109.0
- PyTorch 2.6.0+cu124
- Ultralytics (YOLO)
- Transformers (DINOv2)
- SQLAlchemy

### 前端
- Vue 3.4
- Vite 5
- Element Plus
- Pinia
- Axios

### 标注工具
- LabelImg
- LabelMe
- CVAT

---

## 📄 许可证

MIT License

---

## 📞 联系方式

- **GitHub**: [@taotie111](https://github.com/taotie111)
- **项目地址**: https://github.com/taotie111/findWaterError
- **问题反馈**: [Issues](https://github.com/taotie111/findWaterError/issues)

---

**最后更新**：2026-04-03  
**维护者**：taotie111
