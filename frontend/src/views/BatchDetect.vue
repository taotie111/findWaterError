<template>
  <div class="batch-page">
    <el-card>
      <template #header>
        <h3>📦 批量检测</h3>
      </template>
      
      <el-upload
        ref="uploadRef"
        drag
        :auto-upload="false"
        :on-change="handleFilesChange"
        :on-remove="handleFileRemove"
        :limit="100"
        multiple
        accept="image/*"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或<em>点击上传</em>
        </div>
      </el-upload>
      
      <div class="batch-actions" style="margin-top: 20px;">
        <el-button
          type="primary"
          size="large"
          :loading="detecting"
          @click="handleBatchDetect"
          :disabled="selectedFiles.length === 0"
        >
          🔍 开始批量检测
        </el-button>
        
        <el-button @click="handleClear">清空</el-button>
      </div>
      
      <div v-if="batchResult" class="batch-result" style="margin-top: 20px;">
        <h4>批量检测结果</h4>
        <el-descriptions :column="3" border>
          <el-descriptions-item label="总图像数">
            {{ batchResult.total_images }}
          </el-descriptions-item>
          <el-descriptions-item label="成功处理">
            {{ batchResult.processed_images }}
          </el-descriptions-item>
          <el-descriptions-item label="总目标数">
            {{ batchResult.total_objects }}
          </el-descriptions-item>
        </el-descriptions>
        
        <el-table :data="batchResult.results" stripe style="margin-top: 20px;">
          <el-table-column prop="filename" label="文件名" />
          <el-table-column label="检测结果">
            <template #default="scope">
              <span v-if="scope.row.results">
                {{ scope.row.results.length }} 个目标
              </span>
              <el-tag v-else type="danger">失败</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { detectBatch } from '@/api/detect'

const uploadRef = ref(null)
const selectedFiles = ref([])
const detecting = ref(false)
const batchResult = ref(null)

const handleFilesChange = (file) => {
  selectedFiles.value.push(file.raw)
}

const handleFileRemove = (file) => {
  selectedFiles.value = selectedFiles.value.filter(f => f !== file.raw)
}

const handleClear = () => {
  selectedFiles.value = []
  batchResult.value = null
  uploadRef.value?.clearFiles()
}

const handleBatchDetect = async () => {
  if (selectedFiles.value.length === 0) return
  
  detecting.value = true
  
  try {
    const response = await detectBatch(selectedFiles.value)
    batchResult.value = response
    ElMessage.success(`批量检测完成，处理 ${response.processed_images} 张图像`)
  } catch (error) {
    ElMessage.error('批量检测失败')
  } finally {
    detecting.value = false
  }
}
</script>

<style scoped>
.batch-page {
  padding: 20px 0;
  box-sizing: border-box;
}

.batch-actions {
  text-align: center;
}

.batch-result {
  padding: 20px 0;
}
</style>
