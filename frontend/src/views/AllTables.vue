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

export default {
  name: 'AllTables',
  setup() {
    const tables = ref([]);
    const router = useRouter();

    // 模拟从API获取表名列表
    const fetchTables = async () => {
      // 在实际应用中，这里会调用后端API
      // 例如: const response = await fetch('/api/tables');
      // const data = await response.json();
      // tables.value = data;
      // 此处为模拟数据
      tables.value = [
        { name: 'Departments' },
        { name: 'Programs' },
        { name: 'Courses' },
        { name: 'Students' },
        { name: 'Staffs' },
        // 根据实际后端API返回的表名进行填充
      ];
    };

    const viewTableData = (tableName) => {
      // 跳转到通用的表数据展示页，并传递表名参数
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