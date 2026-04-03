<template>
  <div class="models-page">
    <el-card>
      <template #header>
        <h3>🤖 模型管理</h3>
      </template>
      
      <el-table :data="models" stripe v-loading="loading">
        <el-table-column prop="name" label="模型名称" />
        <el-table-column prop="type" label="类型" width="120" />
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.loaded ? 'success' : 'info'">
              {{ scope.row.loaded ? '已加载' : '未加载' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="活动模型" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.is_active" type="primary">
              当前使用
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="handleSwitch(scope.row.name)"
              :disabled="scope.row.is_active"
            >
              切换
            </el-button>
            <el-button
              size="small"
              @click="handleLoad(scope.row.name)"
              v-if="!scope.row.loaded"
            >
              加载
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleUnload(scope.row.name)"
              v-if="scope.row.loaded && !scope.row.is_active"
            >
              卸载
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getModels, switchModel, loadModel, unloadModel } from '@/api/models'

const loading = ref(false)
const models = ref([])

const loadModels = async () => {
  loading.value = true
  try {
    const response = await getModels()
    models.value = response.models
  } catch (error) {
    ElMessage.error('获取模型列表失败')
  } finally {
    loading.value = false
  }
}

const handleSwitch = async (modelName) => {
  try {
    await switchModel(modelName)
    ElMessage.success(`已切换到 ${modelName}`)
    loadModels()
  } catch (error) {
    ElMessage.error('切换模型失败')
  }
}

const handleLoad = async (modelName) => {
  try {
    await loadModel(modelName)
    ElMessage.success(`模型 ${modelName} 加载成功`)
    loadModels()
  } catch (error) {
    ElMessage.error('加载模型失败')
  }
}

const handleUnload = async (modelName) => {
  try {
    await unloadModel(modelName)
    ElMessage.success(`模型 ${modelName} 卸载成功`)
    loadModels()
  } catch (error) {
    ElMessage.error('卸载模型失败')
  }
}

onMounted(() => {
  loadModels()
})
</script>

<style scoped>
.models-page {
  padding: 20px;
}
</style>
