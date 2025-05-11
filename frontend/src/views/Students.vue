<template>
  <div class="students">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('students') }}</span>
          <div>
            <el-input v-model="search" placeholder="Search by ID or Name" size="small" clearable @input="fetchStudents" />
            <el-button type="primary" size="small" @click="openDialog(null)">+ {{ $t('add') }}</el-button>
          </div>
        </div>
      </template>

      <el-table
          v-loading="loading"
          :data="filteredStudents"
          style="width: 100%"
          stripe
          @row-click="goToDetail"
      >
        <el-table-column prop="student_id" label="ID" width="80" />
        <el-table-column prop="student_name" :label="$t('name')" />
        <el-table-column prop="enrollment_status" :label="$t('status')" />
        <el-table-column prop="admission_year" :label="$t('admission')" />
        <el-table-column fixed="right" :label="$t('actions')" min-width="160">
          <template #default="scope">
            <div class="action-buttons">
              <el-button size="small" @click.stop="openDialog(scope.row)">✏️</el-button>
              <el-button size="small" type="danger" @click.stop="deleteStudent(scope.row)">🗑️</el-button>
              <el-button size="small" type="primary" @click.stop="goToDetail(scope.row)">View</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="error" class="error-text">{{ error }}</div>
    </el-card>

    <!-- 添加/编辑弹窗 -->
    <el-dialog :title="editingStudent ? 'Edit Student' : 'Add Student'" v-model="dialogVisible" width="500px">
      <el-form :model="form" label-width="120px">
        <el-form-item label="Student Name">
          <el-input v-model="form.student_name" />
        </el-form-item>
        <el-form-item label="Admission Year">
          <el-input v-model="form.admission_year" />
        </el-form-item>
        <el-form-item label="Status">
          <el-select v-model="form.enrollment_status" placeholder="Select">
            <el-option label="active" value="active" />
            <el-option label="inactive" value="inactive" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitForm">Submit</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StudentsView',
  data() {
    return {
      students: [],
      search: '',
      loading: false,
      error: null,
      dialogVisible: false,
      editingStudent: null,
      form: {
        student_name: '',
        admission_year: '',
        enrollment_status: ''
      }
    }
  },
  computed: {
    filteredStudents() {
      return this.students.filter(s =>
          String(s.student_id).includes(this.search) ||
          s.student_name.toLowerCase().includes(this.search.toLowerCase())
      )
    }
  },
  mounted() {
    this.fetchStudents()
  },
  methods: {
    async fetchStudents() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/students/?ordering=admission_year')
        this.students = response.data.results
      } catch (err) {
        console.error(err)
        this.error = this.$t('fetch_error')
      } finally {
        this.loading = false
      }
    },
    goToDetail(student) {
      this.$router.push(`/students/${student.student_id}`)
    },
    openDialog(student) {
      this.editingStudent = student
      if (student) {
        this.form = { ...student }
      } else {
        this.form = { student_name: '', admission_year: '', enrollment_status: '' }
      }
      this.dialogVisible = true
    },
    async submitForm() {
      try {
        if (this.editingStudent) {
          await axios.put(`/api/students/${this.editingStudent.student_id}/`, this.form)
        } else {
          await axios.post('/api/students/', this.form)
        }
        this.dialogVisible = false
        this.fetchStudents()
      } catch (err) {
        console.error('Submit failed', err)
      }
    },
    async deleteStudent(student) {
      try {
        await axios.delete(`/api/students/${student.student_id}/`)
        this.fetchStudents()
      } catch (err) {
        console.error('Delete failed', err)
      }
    }
  }
}
</script>

<style scoped>
.students {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-header > div {
  display: flex;
  gap: 10px;
}
.action-buttons {
  display: flex;
  gap: 6px;
}
.error-text {
  color: #f56c6c;
  margin-top: 10px;
}
</style>