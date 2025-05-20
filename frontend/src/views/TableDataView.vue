<template>
  <div class="table-data-view">
    <div class="header-actions">
      <el-button type="primary" icon="el-icon-back" @click="goBack">返回</el-button>
      <h2>{{ tableName }} 数据</h2>
    </div>
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    <div v-else-if="error" class="error-message">
      <el-alert :title="error" type="error" show-icon />
    </div>
    <div v-else>
      <el-table v-if="tableData.length" :data="tableData" style="width: 100%" stripe border height="500">
        <el-table-column v-for="col in columns" :key="col" :prop="col" :label="col"></el-table-column>
      </el-table>
      <div v-else class="empty-tip">暂无数据</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const tableName = ref(route.params.tableName || '');
const tableData = ref([]);
const columns = ref([]);
const loading = ref(false);
const error = ref(null);

const fetchTableData = async () => {
  if (!tableName.value) return;
  loading.value = true;
  error.value = null;
  
  try {
    console.log(`正在请求表${tableName.value}的数据...`);
    
    // 首先尝试获取可用模型列表
    const modelsResponse = await fetch('/api/available-models/');
    if (!modelsResponse.ok) {
      throw new Error('无法获取可用模型列表');
    }
    
    const modelsData = await modelsResponse.json();
    console.log('可用模型:', modelsData.available_models);
    
    // 尝试找到匹配的模型名称（忽略大小写）
    const exactModel = modelsData.available_models.find(
      model => model === tableName.value
    );
    
    const caseInsensitiveModel = modelsData.available_models.find(
      model => model.toLowerCase() === tableName.value.toLowerCase()
    );
    
    // 使用找到的正确大小写模型名
    const modelToUse = exactModel || caseInsensitiveModel || tableName.value;
    console.log('将使用模型名:', modelToUse);
    
    // 使用正确的模型名发起请求，确保使用/api/前缀
    let response;
    try {
      response = await fetch(`/api/table-data/${modelToUse}/`);
      if (!response.ok) {
        // 如果失败，尝试不带/api/前缀
        console.log('尝试不带/api/前缀的请求');
        response = await fetch(`/table-data/${modelToUse}/`);
      }
    } catch (e) {
      // 如果出错，尝试不带/api/前缀
      console.log('API请求出错，尝试不带/api/前缀', e);
      response = await fetch(`/table-data/${modelToUse}/`);
    }
    
    console.log('API响应状态:', response.status);
    
    if (!response.ok) {
      // 尝试解析错误信息
      let errorMsg = '获取数据失败';
      try {
        const errorData = await response.json();
        console.error('API错误详情:', errorData);
        errorMsg = errorData.error || errorMsg;
      } catch (e) {
        errorMsg = `服务器错误 (${response.status})`;
      }
      throw new Error(errorMsg);
    }
    
    const data = await response.json();
    console.log('获取到的数据:', data);
    
    tableData.value = data.rows || [];
    columns.value = data.columns || (data.rows.length ? Object.keys(data.rows[0]) : []);
  } catch (e) {
    console.error('获取表数据失败:', e);
    error.value = e.message || '获取数据失败';
    tableData.value = [];
    columns.value = [];
  } finally {
    loading.value = false;
  }
};

// 添加返回功能
const goBack = () => {
  router.back();
};

onMounted(() => {
  fetchTableData();
});

watch(() => route.params.tableName, (newVal) => {
  tableName.value = newVal;
  fetchTableData();
});
</script>

<style scoped>
.table-data-view {
  padding: 24px;
}
.header-actions {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.header-actions h2 {
  margin: 0 0 0 20px;
}
.empty-tip {
  color: #888;
  margin: 20px 0;
  text-align: center;
  padding: 40px;
  background: #f9f9f9;
  border-radius: 4px;
}
.loading-container {
  padding: 20px;
}
.error-message {
  margin: 20px 0;
}
</style>