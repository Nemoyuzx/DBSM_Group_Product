<template>
  <div class="courses">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('courses') }}</span>
          <el-button type="primary" @click="openAddDialog">{{ $t('add') }}</el-button>
        </div>
      </template>

      <el-table
          :data="courses"
          style="width: 100%"
          stripe
          v-loading="loading"
          @row-dblclick="openEditDialog"
      >
        <el-table-column prop="course_code" :label="$t('id')" width="120" />
        <el-table-column prop="title" :label="$t('course_name')" />
        <el-table-column prop="credit_value" :label="$t('credit')" width="100" />
        <el-table-column prop="language" :label="$t('language')" width="100" />
        <el-table-column fixed="right" :label="$t('actions')" width="120">
          <template #default="scope">
            <el-button size="small" @click="openEditDialog(scope.row)">{{ $t('edit') }}</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="error" class="error-text">{{ error }}</div>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog :title="editMode ? $t('edit') : $t('add')" v-model="dialogVisible" width="500px">
      <el-form :model="form" label-width="120px">
        <el-form-item :label="$t('id')">
          <el-input v-model="form.course_code" :disabled="editMode" />
        </el-form-item>
        <el-form-item :label="$t('course_name')">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item :label="$t('credit')">
          <el-input-number v-model="form.credit_value" :min="0" />
        </el-form-item>
        <el-form-item :label="$t('language')">
          <el-select v-model="form.language">
            <el-option label="中文" value="CN" />
            <el-option label="English" value="EN" />
            <el-option label="Bilingual" value="BI" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">{{ $t('back') }}</el-button>
        <el-button type="primary" @click="submitForm">{{ $t('confirm') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CoursesView',
  data() {
    return {
      courses: [],
      loading: false,
      error: null,
      dialogVisible: false,
      editMode: false,
      form: {
        course_code: '',
        title: '',
        credit_value: 3,
        language: 'EN'
      }
    }
  },
  mounted() {
    this.fetchCourses()
  },
  methods: {
    async fetchCourses() {
      this.loading = true
      this.error = null
      try {
        const res = await axios.get('/api/courses/')
        this.courses = res.data.results || res.data
      } catch (err) {
        this.error = this.$t('fetch_error')
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    openAddDialog() {
      this.editMode = false
      this.form = {
        course_code: '',
        title: '',
        credit_value: 3,
        language: 'EN'
      }
      this.dialogVisible = true
    },
    openEditDialog(row) {
      this.editMode = true
      this.form = { ...row }
      this.dialogVisible = true
    },
    async submitForm() {
      try {
        if (this.editMode) {
          await axios.put(`/api/courses/${this.form.course_code}/`, this.form)
        } else {
          await axios.post('/api/courses/', this.form)
        }
        this.dialogVisible = false
        this.fetchCourses()
      } catch (err) {
        console.error('提交失败:', err)
        this.error = this.$t('fetch_error')
      }
    }
  }
}
</script>

<style scoped>
.courses {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.error-text {
  color: #f56c6c;
  margin-top: 10px;
}
</style>