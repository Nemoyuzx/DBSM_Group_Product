<template>
  <div class="persons">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>人员管理</h2>
          <el-button type="primary" @click="showAddDialog">添加人员</el-button>
        </div>
      </template>
      
      <!-- 搜索栏 -->
      <el-row :gutter="20" class="search-row">
        <el-col :span="6">
          <el-input v-model="searchQuery" placeholder="搜索人员..." clearable @clear="fetchPersons">
            <template #append>
              <el-button @click="fetchPersons">搜索</el-button>
            </template>
          </el-input>
        </el-col>
      </el-row>
      
      <!-- 数据表格 -->
      <el-table 
        :data="persons" 
        style="width: 100%" 
        v-loading="loading"
        border
      >
        <el-table-column prop="person_id" label="ID" width="80" />
        <el-table-column prop="legal_name" label="法定姓名" />
        <el-table-column prop="preferred_name" label="常用名" />
        <el-table-column prop="sex_at_birth" label="性别" width="80">
          <template #default="scope">
            {{ scope.row.sex_at_birth === 'M' ? '男' : scope.row.sex_at_birth === 'F' ? '女' : '未定义' }}
          </template>
        </el-table-column>
        <el-table-column prop="birth_date" label="出生日期" width="120" />
        <el-table-column prop="email" label="电子邮箱" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="viewPerson(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="editPerson(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="confirmDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-if="totalItems > 0"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="totalItems"
          layout="total, prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog 
      :title="isEdit ? '编辑人员' : '添加人员'" 
      v-model="dialogVisible"
      width="50%"
    >
      <el-form :model="form" :rules="rules" ref="personForm" label-width="100px">
        <el-form-item label="法定姓名" prop="legal_name">
          <el-input v-model="form.legal_name" />
        </el-form-item>
        <el-form-item label="常用名" prop="preferred_name">
          <el-input v-model="form.preferred_name" />
        </el-form-item>
        <el-form-item label="性别" prop="sex_at_birth">
          <el-select v-model="form.sex_at_birth" placeholder="请选择性别">
            <el-option label="男" value="M" />
            <el-option label="女" value="F" />
            <el-option label="未定义" value="U" />
          </el-select>
        </el-form-item>
        <el-form-item label="性别认同" prop="gender_identity">
          <el-input v-model="form.gender_identity" />
        </el-form-item>
        <el-form-item label="出生日期" prop="birth_date">
          <el-date-picker v-model="form.birth_date" type="date" placeholder="选择日期" />
        </el-form-item>
        <el-form-item label="身份证号" prop="national_id">
          <el-input v-model="form.national_id" />
        </el-form-item>
        <el-form-item label="电话号码" prop="phone_number">
          <el-input v-model="form.phone_number" />
        </el-form-item>
        <el-form-item label="电子邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'Persons',
  data() {
    return {
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      totalItems: 0,
      dialogVisible: false,
      isEdit: false,
      form: {
        legal_name: '',
        preferred_name: '',
        sex_at_birth: '',
        gender_identity: '',
        birth_date: '',
        national_id: '',
        phone_number: '',
        email: ''
      },
      rules: {
        legal_name: [{ required: true, message: '请输入法定姓名', trigger: 'blur' }],
        preferred_name: [{ required: true, message: '请输入常用名', trigger: 'blur' }],
        sex_at_birth: [{ required: true, message: '请选择性别', trigger: 'change' }],
        birth_date: [{ required: true, message: '请选择出生日期', trigger: 'change' }],
        national_id: [{ required: true, message: '请输入身份证号', trigger: 'blur' }],
        phone_number: [{ required: true, message: '请输入电话号码', trigger: 'blur' }],
        email: [
          { required: true, message: '请输入电子邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的电子邮箱格式', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapState([
      'persons',
      'loading',
      'error'
    ])
  },
  created() {
    this.fetchPersons()
  },
  methods: {
    ...mapActions([
      'fetchPersons',
      'createItem',
      'updateItem',
      'deleteItem'
    ]),
    async fetchPersons() {
      try {
        const response = await this.$axios.get('persons/', {
          params: {
            search: this.searchQuery,
            page: this.currentPage
          }
        })
        this.$store.commit('SET_PERSONS', response.data.results || response.data)
        this.totalItems = response.data.count || response.data.length
      } catch (error) {
        console.error('获取人员列表失败:', error)
      }
    },
    handlePageChange(page) {
      this.currentPage = page
      this.fetchPersons()
    },
    showAddDialog() {
      this.isEdit = false
      this.form = {
        legal_name: '',
        preferred_name: '',
        sex_at_birth: '',
        gender_identity: '',
        birth_date: '',
        national_id: '',
        phone_number: '',
        email: ''
      }
      this.dialogVisible = true
    },
    editPerson(person) {
      this.isEdit = true
      this.form = { ...person }
      this.dialogVisible = true
    },
    viewPerson(person) {
      this.$router.push({ name: 'PersonDetail', params: { id: person.person_id } })
    },
    async submitForm() {
      this.$refs.personForm.validate(async (valid) => {
        if (valid) {
          try {
            if (this.isEdit) {
              // 更新人员
              await this.updateItem({
                endpoint: 'persons/',
                id: this.form.person_id,
                data: this.form,
                mutation: 'UPDATE_PERSON'
              })
              this.$message.success('人员信息更新成功')
            } else {
              // 创建人员
              await this.createItem({
                endpoint: 'persons/',
                data: this.form,
                mutation: 'ADD_PERSON'
              })
              this.$message.success('人员添加成功')
            }
            this.dialogVisible = false
            this.fetchPersons()
          } catch (error) {
            this.$message.error(error.message || '操作失败')
          }
        }
      })
    },
    confirmDelete(person) {
      this.$confirm('此操作将永久删除该人员, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await this.deleteItem({
            endpoint: 'persons/',
            id: person.person_id,
            mutation: 'DELETE_PERSON'
          })
          this.$message.success('删除成功')
          this.fetchPersons()
        } catch (error) {
          this.$message.error(error.message || '删除失败')
        }
      }).catch(() => {
        this.$message.info('已取消删除')
      })
    }
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.search-row {
  margin-bottom: 20px;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>