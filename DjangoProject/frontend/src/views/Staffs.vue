<template>
  <div class="staffs">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>教职工管理</h2>
          <el-button type="primary" @click="showAddDialog">添加教职工</el-button>
        </div>
      </template>
      
      <!-- 搜索栏 -->
      <el-row :gutter="20" class="search-row">
        <el-col :span="6">
          <el-input v-model="searchQuery" placeholder="搜索教职工..." clearable @clear="fetchStaffs">
            <template #append>
              <el-button @click="fetchStaffs">搜索</el-button>
            </template>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-select v-model="statusFilter" placeholder="在职状态" clearable @change="fetchStaffs">
            <el-option label="在职" value="active" />
            <el-option label="休假" value="leave" />
            <el-option label="退休" value="retired" />
          </el-select>
        </el-col>
      </el-row>
      
      <!-- 数据表格 -->
      <el-table 
        :data="staffs" 
        style="width: 100%" 
        v-loading="loading"
        border
      >
        <el-table-column prop="staff_id" label="工号" width="100" />
        <el-table-column prop="staff_name" label="姓名" />
        <el-table-column prop="hire_date" label="入职日期" width="120" />
        <el-table-column prop="employment_type" label="雇佣类型" width="100">
          <template #default="scope">
            {{ getEmploymentType(scope.row.employment_type) }}
          </template>
        </el-table-column>
        <el-table-column prop="staff_status" label="在职状态" width="100">
          <template #default="scope">
            {{ getStaffStatus(scope.row.staff_status) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="viewStaff(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="editStaff(scope.row)">编辑</el-button>
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
      :title="isEdit ? '编辑教职工' : '添加教职工'" 
      v-model="dialogVisible"
      width="50%"
    >
      <el-form :model="form" :rules="rules" ref="staffForm" label-width="100px">
        <el-form-item label="人员" prop="staff_id" v-if="!isEdit">
          <el-select 
            v-model="form.staff_id" 
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
        <el-form-item label="入职日期" prop="hire_date">
          <el-date-picker v-model="form.hire_date" type="date" placeholder="选择日期" />
        </el-form-item>
        <el-form-item label="雇佣类型" prop="employment_type">
          <el-select v-model="form.employment_type" placeholder="请选择雇佣类型">
            <el-option label="全职" value="full-time" />
            <el-option label="兼职" value="part-time" />
            <el-option label="临时" value="adjunct" />
            <el-option label="助教" value="GTA" />
          </el-select>
        </el-form-item>
        <el-form-item label="在职状态" prop="staff_status">
          <el-select v-model="form.staff_status" placeholder="请选择在职状态">
            <el-option label="在职" value="active" />
            <el-option label="休假" value="leave" />
            <el-option label="退休" value="retired" />
          </el-select>
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
      <p>确定要删除教职工 {{ deleteItem?.staff_name || '' }} 吗？此操作不可恢复。</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="deleteStaff">确定删除</el-button>
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
  name: 'Staffs',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    // 状态变量
    const staffs = ref([])
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
    const staffForm = ref(null)
    
    // 人员选择相关
    const personOptions = ref([])
    const personsLoading = ref(false)
    
    // 表单数据
    const form = reactive({
      staff_id: '',
      hire_date: new Date(),
      employment_type: 'full-time',
      staff_status: 'active'
    })
    
    // 表单验证规则
    const rules = {
      staff_id: [
        { required: true, message: '请选择人员', trigger: 'change' }
      ],
      hire_date: [
        { required: true, message: '请选择入职日期', trigger: 'change' }
      ],
      employment_type: [
        { required: true, message: '请选择雇佣类型', trigger: 'change' }
      ],
      staff_status: [
        { required: true, message: '请选择在职状态', trigger: 'change' }
      ]
    }
    
    // 获取教职工列表
    const fetchStaffs = async () => {
      loading.value = true
      error.value = null
      try {
        let url = `staffs/?page=${currentPage.value}`
        
        if (searchQuery.value) {
          url += `&search=${searchQuery.value}`
        }
        
        if (statusFilter.value) {
          url += `&staff_status=${statusFilter.value}`
        }
        
        const response = await axios.get(url)
        staffs.value = response.data.results || response.data
        totalItems.value = response.data.count || staffs.value.length
      } catch (err) {
        error.value = err.message || '获取教职工数据失败'
        console.error('Error fetching staffs:', err)
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
        staff_id: '',
        hire_date: new Date(),
        employment_type: 'full-time',
        staff_status: 'active'
      })
      dialogVisible.value = true
    }
    
    // 编辑教职工
    const editStaff = (staff) => {
      isEdit.value = true
      Object.assign(form, {
        staff_id: staff.staff_id,
        hire_date: staff.hire_date,
        employment_type: staff.employment_type,
        staff_status: staff.staff_status
      })
      dialogVisible.value = true
    }
    
    // 查看教职工详情
    const viewStaff = (staff) => {
      router.push(`/persons/${staff.staff_id}`)
    }
    
    // 确认删除对话框
    const confirmDelete = (staff) => {
      deleteItem.value = staff
      deleteDialogVisible.value = true
    }
    
    // 删除教职工
    const deleteStaff = async () => {
      try {
        await axios.delete(`staffs/${deleteItem.value.staff_id}/`)
        await fetchStaffs()
        deleteDialogVisible.value = false
        deleteItem.value = null
      } catch (err) {
        console.error('Error deleting staff:', err)
        error.value = err.message || '删除教职工失败'
      }
    }
    
    // 提交表单
    const submitForm = async () => {
      if (!staffForm.value) return
      
      await staffForm.value.validate(async (valid) => {
        if (valid) {
          try {
            if (isEdit.value) {
              // 更新教职工
              await axios.put(`staffs/${form.staff_id}/`, form)
            } else {
              // 添加教职工
              await axios.post('staffs/', form)
            }
            dialogVisible.value = false
            await fetchStaffs()
          } catch (err) {
            console.error('Error saving staff:', err)
            error.value = err.message || '保存教职工数据失败'
          }
        }
      })
    }
    
    // 处理分页
    const handlePageChange = (page) => {
      currentPage.value = page
      fetchStaffs()
    }
    
    // 获取雇佣类型显示文本
    const getEmploymentType = (type) => {
      const typeMap = {
        'full-time': '全职',
        'part-time': '兼职',
        'adjunct': '临时',
        'GTA': '助教'
      }
      return typeMap[type] || type
    }
    
    // 获取在职状态显示文本
    const getStaffStatus = (status) => {
      const statusMap = {
        'active': '在职',
        'leave': '休假',
        'retired': '退休'
      }
      return statusMap[status] || status
    }
    
    // 初始化
    onMounted(() => {
      fetchStaffs()
    })
    
    return {
      staffs,
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
      staffForm,
      form,
      rules,
      personOptions,
      personsLoading,
      fetchStaffs,
      searchPersons,
      showAddDialog,
      editStaff,
      viewStaff,
      confirmDelete,
      deleteStaff,
      submitForm,
      handlePageChange,
      getEmploymentType,
      getStaffStatus
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