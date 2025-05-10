<template>
  <div class="home">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <h2>欢迎使用教育管理系统</h2>
        </div>
      </template>
      <div class="card-content">
        <p>本系统提供全面的教育管理功能，包括人员管理、课程管理、院系管理等。</p>
        <el-row :gutter="20" class="stat-row">
          <el-col :span="8" v-for="(stat, index) in stats" :key="index">
            <el-card class="stat-card" shadow="hover">
              <h3>{{ stat.label }}</h3>
              <div class="stat-value">{{ stat.value }}</div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      stats: [
        { label: '人员总数', value: 0 },
        { label: '学生总数', value: 0 },
        { label: '教职工总数', value: 0 },
        { label: '课程总数', value: 0 },
        { label: '院系总数', value: 0 },
        { label: '项目总数', value: 0 }
      ]
    }
  },
  created() {
    this.fetchStats()
  },
  methods: {
    async fetchStats() {
      try {
        // 获取人员总数
        const personsResponse = await this.$axios.get('persons/')
        this.stats[0].value = personsResponse.data.count || personsResponse.data.length || 0
        
        // 获取学生总数
        const studentsResponse = await this.$axios.get('students/')
        this.stats[1].value = studentsResponse.data.count || studentsResponse.data.length || 0
        
        // 获取教职工总数
        const staffsResponse = await this.$axios.get('staffs/')
        this.stats[2].value = staffsResponse.data.count || staffsResponse.data.length || 0
        
        // 获取课程总数
        const coursesResponse = await this.$axios.get('courses/')
        this.stats[3].value = coursesResponse.data.count || coursesResponse.data.length || 0
        
        // 获取院系总数
        const departmentsResponse = await this.$axios.get('departments/')
        this.stats[4].value = departmentsResponse.data.count || departmentsResponse.data.length || 0
        
        // 获取项目总数
        const programsResponse = await this.$axios.get('programs/')
        this.stats[5].value = programsResponse.data.count || programsResponse.data.length || 0
      } catch (error) {
        console.error('获取统计数据失败:', error)
      }
    }
  }
}
</script>

<style scoped>
.welcome-card {
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-content {
  text-align: center;
}
.stat-row {
  margin-top: 20px;
}
.stat-card {
  text-align: center;
  margin-bottom: 20px;
}
.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-top: 10px;
}
</style>