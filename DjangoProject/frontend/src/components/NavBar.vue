<template>
  <div class="navbar">
    <el-menu
      :default-active="activeIndex"
      mode="horizontal"
      router
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
    >
      <el-menu-item index="/">首页</el-menu-item>
      <el-sub-menu index="1">
        <template #title>人员管理</template>
        <el-menu-item index="/persons">人员列表</el-menu-item>
        <el-menu-item index="/students">学生管理</el-menu-item>
        <el-menu-item index="/staffs">教职工管理</el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="2">
        <template #title>学术管理</template>
        <el-menu-item index="/courses">课程管理</el-menu-item>
        <el-menu-item index="/departments">院系管理</el-menu-item>
        <el-menu-item index="/programs">项目管理</el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="3">
        <template #title>更多功能</template>
        <el-menu-item index="/enrollments">选课管理</el-menu-item>
        <el-menu-item index="/assessments">评估管理</el-menu-item>
        <el-menu-item index="/classes">班级管理</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      activeIndex: this.$route.path
    }
  },
  watch: {
    $route(to) {
      this.activeIndex = to.path
    }
  }
}
</script>

<style scoped>
.navbar {
  width: 100%;
}
</style>