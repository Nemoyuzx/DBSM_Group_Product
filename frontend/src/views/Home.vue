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
    
    <!-- 数据统计卡片 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="24">
        <el-card class="data-stats-card">
          <template #header>
            <div class="card-header">
              <span>数据统计概览</span>
              <el-button class="button" text @click="refreshStats">刷新</el-button>
            </div>
          </template>
          <div v-loading="loading">
            <div v-if="error" class="error-message">{{ error }}</div>
            <div v-else>
              <!-- 分类统计 -->
              <div v-for="(models, category) in categorizedCounts" :key="category" class="category-section">
                <h3>{{ category }}</h3>
                <el-row :gutter="10">
                  <el-col :xs="12" :sm="8" :md="6" :lg="4" v-for="(count, model) in models" :key="model">
                    <el-card shadow="hover" class="stat-card">
                      <div class="stat-name">{{ model }}</div>
                      <div class="stat-count">{{ count }}</div>
                    </el-card>
                  </el-col>
                </el-row>
              </div>
            </div>
          </div>
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
import axios from 'axios'

export default {
  name: 'Home',
  data() {
    return {
      counts: {},
      categorizedCounts: {},
      loading: false,
      error: null
    }
  },
  mounted() {
    this.fetchTableCounts()
  },
  methods: {
    async fetchTableCounts() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('table-counts/')
        this.counts = response.data.counts
        this.categorizedCounts = response.data.categorized_counts
      } catch (err) {
        console.error('获取数据统计失败:', err)
        this.error = '获取数据统计失败，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    refreshStats() {
      this.fetchTableCounts()
    }
  }
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
.data-stats-card {
  margin-bottom: 20px;
}
.category-section {
  margin-bottom: 20px;
}
.category-section h3 {
  margin-bottom: 15px;
  padding-bottom: 8px;
  border-bottom: 1px solid #ebeef5;
  color: #409EFF;
}
.stat-card {
  text-align: center;
  margin-bottom: 15px;
  transition: all 0.3s;
}
.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}
.stat-name {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}
.stat-count {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}
.error-message {
  color: #F56C6C;
  text-align: center;
  padding: 20px;
}
</style>