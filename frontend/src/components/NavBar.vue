<template>
  <div class="nav-bar">
    <el-menu mode="horizontal" :router="true" background-color="#409EFF" text-color="#fff" active-text-color="#ffd04b">
      <el-menu-item index="/">首页</el-menu-item>
      <el-menu-item index="/departments">院系管理</el-menu-item>
      <el-menu-item index="/programs">专业管理</el-menu-item>
      <el-menu-item index="/courses">课程管理</el-menu-item>
      <el-menu-item index="/students">学生管理</el-menu-item>
      <el-menu-item index="/staffs">教职工管理</el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style scoped>
.nav-bar {
  width: 100%;
}
</style>