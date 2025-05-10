<template>
  <div class="programs">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>教学计划管理</h2>
          <el-button type="primary" @click="showAddDialog">添加教学计划</el-button>
        </div>
      </template>
      
      <!-- 搜索栏 -->
      <el-row :gutter="20" class="search-row">
        <el-col :span="6">
          <el-input v-model="searchQuery" placeholder="搜索教学计划..." clearable @clear="fetchPrograms">
            <template #append>
              <el-button @click="fetchPrograms">搜索</el-button>
            </template>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-select v-model="degreeFilter" placeholder="学位类型" clearable @change="fetchPrograms">
            <el-option label="学士" value="bachelor" />
            <el-option label="硕士" value="master" />
            <el-option label="博士" value="phd" />
          </el-select>
        </el-col>
      </el-row>
      
      <!-- 数据表格 -->
      <el-table 
        :data="programs" 
        style="width: 100%" 
        v-loading="loading"
        border
      >
        <el-table-column prop="program_id" label="计划编号" width="120" />
        <el-table-column prop="name" label="计划名称" />
        <el-table-column prop="degree_type" label="学位类型" width="100">
          <template #default="scope">
            {{ getDegreeType(scope.row.degree_type) }}
          </template>
        </el-table-column>
        <el-table-column prop="dept_id" label="所属院系" width="120" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="viewProgram(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="editProgram(scope.row)">编辑</el-button>
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
      :title="isEdit ? '编辑教学计划' : '添加教学计划'" 
      v-model="dialogVisible"
      width="50%"
    >
      <el-form :model="form" :rules="rules" ref="programForm" label-width="100px">
        <el-form-item label="计划名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="学位类型" prop="degree_type">
          <el-select v-model="form.degree_type" placeholder="请选择学位类型">
            <el-option label="学士" value="bachelor" />
            <el-option label="硕士" value="master" />
            <el-option label="博士" value="phd" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属院系" prop="dept_id">
          <el-select v-model="form.dept_id" filterable placeholder="请选择院系">
            <el-option 
              v-for="dept in departments" 
              :key="dept.dept_id" 
              :label="dept.name" 
              :value="dept.dept_id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="学分要求" prop="credit_requirement">
          <el-input-number v-model="form.credit_requirement" :min="0" :precision="0" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="form.description" rows="4" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

export default {
  name: 'Programs',
  setup() {
    const programForm = ref(null)
    const programs = ref([])
    const departments = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalItems = ref(0)
    const searchQuery = ref('')
    const degreeFilter = ref('')
    
    const form = reactive({
      program_id: '',
      name: '',
      degree_type: '',
      dept_id: '',
      credit_requirement: 120,
      description: ''
    })
    
    const rules = {
      name: [{ required: true, message: '请输入计划名称', trigger: 'blur' }],
      degree_type: [{ required: true, message: '请选择学位类型', trigger: 'change' }],
      dept_id: [{ required: true, message: '请选择所属院系', trigger: 'change' }],
      credit_requirement: [{ required: true, message: '请输入学分要求', trigger: 'change' }]
    }
    
    const getDegreeType = (type) => {
      const types = {
        'bachelor': '学士',
        'master': '硕士',
        'phd': '博士'
      }
      return types[type] || type
    }
    
    const fetchPrograms = async () => {
      loading.value = true
      try {
        let url = `/api/programs/?page=${currentPage.value}`
        if (searchQuery.value) {
          url += `&search=${searchQuery.value}`
        }
        if (degreeFilter.value) {
          url += `&degree_type=${degreeFilter.value}`
        }
        
        const response = await axios.get(url)
        programs.value = response.data.results || response.data
        totalItems.value = response.data.count || programs.value.length
      } catch (err) {
        console.error('获取教学计划列表失败:', err)
        ElMessage.error('获取教学计划列表失败')
      } finally {
        loading.value = false
      }
    }
    
    const fetchDepartments = async () => {
      try {
        const response = await axios.get('/api/departments/')
        departments.value = response.data.results || response.data
      } catch (err) {
        console.error('获取院系列表失败:', err)
      }
    }
    
    const resetForm = () => {
      if (programForm.value) {
        programForm.value.resetFields()
      }
      form.program_id = ''
      form.name = ''
      form.degree_type = ''
      form.dept_id = ''
      form.credit_requirement = 120
      form.description = ''
    }
    
    const showAddDialog = () => {
      isEdit.value = false
      resetForm()
      dialogVisible.value = true
    }
    
    const editProgram = (row) => {
      isEdit.value = true
      resetForm()
      Object.assign(form, row)
      dialogVisible.value = true
    }
    
    const viewProgram = (row) => {
      // 如果有详情页面，可以跳转到详情页
      // router.push(`/programs/${row.program_id}`)
      ElMessage.info('查看教学计划详情功能正在开发中')
    }
    
    const submitForm = async () => {
      if (!programForm.value) return
      
      await programForm.value.validate(async (valid) => {
        if (valid) {
          try {
            if (isEdit.value) {
              await axios.put(`/api/programs/${form.program_id}/`, form)
              ElMessage.success('更新教学计划成功')
            } else {
              await axios.post('/api/programs/', form)
              ElMessage.success('添加教学计划成功')
            }
            dialogVisible.value = false
            fetchPrograms()
          } catch (err) {
            console.error('保存教学计划失败:', err)
            ElMessage.error(err.response?.data?.detail || '保存教学计划失败')
          }
        }
      })
    }
    
    const confirmDelete = (row) => {
      ElMessageBox.confirm(
        '确定要删除这个教学计划吗？此操作不可逆。',
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      ).then(async () => {
        try {
          await axios.delete(`/api/programs/${row.program_id}/`)
          ElMessage.success('删除成功')
          fetchPrograms()
        } catch (err) {
          console.error('删除教学计划失败:', err)
          ElMessage.error(err.response?.data?.detail || '删除教学计划失败')
        }
      }).catch(() => {
        ElMessage.info('已取消删除')
      })
    }
    
    const handlePageChange = (page) => {
      currentPage.value = page
      fetchPrograms()
    }
    
    onMounted(() => {
      fetchPrograms()
      fetchDepartments()
    })
    
    return {
      programs,
      departments,
      loading,
      dialogVisible,
      isEdit,
      form,
      rules,
      programForm,
      currentPage,
      pageSize,
      totalItems,
      searchQuery,
      degreeFilter,
      getDegreeType,
      fetchPrograms,
      showAddDialog,
      editProgram,
      viewProgram,
      submitForm,
      confirmDelete,
      handlePageChange
    }
  }
}
</script>

<style scoped>
.programs {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
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