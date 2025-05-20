<!-- src/views/StudentDetail.vue -->
<template>
  <div class="student-detail" shadow="hover">
    <el-card v-if="student" class="box-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('student_detail') }}</span>
          <el-button @click="$router.back()">{{ $t('back') }}</el-button>
        </div>
      </template>

      <el-descriptions :title="$t('student_info')" column="2" border>
        <el-descriptions-item :label="$t('name')">{{ student.student_name }}</el-descriptions-item>
        <el-descriptions-item :label="$t('admission')">{{ student.admission_year }}</el-descriptions-item>
        <el-descriptions-item :label="$t('status')">{{ student.enrollment_status }}</el-descriptions-item>
        <el-descriptions-item :label="$t('grad_term')">{{ student.expected_grad_term }}</el-descriptions-item>
        <el-descriptions-item :label="$t('disability')">
          {{ student.disability_flag ? $t('yes') : $t('no') }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- 关联的 Person 信息展示 -->
      <el-descriptions :title="$t('person_info')" column="2" border class="mt-20">
        <el-descriptions-item :label="$t('person_id')">{{ student.person_id }}</el-descriptions-item>
        <el-descriptions-item :label="$t('preferred_name')">{{ student.person.preferred_name }}</el-descriptions-item>
        <el-descriptions-item :label="$t('birth_date')">{{ student.person.birth_date }}</el-descriptions-item>
        <el-descriptions-item :label="$t('email')">{{ student.person.email }}</el-descriptions-item>
        <el-descriptions-item :label="$t('phone')">{{ student.person.phone_number }}</el-descriptions-item>
      </el-descriptions>

      <!-- GPA 趋势分析（模拟数据） -->
      <el-card class="mt-30" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>📊 GPA Trend</span>
          </div>
        </template>
        <el-table :data="gpaTrend" style="width: 100%" border>
          <el-table-column prop="term" label="Term" />
          <el-table-column prop="gpa" label="GPA" />
        </el-table>
      </el-card>
    </el-card>

    <div v-else class="loading">
      <el-skeleton rows="4" animated />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const student = ref(null);
const gpaTrend = ref([]);

onMounted(async () => {
  try {
    const id = route.params.id;
    const res = await axios.get(`/api/students/${id}/`);
    student.value = res.data;

    // 模拟 GPA 趋势数据
    gpaTrend.value = [
      { term: '2022F', gpa: 3.2 },
      { term: '2023S', gpa: 3.5 },
      { term: '2023F', gpa: 3.1 },
      { term: '2024S', gpa: 3.6 }
    ]
  } catch (err) {
    console.error('Failed to load student detail:', err);
  }
});
</script>

<style scoped>
.student-detail {
  padding: 20px;
}
.mt-30 {
  margin-top: 30px;
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