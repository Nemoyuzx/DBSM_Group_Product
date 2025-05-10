<template>
  <div class="students">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>学生管理</h2>
          <el-button type="primary" @click="showAddDialog">添加学生</el-button>
        </div>
      </template>
      
      <!-- 搜索栏 -->
      <el-row :gutter="20" class="search-row">
        <el-col :span="6">
          <el-input v-model="searchQuery" placeholder="搜索学生..." clearable @clear="fetchStudents">
            <template #append>
              <el-button @click="fetchStudents">搜索</el-button>
            </template>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-select v-model="statusFilter" placeholder="注册状态" clearable @change="fetchStudents">
            <el-option label="在读" value="active" />
            <el-option label="休学" value="leave" />
            <el-option label="毕业" value="graduate" />
            <el-option label="退学" value="dismissed" />
          </el-select>
        </el-col>
      </el-row>
      
      <!-- 数据表格 -->
      <el-table 
        :data="students" 
        style="width: 100%" 
        v-loading="loading"
        border
      >
        <el-table-column prop="student_id" label="学号" width="100" />
        <el-table-column prop="student_name" label="姓名" />
        <el-table-column prop="admission_year" label="入学年份" width="100" />
        <el-table-column prop="enrollment_status" label="注册状态" width="100">
          <template #default="scope">
            {{ getEnrollmentStatus(scope.row.enrollment_status) }}
          </template>
        </el-table-column>
        <el-table-column prop="expected_grad_term" label="预计毕业学期" width="120" />
        <el-table-column prop="disability_flag" label="残障登记" width="80">
          <template #default="scope">
            {{ scope.row.disability_flag ? '是' : '否' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="viewStudent(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="editStudent(scope.row)">编辑</el-button>
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
      :title="isEdit ? '编辑学生' : '添加学生'" 
      v-model="dialogVisible"
      width="50%"
    >
      <el-form :model="form" :rules="rules" ref="studentForm" label-width="100px">
        <el-form-item label="学生" prop="student_id" v-if="!isEdit">
          <el-select 
            v-model="form.student_id" 
            filterable 
            remote 
            placeholder="请选择人员" 
            :remote-method="searchPersons"
            :loading="personsLoading"
          >
            <el-option 
              v-for="person in personOptions" 
              :key="person.person_id" 
              :label="`${person.legal_name} (${person.person_id})`" 
              :value="person.person_id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="入学年份" prop="admission_year">
          <el-input-number v-model="form.admission_year" :min="2000" :max="2100" />
        </el-form-item>
        <el-form-item label="注册状态" prop="enrollment_status">
          <el-select v-model="form.enrollment_status" placeholder="请选择注册状态">
            <el-option label="在读" value="active" />
            <el-option label="休学" value="leave" />
            <el-option label="毕业" value="graduate" />
            <el-option label="退学" value="dismissed" />
          </el-select>
        </el-form-item>
        <el-form-item label="预计毕业学期" prop="expected_grad_term">
          <el-input v-model="form.expected_grad_term" placeholder="例如: 202306" />
        </el-form-item>
        <el-form-item label="残障登记" prop="disability_flag">
          <el-switch v-model="form.disability_flag" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 删除确认对话框 -->
    <el-dialog
      title="确认删除"
      v-model="deleteDialogVisible"
      width="30%"
    >
      <p>确定要删除学生 {{ deleteItem?.student_name || '' }} 吗？此操作不可恢复。</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="deleteStudent">确定删除</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import axios from 'axios'

export default {
  name: 'Students',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    // 状态变量
    const students = ref([])
    const loading = ref(false)
    const error = ref(null)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalItems = ref(0)
    const searchQuery = ref('')
    const statusFilter = ref('')
    
    // 对话框状态
    const dialogVisible = ref(false)
    const deleteDialogVisible = ref(false)
    const isEdit = ref(false)
    const deleteItem = ref(null)
    const studentForm = ref(null)
    
    // 人员选择相关
    const personOptions = ref([])
    const personsLoading = ref(false)
    
    // 表单数据
    const form = reactive({
      student_id: '',
      admission_year: new Date().getFullYear(),
      enrollment_status: 'active',
      expected_grad_term: '',
      disability_flag: false
    })
    
    // 表单验证规则
    const rules = {
      student_id: [
        { required: true, message: '请选择人员', trigger: 'change' }
      ],
      admission_year: [
        { required: true, message: '请输入入学年份', trigger: 'blur' },
        { type: 'number', message: '入学年份必须为数字', trigger: 'blur' }
      ],
      enrollment_status: [
        { required: true, message: '请选择注册状态', trigger: 'change' }
      ],
      expected_grad_term: [
        { required: true, message: '请输入预计毕业学期', trigger: 'blur' },
        { pattern: /^\d{6}$/, message: '格式应为6位数字，如202306', trigger: 'blur' }
      ]
    }
    
    // 获取学生列表
    const fetchStudents = async () => {
      loading.value = true
      error.value = null
      try {
        let url = `students/?page=${currentPage.value}`
        
        if (searchQuery.value) {
          url += `&search=${searchQuery.value}`
        }
        
        if (statusFilter.value) {
          url += `&enrollment_status=${statusFilter.value}`
        }
        
        const response = await axios.get(url)
        students.value = response.data.results || response.data
        totalItems.value = response.data.count || students.value.length
      } catch (err) {
        error.value = err.message || '获取学生数据失败'
        console.error('Error fetching students:', err)
      } finally {
        loading.value = false
      }
    }
    
    // 搜索人员
    const searchPersons = async (query) => {
      if (query.length < 2) return
      personsLoading.value = true
      try {
        const response = await axios.get(`persons/?search=${query}`)
        personOptions.value = response.data.results || response.data
      } catch (err) {
        console.error('Error searching persons:', err)
      } finally {
        personsLoading.value = false
      }
    }
    
    // 显示添加对话框
    const showAddDialog = () => {
      isEdit.value = false
      Object.assign(form, {
        student_id: '',
        admission_year: new Date().getFullYear(),
        enrollment_status: 'active',
        expected_grad_term: '',
        disability_flag: false
      })
      dialogVisible.value = true
    }
    
    // 编辑学生
    const editStudent = (student) => {
      isEdit.value = true
      Object.assign(form, {
        student_id: student.student_id,
        admission_year: student.admission_year,
        enrollment_status: student.enrollment_status,
        expected_grad_term: student.expected_grad_term,
        disability_flag: student.disability_flag
      })
      dialogVisible.value = true
    }
    
    // 查看学生详情
    const viewStudent = (student) => {
      router.push(`/persons/${student.student_id}`)
    }
    
    // 确认删除对话框
    const confirmDelete = (student) => {
      deleteItem.value = student
      deleteDialogVisible.value = true
    }
    
    // 删除学生
    const deleteStudent = async () => {
      try {
        await axios.delete(`students/${deleteItem.value.student_id}/`)
        await fetchStudents()
        deleteDialogVisible.value = false
        deleteItem.value = null
      } catch (err) {
        console.error('Error deleting student:', err)
        error.value = err.message || '删除学生失败'
      }
    }
    
    // 提交表单
    const submitForm = async () => {
      if (!studentForm.value) return
      
      await studentForm.value.validate(async (valid) => {
        if (valid) {
          try {
            if (isEdit.value) {
              // 更新学生
              await axios.put(`students/${form.student_id}/`, form)
            } else {
              // 添加学生
              await axios.post('students/', form)
            }
            dialogVisible.value = false
            await fetchStudents()
          } catch (err) {
            console.error('Error saving student:', err)
            error.value = err.message || '保存学生数据失败'
          }
        }
      })
    }
    
    // 处理分页
    const handlePageChange = (page) => {
      currentPage.value = page
      fetchStudents()
    }
    
    // 获取注册状态显示文本
    const getEnrollmentStatus = (status) => {
      const statusMap = {
        'active': '在读',
        'leave': '休学',
        'graduate': '毕业',
        'dismissed': '退学'
      }
      return statusMap[status] || status
    }
    
    // 初始化
    onMounted(() => {
      fetchStudents()
    })
    
    return {
      students,
      loading,
      error,
      currentPage,
      pageSize,
      totalItems,
      searchQuery,
      statusFilter,
      dialogVisible,
      deleteDialogVisible,
      isEdit,
      deleteItem,
      studentForm,
      form,
      rules,
      personOptions,
      personsLoading,
      fetchStudents,
      searchPersons,
      showAddDialog,
      editStudent,
      viewStudent,
      confirmDelete,
      deleteStudent,
      submitForm,
      handlePageChange,
      getEnrollmentStatus
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