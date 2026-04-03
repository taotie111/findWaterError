# 水体问题智能检测平台 - 前端

基于 Vue 3 + Element Plus 的 Web 前端应用。

## 技术栈

- **Vue 3.4** - 渐进式 JavaScript 框架
- **Vite 5** - 下一代前端构建工具
- **Element Plus** - Vue 3 组件库
- **Pinia** - Vue 3 状态管理
- **Vue Router 4** - 路由管理
- **Axios** - HTTP 客户端
- **ECharts** - 数据可视化（待集成）

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
# Windows
start.bat

# 或直接运行
npm run dev
```

访问：http://localhost:5173

### 3. 构建生产版本

```bash
npm run build
```

## 项目结构

```
frontend/
├── src/
│   ├── api/                    # API 封装
│   │   ├── index.js           # axios 实例
│   │   ├── detect.js          # 检测 API
│   │   └── models.js          # 模型管理 API
│   ├── assets/                # 静态资源
│   ├── components/            # 公共组件
│   ├── router/                # 路由配置
│   │   └── index.js
│   ├── stores/                # Pinia 状态管理
│   ├── views/                 # 页面视图
│   │   ├── Home.vue           # 首页
│   │   ├── Detect.vue         # 图像检测
│   │   ├── BatchDetect.vue    # 批量检测
│   │   ├── History.vue        # 历史记录
│   │   ├── Stats.vue          # 统计分析
│   │   └── Models.vue         # 模型管理
│   ├── App.vue                # 根组件
│   └── main.js                # 应用入口
├── public/                    # 公共文件
├── index.html                 # HTML 模板
├── package.json               # 依赖配置
├── vite.config.js             # Vite 配置
└── start.bat                  # 启动脚本
```

## 功能页面

### 1. 首页 (`/`)
- 平台介绍
- 快速入口
- 系统状态

### 2. 图像检测 (`/detect`)
- 图像上传（拖拽/选择）
- 模型选择
- 实时检测
- 结果可视化
- 检测详情

### 3. 批量检测 (`/batch`)
- 批量上传
- 进度显示
- 批量结果

### 4. 历史记录 (`/history`)
- 检测历史列表
- 详情查看
- 搜索筛选

### 5. 统计分析 (`/stats`)
- 检测统计
- 类别分布
- 趋势图表（待实现）

### 6. 模型管理 (`/models`)
- 模型列表
- 模型切换
- 加载/卸载

## API 代理

开发服务器已配置 API 代理：

```javascript
// vite.config.js
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true
  }
}
```

## 环境变量

创建 `.env` 文件（可选）：

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 开发指南

### 添加新页面

1. 在 `src/views/` 创建新组件
2. 在 `src/router/index.js` 添加路由
3. 在 `App.vue` 添加菜单项

### 调用 API

```javascript
import { detectImage } from '@/api/detect'

const result = await detectImage(file, 'yolov8')
```

### 状态管理

使用 Pinia 创建全局状态：

```javascript
// stores/detect.js
import { defineStore } from 'pinia'

export const useDetectStore = defineStore('detect', {
  state: () => ({
    results: []
  }),
  actions: {
    addResult(result) {
      this.results.push(result)
    }
  }
})
```

## 注意事项

1. **后端服务**：确保后端服务运行在 http://localhost:8000
2. **CORS**：开发环境已配置代理，生产环境需要配置 CORS
3. **大文件上传**：默认限制 50MB，可在后端配置中调整

## 下一步

- [ ] 完善统计图表（ECharts）
- [ ] 添加用户认证
- [ ] 优化移动端适配
- [ ] 添加 PWA 支持

## 许可证

MIT License

---

**维护者**：taotie111  
**GitHub**：https://github.com/taotie111/findWaterError
