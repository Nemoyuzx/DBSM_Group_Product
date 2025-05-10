<template>
  <div class="table-data-view">
    <h2>{{ tableName }} 数据</h2>
    <el-table v-if="tableData.length" :data="tableData" style="width: 100%" stripe border>
      <el-table-column v-for="col in columns" :key="col" :prop="col" :label="col"></el-table-column>
    </el-table>
    <div v-else class="empty-tip">暂无数据</div>
    <div class="chart-section">
      <h3>数据可视化</h3>
      <div ref="chartRef" class="chart-container"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import * as echarts from 'echarts';

const route = useRoute();
const tableName = ref(route.params.tableName || '');
const tableData = ref([]);
const columns = ref([]);
const chartRef = ref(null);
let chartInstance = null;

const fetchTableData = async () => {
  if (!tableName.value) return;
  // 假设后端API为 /api/table-data/:tableName
  try {
    const res = await fetch(`/api/table-data/${tableName.value}`);
    const data = await res.json();
    tableData.value = data.rows || [];
    columns.value = data.columns || (data.rows.length ? Object.keys(data.rows[0]) : []);
    renderChart();
  } catch (e) {
    tableData.value = [];
    columns.value = [];
  }
};

const renderChart = () => {
  if (!chartRef.value || !tableData.value.length) return;
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value);
  }
  // 简单示例：统计每一列的非空数量
  const option = {
    title: { text: `${tableName.value} 字段非空统计` },
    tooltip: {},
    xAxis: { type: 'category', data: columns.value },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: columns.value.map(col => tableData.value.filter(row => row[col] !== null && row[col] !== '').length)
    }]
  };
  chartInstance.setOption(option);
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
.empty-tip {
  color: #888;
  margin: 20px 0;
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
</style>