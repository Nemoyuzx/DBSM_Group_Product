<template>
  <div id="app">
    <el-container>
      <el-header>
        <nav-bar />
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>
        <footer-bar />
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import FooterBar from '@/components/FooterBar.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    FooterBar
  }
}
</script>

<style>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.el-header {
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
  z-index: 1000;
}

.el-footer {
  padding: 20px 0;
  text-align: center;
  color: #909399;
  font-size: 14px;
  border-top: 1px solid #ebeef5;
}

.el-main {
  padding: 20px;
  min-height: calc(100vh - 120px);
}
</style>