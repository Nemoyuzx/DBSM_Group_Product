<template>
  <div class="api-debug">
    <h2>API 调试工具</h2>
    
    <el-form>
      <el-form-item label="API路径">
        <el-input v-model="apiPath" placeholder="/api/table-data/Student/"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="testApi">测试API</el-button>
        <el-button @click="addApiPrefix">添加/api/前缀</el-button>
        <el-button @click="removeApiPrefix">删除/api/前缀</el-button>
      </el-form-item>
    </el-form>
    
    <div v-if="loading" class="api-loading">
      <el-progress type="circle" :percentage="50" status="exception"></el-progress>
      <p>请求中...</p>
    </div>
    
    <div v-if="error" class="api-error">
      <h3>错误信息</h3>
      <pre>{{ error }}</pre>
    </div>
    
    <div v-if="response" class="api-response">
      <h3>API响应</h3>
      <pre class="json-response">{{ formattedResponse }}</pre>
    </div>
    
    <h3>常用API端点:</h3>
    <div class="api-links">
      <div @click="apiPath = '/api/table-counts/'; testApi()" class="api-link">表计数</div>
      <div @click="apiPath = '/api/available-models/'; testApi()" class="api-link">可用模型</div>
      <div @click="apiPath = '/api/table-data/Student/'; testApi()" class="api-link">学生数据</div>
      <div @click="apiPath = '/api/table-data/Person/'; testApi()" class="api-link">人员数据</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApiDebug',
  data() {
    return {
      apiPath: '/api/table-counts/',
      loading: false,
      error: null,
      response: null
    }
  },
  computed: {
    formattedResponse() {
      try {
        return JSON.stringify(JSON.parse(this.response), null, 2);
      } catch (e) {
        return this.response;
      }
    }
  },
  methods: {
    async testApi() {
      this.loading = true;
      this.error = null;
      this.response = null;
      
      try {
        console.log(`测试API: ${this.apiPath}`);
        const response = await fetch(this.apiPath);
        const statusText = response.statusText;
        const contentType = response.headers.get('content-type');
        
        if (contentType && contentType.includes('application/json')) {
          const data = await response.json();
          this.response = JSON.stringify(data);
        } else {
          const text = await response.text();
          this.response = text;
          if (!response.ok) {
            this.error = `请求失败: ${response.status} ${statusText}\n内容类型: ${contentType}`;
          }
        }
      } catch (e) {
        this.error = `请求异常: ${e.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    addApiPrefix() {
      if (!this.apiPath.startsWith('/api/')) {
        this.apiPath = `/api${this.apiPath.startsWith('/') ? '' : '/'}${this.apiPath}`;
      }
    },
    
    removeApiPrefix() {
      if (this.apiPath.startsWith('/api/')) {
        this.apiPath = this.apiPath.replace('/api/', '/');
      }
    }
  }
}
</script>

<style scoped>
.api-debug {
  padding: 20px;
}
.api-loading {
  margin: 20px 0;
  text-align: center;
}
.api-error {
  margin: 20px 0;
  padding: 10px;
  background-color: #fef0f0;
  border: 1px solid #fbc4c4;
  border-radius: 4px;
}
.api-response {
  margin: 20px 0;
}
.json-response {
  padding: 10px;
  background-color: #f8f8f8;
  border-radius: 4px;
  overflow: auto;
  max-height: 400px;
}
.api-links {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 10px 0;
}
.api-link {
  padding: 5px 10px;
  background-color: #409EFF;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}
.api-link:hover {
  background-color: #337ecc;
}
</style>
