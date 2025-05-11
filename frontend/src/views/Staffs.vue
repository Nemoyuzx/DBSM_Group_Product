<template>
  <div class="staffs">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('staffs') }}</span>
          <el-button type="primary" @click="openDialog()">{{ $t('add') }}</el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="staffs" stripe style="width: 100%">
        <el-table-column prop="staff_id" :label="$t('id')" width="80" />
        <el-table-column prop="legal_name" :label="$t('name')" />
        <el-table-column prop="employment_type" :label="$t('employment_type')" />
        <el-table-column prop="staff_status" :label="$t('staff_status')" />
        <el-table-column prop="hire_date" :label="$t('hire_date')" />
        <el-table-column fixed="right" :label="$t('actions')" width="140">
          <template #default="scope">
            <el-button size="small" @click="openDialog(scope.row)">✏️</el-button>
            <el-button size="small" type="danger" @click="deleteStaff(scope.row)">🗑️</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="error" class="error-text">{{ error }}</div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="editMode ? $t('edit') : $t('add')" width="500px">
      <el-form :model="form">
        <el-form-item :label="$t('id')">
          <el-input v-model="form.staff_id" :disabled="editMode" />
        </el-form-item>
        <el-form-item :label="$t('name')">
          <el-input v-model="form.legal_name" />
        </el-form-item>
        <el-form-item :label="$t('employment_type')">
          <el-input v-model="form.employment_type" />
        </el-form-item>
        <el-form-item :label="$t('staff_status')">
          <el-input v-model="form.staff_status" />
        </el-form-item>
        <el-form-item :label="$t('hire_date')">
          <el-date-picker v-model="form.hire_date" type="date" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">{{ $t('back') }}</el-button>
        <el-button type="primary" @click="saveStaff">{{ $t('confirm') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'StaffsView',
  data() {
    return {
      staffs: [],
      loading: false,
      error: null,
      dialogVisible: false,
      editMode: false,
      form: {
        staff_id: '',
        legal_name: '',
        employment_type: '',
        staff_status: '',
        hire_date: ''
      }
    };
  },
  mounted() {
    this.fetchStaffs();
  },
  methods: {
    async fetchStaffs() {
      this.loading = true;
      try {
        const res = await axios.get('/api/staffs/');
        this.staffs = res.data.results || res.data;
      } catch (err) {
        this.error = this.$t('fetch_error');
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    openDialog(staff = null) {
      if (staff) {
        this.editMode = true;
        this.form = { ...staff };
      } else {
        this.editMode = false;
        this.form = {
          staff_id: '',
          legal_name: '',
          employment_type: '',
          staff_status: '',
          hire_date: ''
        };
      }
      this.dialogVisible = true;
    },
    async saveStaff() {
      try {
        if (this.editMode) {
          await axios.put(`/api/staffs/${this.form.staff_id}/`, this.form);
        } else {
          await axios.post('/api/staffs/', this.form);
        }
        this.dialogVisible = false;
        this.fetchStaffs();
      } catch (err) {
        console.error(err);
        alert(this.$t('fetch_error'));
      }
    },
    async deleteStaff(row) {
      if (confirm(`${this.$t('confirm_delete')} ${row.legal_name}?`)) {
        try {
          await axios.delete(`/api/staffs/${row.staff_id}/`);
          this.fetchStaffs();
        } catch (err) {
          console.error(err);
          alert(this.$t('fetch_error'));
        }
      }
    }
  }
};
</script>

<style scoped>
.staffs {
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