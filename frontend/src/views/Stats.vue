<template>
  <div class="stats-page">
    <el-card>
      <template #header>
        <h3>📊 统计分析</h3>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-statistic title="总检测次数" :value="stats.total_detections" />
        </el-col>
        <el-col :span="8">
          <el-statistic title="总目标数" :value="stats.total_objects" />
        </el-col>
        <el-col :span="8">
          <el-statistic title="已加载模型" :value="stats.loaded_models" />
        </el-col>
      </el-row>
      
      <div style="margin-top: 40px;">
        <h4>检测趋势（待实现）</h4>
        <div style="height: 300px; background: #f5f7fa; display: flex; align-items: center; justify-content: center;">
          <el-empty description="统计图表功能开发中" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const stats = ref({
  total_detections: 0,
  total_objects: 0,
  loaded_models: 0
})

onMounted(() => {
  // TODO: 调用 API 获取统计数据
  stats.value = {
    total_detections: 0,
    total_objects: 0,
    loaded_models: 0
  }
})
</script>

<style scoped>
.stats-page {
  padding: 20px;
}
</style>
