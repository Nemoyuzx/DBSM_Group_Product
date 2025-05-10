<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="welcome-card">
          <h1>欢迎使用DBMS系统</h1>
          <p>这是一个用于管理学校数据的数据库管理系统</p>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" class="mt-20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>院系管理</span>
              <el-button class="button" text @click="$router.push('/departments')">查看</el-button>
            </div>
          </template>
          <div>管理学校的院系信息</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>专业管理</span>
              <el-button class="button" text @click="$router.push('/programs')">查看</el-button>
            </div>
          </template>
          <div>管理学校的专业信息</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>课程管理</span>
              <el-button class="button" text @click="$router.push('/courses')">查看</el-button>
            </div>
          </template>
          <div>管理学校的课程信息</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home {
  padding: 20px;
}
.welcome-card {
  margin-bottom: 20px;
  text-align: center;
}
.mt-20 {
  margin-top: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>