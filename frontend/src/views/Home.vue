<template>
  <div class="home">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <h2>🌊 欢迎使用河湖问题智能检测中台</h2>
        </div>
      </template>
      
      <div class="welcome-content">
        <el-row :gutter="20">
          <el-col :span="8" v-for="feature in features" :key="feature.title">
            <el-card shadow="hover" class="feature-card">
              <div class="feature-icon">{{ feature.icon }}</div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
            </el-card>
          </el-col>
        </el-row>
        
        <div class="quick-actions">
          <h3>快速开始</h3>
          <el-space>
            <el-button type="primary" size="large" @click="$router.push('/detect')">
              <el-icon><Search /></el-icon>
              开始检测
            </el-button>
            <el-button type="success" size="large" @click="$router.push('/batch')">
              <el-icon><FolderOpened /></el-icon>
              批量检测
            </el-button>
            <el-button type="info" size="large" @click="$router.push('/history')">
              <el-icon><Document /></el-icon>
              查看历史
            </el-button>
          </el-space>
        </div>
        
        <div class="system-status" v-if="systemStatus">
          <h3>系统状态</h3>
          <el-descriptions :column="3" border>
            <el-descriptions-item label="活动模型">
              <el-tag type="success">{{ systemStatus.active_model }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="已加载模型">
              {{ systemStatus.loaded_models.join(', ') }}
            </el-descriptions-item>
            <el-descriptions-item label="设备">
              {{ systemStatus.device }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getModelStatus } from '@/api/models'

const features = [
  {
    icon: '🤖',
    title: '多模型支持',
    description: '支持 DINOv2、YOLOv8、YOLOv10、YOLO-SE 等多种检测模型'
  },
  {
    icon: '⚡',
    title: '实时检测',
    description: '上传图像后立即检测，实时显示检测结果和统计信息'
  },
  {
    icon: '📊',
    title: '数据分析',
    description: '完善的统计功能，支持按类别、时间等多维度分析'
  }
]

const systemStatus = ref(null)

onMounted(async () => {
  try {
    const status = await getModelStatus()
    systemStatus.value = status.status
  } catch (error) {
    console.error('获取系统状态失败:', error)
  }
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 30px auto 0;
  padding: 0 20px;
  box-sizing: border-box;
}

.welcome-card {
  margin-bottom: 20px;
}

.card-header h2 {
  margin: 0;
  color: #667eea;
}

.welcome-content {
  padding: 10px 0;
}

.feature-card {
  text-align: center;
  padding: 20px 10px;
  transition: transform 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

:deep(.el-card__body) {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.feature-card h3 {
  margin: 8px 0;
  color: #333;
  font-size: 16px;
}

.feature-card p {
  color: #666;
  line-height: 1.4;
  font-size: 13px;
  margin: 0;
}

.quick-actions {
  margin: 30px 0;
  text-align: center;
}

.quick-actions h3 {
  margin-bottom: 15px;
  color: #333;
}

.system-status {
  margin-top: 30px;
}

.system-status h3 {
  margin-bottom: 15px;
  color: #333;
}
</style>
