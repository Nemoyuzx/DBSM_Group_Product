<template>
  <div class="all-tables">
    <h1>所有数据表</h1>
    <el-table :data="tables" style="width: 100%" @row-click="handleRowClick" stripe border>
      <el-table-column prop="name" label="表名"></el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="viewTableData(scope.row.name)">查看数据</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'AllTables',
  setup() {
    const tables = ref([]);
    const router = useRouter();

    const fetchTables = async () => {
      try {
        const response = await axios.get('/api/table-counts/');
        const rawData = response.data;
        tables.value = Object.keys(rawData).map(key => ({ name: key }));
      } catch (error) {
        console.error('Failed to fetch table list:', error);
      }
    };

    const viewTableData = (tableName) => {
      router.push({ name: 'TableDataView', params: { tableName } });
    };

    const handleRowClick = (row) => {
      viewTableData(row.name);
    };

    onMounted(() => {
      fetchTables();
    });

    return {
      tables,
      viewTableData,
      handleRowClick,
    };
  },
};
</script>

<style scoped>
.all-tables {
  padding: 32px 24px;
  background: #f7f8fa;
  min-height: 100vh;
}
.el-table {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  background: #fff;
}
.el-table th, .el-table td {
  font-size: 15px;
}
.el-button {
  background: linear-gradient(90deg, #409EFF 0%, #66b1ff 100%);
  color: #fff;
  border: none;
  border-radius: 4px;
}
</style>