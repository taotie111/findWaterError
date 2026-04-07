<template>
  <div class="detect-page">
    <el-row :gutter="20">
      <!-- 左侧：上传和设置 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <h3>📤 图像上传</h3>
          </template>
          
          <el-upload
            ref="uploadRef"
            drag
            :auto-upload="false"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            :limit="1"
            :on-exceed="handleExceed"
            accept="image/*"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              拖拽文件到此处或<em>点击上传</em>
            </div>
          </el-upload>
          
          <div class="model-selector" style="margin-top: 20px;">
            <label>选择模型：</label>
            <el-select v-model="selectedModel" placeholder="请选择模型" style="width: 100%;">
              <el-option
                v-for="model in availableModels"
                :key="model.name"
                :label="model.name"
                :value="model.name"
                :disabled="!model.enabled"
              />
            </el-select>
          </div>
          
          <el-button
            type="primary"
            size="large"
            style="width: 100%; margin-top: 20px;"
            :loading="detecting"
            @click="handleDetect"
            :disabled="!selectedFile"
          >
            🔍 开始检测
          </el-button>
        </el-card>
      </el-col>
      
      <!-- 右侧：结果展示 -->
      <el-col :span="16">
        <el-card>
          <template #header>
            <h3>📊 检测结果</h3>
          </template>
          
          <div v-if="!detectionResult" class="empty-result">
            <el-empty description="请先上传图像并点击检测" />
          </div>
          
          <div v-else class="result-content">
            <el-row :gutter="20">
              <el-col :span="12">
                <h4>原始图像</h4>
                <img :src="imageUrl" alt="原始图像" class="result-image" />
              </el-col>
              
              <el-col :span="12">
                <h4>检测结果</h4>
                <img :src="resultImageUrl" alt="检测结果" class="result-image" />
              </el-col>
            </el-row>
            
            <div class="detection-info">
              <h4>检测详情</h4>
              <el-table :data="detectionResult.results" stripe style="width: 100%">
                <el-table-column prop="class_name" label="类别" width="120" />
                <el-table-column prop="confidence" label="置信度" width="100">
                  <template #default="scope">
                    <el-tag :type="getConfidenceType(scope.row.confidence)">
                      {{ (scope.row.confidence * 100).toFixed(1) }}%
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="边界框">
                  <template #default="scope">
                    {{ formatBbox(scope.row.bbox) }}
                  </template>
                </el-table-column>
              </el-table>
              
              <div class="summary">
                <el-statistic title="检测目标数" :value="detectionResult.total_objects" />
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { getModels } from '@/api/models'
import { detectImage } from '@/api/detect'

const uploadRef = ref(null)
const selectedFile = ref(null)
const selectedModel = ref('yolov8')
const availableModels = ref([])
const detecting = ref(false)
const detectionResult = ref(null)
const imageUrl = ref(null)
const resultImageUrl = ref(null)

// 加载可用模型
const loadModels = async () => {
  try {
    const response = await getModels()
    availableModels.value = response.models
    if (response.models.length > 0) {
      selectedModel.value = response.active_model || response.models[0].name
    }
  } catch (error) {
    ElMessage.error('获取模型列表失败')
  }
}

// 处理文件选择
const handleFileChange = (file) => {
  selectedFile.value = file.raw
  imageUrl.value = URL.createObjectURL(file.raw)
  detectionResult.value = null
  resultImageUrl.value = null
  // 清除之前的检测结果图片
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
}

const handleFileRemove = () => {
  selectedFile.value = null
  imageUrl.value = null
  detectionResult.value = null
  resultImageUrl.value = null
}

// 超出文件数量限制
const handleExceed = () => {
  // 清除旧文件
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
  ElMessage.warning('请先清除当前图片再上传新图片')
}

// 执行检测
const handleDetect = async () => {
  if (!selectedFile.value) return
  
  detecting.value = true
  
  try {
    const response = await detectImage(selectedFile.value, selectedModel.value)
    
    if (response.success) {
      detectionResult.value = response
      resultImageUrl.value = '/outputs/' + response.output_image.split('/').pop()
      ElMessage.success(`检测完成，发现 ${response.total_objects} 个目标`)
    } else {
      ElMessage.error('检测失败')
    }
  } catch (error) {
    console.error('检测错误:', error)
    ElMessage.error('检测失败：' + (error.response?.data?.detail || error.message))
  } finally {
    detecting.value = false
  }
}

// 置信度标签类型
const getConfidenceType = (confidence) => {
  if (confidence >= 0.8) return 'success'
  if (confidence >= 0.6) return 'warning'
  return 'danger'
}

// 格式化边界框
const formatBbox = (bbox) => {
  return `(${Math.round(bbox.x_min)}, ${Math.round(bbox.y_min)}) - (${Math.round(bbox.x_max)}, ${Math.round(bbox.y_max)})`
}

// 初始化
loadModels()
</script>

<style scoped>
.detect-page {
  padding: 20px 0;
  box-sizing: border-box;
}

.empty-result {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.result-content {
  padding: 10px 0;
}

.result-image {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.detection-info {
  margin-top: 20px;
}

.summary {
  margin-top: 20px;
  text-align: center;
}

.model-selector {
  display: flex;
  flex-direction: column;
}

.model-selector label {
  margin-bottom: 8px;
  font-weight: bold;
}
</style>
