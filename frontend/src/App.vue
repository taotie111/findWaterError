<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>🌊 水体问题智能检测平台</h1>
          <el-menu mode="horizontal" :router="true" :default-active="$route.path">
            <el-menu-item index="/">🏠 首页</el-menu-item>
            <el-menu-item index="/detect">🔍 图像检测</el-menu-item>
            <el-menu-item index="/batch">📦 批量检测</el-menu-item>
            <el-menu-item index="/history">📜 历史记录</el-menu-item>
            <el-menu-item index="/stats">📊 统计分析</el-menu-item>
            <el-menu-item index="/models">🤖 模型管理</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
      
      <el-footer>
        <p>© 2026 水体问题智能检测平台 | Powered by Vue 3 + FastAPI</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
// 应用主组件
</script>

<style scoped>
#app {
  min-height: 100vh;
}

.el-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.header-content h1 {
  margin: 0;
  padding: 15px 0;
  font-size: 24px;
}

.el-menu {
  background: transparent;
  border: none;
}

.el-menu-item {
  color: white !important;
}

.el-menu-item:hover {
  background: rgba(255, 255, 255, 0.2) !important;
}

.el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.3) !important;
}

.el-main {
  min-height: calc(100vh - 120px);
  background: #f5f7fa;
}

.el-footer {
  background: #333;
  color: white;
  text-align: center;
  line-height: 60px;
}
</style>
