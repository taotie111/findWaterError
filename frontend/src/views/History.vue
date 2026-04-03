<template>
  <div class="history-page">
    <el-card>
      <template #header>
        <h3>📜 检测历史</h3>
      </template>
      
      <el-table :data="history" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="image_name" label="图像名称" />
        <el-table-column prop="model_name" label="模型" width="120" />
        <el-table-column prop="total_objects" label="目标数" width="100" />
        <el-table-column prop="created_at" label="检测时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" @click="viewDetail(scope.row.id)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const loading = ref(false)
const history = ref([])

const loadHistory = async () => {
  loading.value = true
  // TODO: 调用 API 获取历史
  history.value = [
    { id: 1, image_name: 'test.jpg', model_name: 'yolov8', total_objects: 3, created_at: '2026-04-03 10:00:00' }
  ]
  loading.value = false
}

const viewDetail = (id) => {
  console.log('查看详情:', id)
}

onMounted(() => {
  loadHistory()
})
</script>

<style scoped>
.history-page {
  padding: 20px;
}
</style>
