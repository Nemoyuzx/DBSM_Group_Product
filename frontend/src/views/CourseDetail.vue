<template>
  <div class="course-detail">
    <el-card v-if="course" class="course-info-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('course_detail') }}</span>
          <el-button text @click="$router.back()">{{ $t('back') }}</el-button>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item :label="$t('id')">{{ course.course_code }}</el-descriptions-item>
        <el-descriptions-item :label="$t('name')">{{ course.title }}</el-descriptions-item>
        <el-descriptions-item :label="$t('credit')">{{ course.credit_value }}</el-descriptions-item>
        <el-descriptions-item :label="$t('language')">{{ formatLanguage(course.language) }}</el-descriptions-item>
        <el-descriptions-item :label="$t('grading')">{{ formatGrading(course.default_grading_scheme) }}</el-descriptions-item>
        <el-descriptions-item :label="$t('department')">{{ course.owning_dept_name || '--' }}</el-descriptions-item>
        <el-descriptions-item :label="$t('canonical')">{{ course.canonical_flag ? $t('yes') : $t('no') }}</el-descriptions-item>
        <el-descriptions-item :label="$t('syllabus')">{{ course.syllabus_blob || '--' }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="offering-list-card mt-20">
      <template #header>
        <div class="card-header">
          <span>{{ $t('offerings') }}</span>
        </div>
      </template>

      <el-table v-if="offerings.length" :data="offerings" stripe border style="width: 100%">
        <el-table-column prop="term_code" :label="$t('term')"></el-table-column>
        <el-table-column prop="section_number" :label="$t('section')"></el-table-column>
        <el-table-column prop="delivery_mode" :label="$t('mode')"></el-table-column>
        <el-table-column prop="campus" :label="$t('campus')"></el-table-column>
        <el-table-column prop="room_id" :label="$t('room')"></el-table-column>
        <el-table-column prop="capacity" :label="$t('capacity')"></el-table-column>
        <el-table-column prop="waitlist_capacity" :label="$t('waitlist')"></el-table-column>
        <el-table-column prop="status" :label="$t('status')"></el-table-column>
      </el-table>
      <div v-else class="empty-tip">{{ $t('no_data') }}</div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'

export default {
  name: 'CourseDetail',
  setup() {
    const route = useRoute()
    const courseId = route.params.id
    const course = ref(null)
    const offerings = ref([])

    const fetchCourse = async () => {
      try {
        const res = await axios.get(`/api/courses/${courseId}/`)
        course.value = res.data
      } catch (e) {
        console.error('Failed to load course', e)
      }
    }

    const fetchOfferings = async () => {
      try {
        const res = await axios.get(`/api/courses/${courseId}/offerings/`)
        offerings.value = res.data
      } catch (e) {
        console.error('Failed to load offerings', e)
      }
    }

    const formatLanguage = (val) => {
      switch (val) {
        case 'CN': return '中文'
        case 'EN': return 'English'
        case 'BI': return 'Bilingual'
        default: return val
      }
    }

    const formatGrading = (val) => {
      switch (val) {
        case 'letter': return 'Letter Grade'
        case 'percent': return 'Percent'
        case 'passfail': return 'Pass/Fail'
        default: return val
      }
    }

    onMounted(() => {
      fetchCourse()
      fetchOfferings()
    })

    return { course, offerings, formatLanguage, formatGrading }
  }
}
</script>

<style scoped>
.course-detail {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.mt-20 {
  margin-top: 20px;
}
.empty-tip {
  text-align: center;
  color: #999;
  padding: 20px;
}
</style>