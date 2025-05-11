<!-- src/views/Departments.vue -->
<template>
  <div class="departments">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('departments') }}</span>
          <el-button type="primary" @click="openDialog()">{{ $t('add') }}</el-button>
        </div>
      </template>

      <el-table
          v-loading="loading"
          :data="departments"
          style="width: 100%"
          stripe
      >
        <el-table-column prop="dept_id" :label="$t('id')" width="80" />
        <el-table-column prop="name" :label="$t('name')" />
        <el-table-column prop="office_location" label="Location" />
        <el-table-column fixed="right" :label="$t('actions')" width="120">
          <template #default="scope">
            <el-button size="mini" @click="openDialog(scope.row)">Edit</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="error" class="error-text">{{ error }}</div>
    </el-card>

    <!-- 弹窗 -->
    <el-dialog :title="formData.dept_id ? 'Edit Department' : 'Add Department'" v-model="dialogVisible">
      <el-form :model="formData" label-width="100px">
        <el-form-item label="Name">
          <el-input v-model="formData.name" />
        </el-form-item>
        <el-form-item label="Location">
          <el-input v-model="formData.office_location" />
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
  name: 'DepartmentsView',
  data() {
    return {
      departments: [],
      loading: false,
      error: null,
      dialogVisible: false,
      formData: {
        dept_id: null,
        name: '',
        office_location: ''
      }
    }
  },
  mounted() {
    this.fetchDepartments()
  },
  methods: {
    async fetchDepartments() {
      this.loading = true
      try {
        const res = await axios.get('/api/departments/')
        this.departments = res.data.results || res.data
      } catch (err) {
        console.error(err)
        this.error = this.$t('fetch_error')
      } finally {
        this.loading = false
      }
    },
    openDialog(dept = null) {
      if (dept) {
        this.formData = { ...dept }
      } else {
        this.formData = { dept_id: null, name: '', office_location: '' }
      }
      this.dialogVisible = true
    },
    async submitForm() {
      try {
        if (this.formData.dept_id) {
          await axios.put(`/api/departments/${this.formData.dept_id}/`, this.formData)
        } else {
          await axios.post('/api/departments/', this.formData)
        }
        this.dialogVisible = false
        this.fetchDepartments()
      } catch (err) {
        console.error('Failed to submit:', err)
        this.$message.error('Failed to submit department data.')
      }
    }
  }
}
</script>

<style scoped>
.departments {
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