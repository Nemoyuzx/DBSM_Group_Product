<template>
  <div class="programs">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('programs') }}</span>
          <el-button type="primary" @click="openAddDialog">{{ $t('add') }}</el-button>
        </div>
      </template>

      <el-table :data="programs" style="width: 100%" v-loading="loading" stripe>
        <el-table-column prop="program_id" :label="$t('id')" width="100" />
        <el-table-column prop="name" :label="$t('program_name')" />
        <el-table-column prop="degree_type" label="Degree" />
        <el-table-column fixed="right" :label="$t('actions')" width="120">
          <template #default="scope">
            <el-button size="small" @click="openEditDialog(scope.row)">{{ $t('edit') }}</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="error" class="error-text">{{ error }}</div>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible">
      <el-form :model="form">
        <el-form-item :label="$t('name')">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="Degree">
          <el-input v-model="form.degree_type" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">{{ $t('cancel') }}</el-button>
        <el-button type="primary" @click="submitForm">{{ $t('confirm') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProgramsView',
  data() {
    return {
      programs: [],
      loading: false,
      error: null,
      dialogVisible: false,
      dialogTitle: '',
      form: {
        program_id: null,
        name: '',
        degree_type: ''
      }
    }
  },
  mounted() {
    this.fetchPrograms()
  },
  methods: {
    async fetchPrograms() {
      this.loading = true
      try {
        const res = await axios.get('/api/programs/')
        this.programs = res.data.results || res.data
      } catch (err) {
        console.error(err)
        this.error = this.$t('fetch_error')
      } finally {
        this.loading = false
      }
    },
    openAddDialog() {
      this.dialogTitle = this.$t('add')
      this.form = { program_id: null, name: '', degree_type: '' }
      this.dialogVisible = true
    },
    openEditDialog(program) {
      this.dialogTitle = this.$t('edit')
      this.form = { ...program }
      this.dialogVisible = true
    },
    async submitForm() {
      try {
        if (this.form.program_id) {
          // 编辑
          await axios.put(`/api/programs/${this.form.program_id}/`, this.form)
        } else {
          // 添加
          await axios.post('/api/programs/', this.form)
        }
        this.dialogVisible = false
        this.fetchPrograms()
      } catch (err) {
        console.error(err)
        this.$message.error(this.$t('fetch_error'))
      }
    }
  }
}
</script>

<style scoped>
.programs {
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