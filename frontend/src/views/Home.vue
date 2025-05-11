<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="welcome-card">
          <h1>{{ $t('welcome') }}</h1>
          <p>{{ $t('description') }}</p>
          <div class="contact">
            Group19 · Rui ❤️‍🔥：<a href="mailto:jp2023213616@qmul.ac.uk">jp2023213616@qmul.ac.uk</a>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 数据统计卡片 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="24">
        <el-card class="data-stats-card">
          <template #header>
            <div class="card-header">
              <span>{{ $t('stats') }}</span>
              <el-button class="button" text @click="refreshStats">{{ $t('refresh') }}</el-button>
            </div>
          </template>
          <div v-loading="loading">
            <div v-if="error" class="error-message">{{ error }}</div>
            <div v-else>
              <!-- 分类统计 -->
              <div v-for="(models, categoryKey) in categorizedCounts" :key="categoryKey" class="category-section">
                <h3>{{ $t(`category_${categoryKey}`) }}</h3>
                <el-row :gutter="10">
                  <el-col
                      :xs="12"
                      :sm="8"
                      :md="6"
                      :lg="4"
                      v-for="(count, model) in models"
                      :key="model"
                  >
                    <el-card shadow="hover" class="stat-card" @click="viewTableData(model)">
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

    <!-- 快捷导航卡片 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>{{ $t('departments') }}</span>
              <el-button class="button" text @click="$router.push('/departments')">{{ $t('view') }}</el-button>
            </div>
          </template>
          <div>{{ $t('dept_desc') }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>{{ $t('programs') }}</span>
              <el-button class="button" text @click="$router.push('/programs')">{{ $t('view') }}</el-button>
            </div>
          </template>
          <div>{{ $t('prog_desc') }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>{{ $t('courses') }}</span>
              <el-button class="button" text @click="$router.push('/courses')">{{ $t('view') }}</el-button>
            </div>
          </template>
          <div>{{ $t('course_desc') }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 页脚 -->
    <p class="footer">{{ $t('copyright') }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HomeView',
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
        // 确保请求使用/api前缀
        const response = await axios.get('/api/table-counts/')
        console.log('获取到的表计数:', response.data)
        this.counts = response.data.counts
        this.categorizedCounts = response.data.categorized_counts
      } catch (err) {
        console.error('获取数据统计失败:', err)
        this.error = this.$t('fetch_error')
        
        // 如果请求失败，尝试不带/api/前缀的请求
        try {
          const fallbackResponse = await axios.get('/table-counts/')
          console.log('通过备用路径获取表计数:', fallbackResponse.data)
          this.counts = fallbackResponse.data.counts
          this.categorizedCounts = fallbackResponse.data.categorized_counts
        } catch (fallbackErr) {
          console.error('备用请求也失败:', fallbackErr)
        }
      } finally {
        this.loading = false
      }
    },
    refreshStats() {
      this.fetchTableCounts()
    },
    viewTableData(tableName) {
      // 添加调试日志
      console.log(`正在跳转到表 ${tableName} 的数据视图`);
      
      // 确保使用正确的路由路径
      this.$router.push({
        name: 'TableDataView',
        params: { tableName }
      });
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
.contact {
  margin-top: 10px;
  font-size: 13px;
  color: #666;
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
  cursor: pointer;  /* 添加鼠标指针样式 */
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
.footer {
  margin-top: 40px;
  text-align: center;
  color: #909399;
}
</style>