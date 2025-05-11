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
      <div class="chart-section" v-if="tableData.length">
        <h3>数据可视化</h3>
        <div ref="chartRef" class="chart-container"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import * as echarts from 'echarts';

const route = useRoute();
const router = useRouter();
const tableName = ref(route.params.tableName || '');
const tableData = ref([]);
const columns = ref([]);
const chartRef = ref(null);
const loading = ref(false);
const error = ref(null);
let chartInstance = null;

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
    
    setTimeout(() => {
      renderChart();
    }, 300);
  } catch (e) {
    console.error('获取表数据失败:', e);
    error.value = e.message || '获取数据失败';
    tableData.value = [];
    columns.value = [];
  } finally {
    loading.value = false;
  }
};

const renderChart = () => {
  if (!chartRef.value || !tableData.value.length) return;
  
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value);
  }
  
  // 根据数据类型选择合适的可视化
  const numericColumns = columns.value.filter(col => {
    return tableData.value.some(row => typeof row[col] === 'number');
  });
  
  if (numericColumns.length) {
    // 如果有数值型数据，使用柱状图显示
    const firstNumericCol = numericColumns[0];
    const option = {
      title: { text: `${tableName.value} 数据统计` },
      tooltip: {},
      xAxis: { 
        type: 'category', 
        data: tableData.value.slice(0, 20).map((_, index) => `记录 ${index + 1}`),
        axisLabel: { interval: 0, rotate: 45 }
      },
      yAxis: { type: 'value' },
      series: [{
        name: firstNumericCol,
        type: 'bar',
        data: tableData.value.slice(0, 20).map(row => row[firstNumericCol] || 0)
      }]
    };
    chartInstance.setOption(option);
  } else {
    // 默认统计记录数量的饼图
    const option = {
      title: { text: `${tableName.value} 记录分布` },
      tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
      series: [{
        type: 'pie',
        radius: '65%',
        center: ['50%', '50%'],
        data: [{ value: tableData.value.length, name: '总记录数' }],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    };
    chartInstance.setOption(option);
  }
};

// 添加返回功能
const goBack = () => {
  router.back();
};

onMounted(() => {
  fetchTableData();
});

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose();
  }
});

watch(() => route.params.tableName, (newVal) => {
  tableName.value = newVal;
  fetchTableData();
});

// 监听窗口大小变化，调整图表大小
window.addEventListener('resize', () => {
  if (chartInstance) {
    chartInstance.resize();
  }
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
.chart-section {
  margin-top: 32px;
}
.chart-container {
  width: 100%;
  height: 350px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.loading-container {
  padding: 20px;
}
.error-message {
  margin: 20px 0;
}
</style>