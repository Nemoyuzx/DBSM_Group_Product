<template>
  <div class="departments">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>院系管理</h2>
          <el-button type="primary" @click="showAddDialog">添加院系</el-button>
        </div>
      </template>
      
      <!-- 搜索栏 -->
      <el-row :gutter="20" class="search-row">
        <el-col :span="6">
          <el-input v-model="searchQuery" placeholder="搜索院系..." clearable @clear="fetchDepartments">
            <template #append>
              <el-button @click="fetchDepartments">搜索</el-button>
            </template>
          </el-input>
        </el-col>
      </el-row>
      
      <!-- 数据表格 -->
      <el-table 
        :data="departments" 
        style="width: 100%" 
        v-loading="loading"
        border
      >
        <el-table-column prop="dept_id" label="ID" width="80" />
        <el-table-column prop="name" label="院系名称" />
        <el-table-column prop="inst_id" label="所属机构" width="120" />
        <el-table-column prop="phone" label="联系电话" width="120" />
        <el-table-column prop="office_location" label="办公地点" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="viewDepartment(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="editDepartment(scope.row)">编辑</el-button>
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
      :title="isEdit ? '编辑院系' : '添加院系'" 
      v-model="dialogVisible"
      width="50%"
    >
      <el-form :model="form" :rules="rules" ref="departmentForm" label-width="100px">
        <el-form-item label="院系名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="所属机构" prop="inst_id">
          <el-select v-model="form.inst_id" filterable placeholder="请选择机构">
            <el-option 
              v-for="inst in institutions" 
              :key="inst.inst_id" 
              :label="inst.name" 
              :value="inst.inst_id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="办公地点" prop="office_location">
          <el-input v-model="form.office_location" />
        </el-form-item>
        <el-form-item label="系主任" prop="chair_staff_id">
          <el-select 
            v-model="form.chair_staff_id" 
            filterable 
            remote 
            placeholder="请选择系主任" 
            :remote-method="searchStaffs"
            :loading="staffsLoading"
          >
            <el-option 
              v-for="staff in staffOptions" 
              :key="staff.staff_id" 
              :label="staff.staff_name" 
              :value="staff.staff_id" 
            />
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
      <p>确定要删除院系 {{ deleteItem?.name || '' }} 吗？此操作不可恢复。</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="deleteDepartment">确定删除</el-button>
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
  name: 'Departments',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    // 状态变量
    const departments = ref([])
    const institutions = ref([])
    const loading = ref(false)
    const error = ref(null)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalItems = ref(0)
    const searchQuery = ref('')
    
    // 对话框状态
    const dialogVisible = ref(false)
    const deleteDialogVisible = ref(false)
    const isEdit = ref(false)
    const deleteItem = ref(null)
    const departmentForm = ref(null)
    
    // 教职工选择相关
    const staffOptions = ref([])
    const staffsLoading = ref(false)
    
    // 表单数据
    const form = reactive({
      name: '',
      inst_id: null,
      phone: '',
      office_location: '',
      chair_staff_id: null
    })
    
    // 表单验证规则
    const rules = {
      name: [
        { required: true, message: '请输入院系名称', trigger: 'blur' }
      ],
      inst_id: [
        { required: true, message: '请选择所属机构', trigger: 'change' }
      ],
      office_location: [
        { required: true, message: '请输入办公地点', trigger: 'blur' }
      ]
    }
    
    // 获取院系列表
    const fetchDepartments = async () => {
      loading.value = true
      error.value = null
      try {
        let url = `departments/?page=${currentPage.value}`
        
        if (searchQuery.value) {
          url += `&search=${searchQuery.value}`
        }
        
        const response = await axios.get(url)
        departments.value = response.data.results || response.data
        totalItems.value = response.data.count || departments.value.length
      } catch (err) {
        error.value = err.message || '获取院系数据失败'
        console.error('Error fetching departments:', err)
      } finally {
        loading.value = false
      }
    }
    
    // 获取机构列表
    const fetchInstitutions = async () => {
      try {
        const response = await axios.get('institutions/')
        institutions.value = response.data.results || response.data
      } catch (err) {
        console.error('Error fetching institutions:', err)
      }
    }
    
    // 搜索教职工
    const searchStaffs = async (query) => {
      if (query.length < 2) return
      staffsLoading.value = true
      try {
        const response = await axios.get(`staffs/?search=${query}`)
        staffOptions.value = response.data.results || response.data
      } catch (err) {
        console.error('Error searching staffs:', err)
      } finally {
        staffsLoading.value = false
      }
    }
    
    // 显示添加对话框
    const showAddDialog = () => {
      isEdit.value = false
      Object.assign(form, {
        name: '',
        inst_id: null,
        phone: '',
        office_location: '',
        chair_staff_id: null
      })
      dialogVisible.value = true
    }
    
    // 编辑院系
    const editDepartment = (department) => {
      isEdit.value = true
      Object.assign(form, {
        dept_id: department.dept_id,
        name: department.name,
        inst_id: department.inst_id,
        phone: department.phone || '',
        office_location: department.office_location,
        chair_staff_id: department.chair_staff_id
      })
      dialogVisible.value = true
    }
    
    // 查看院系详情
    const viewDepartment = (department) => {
      // 可以实现详情页面，或者在当前页面显示详情对话框
      console.log('View department:', department)
    }
    
    // 确认删除对话框
    const confirmDelete = (department) => {
      deleteItem.value = department
      deleteDialogVisible.value = true
    }
    
    // 删除院系
    const deleteDepartment = async () => {
      try {
        await axios.delete(`departments/${deleteItem.value.dept_id}/`)
        await fetchDepartments()
        deleteDialogVisible.value = false
        deleteItem.value = null
      } catch (err) {
        console.error('Error deleting department:', err)
        error.value = err.message || '删除院系失败'
      }
    }
    
    // 提交表单
    const submitForm = async () => {
      if (!departmentForm.value) return
      
      await departmentForm.value.validate(async (valid) => {
        if (valid) {
          try {
            if (isEdit.value) {
              // 更新院系
              await axios.put(`departments/${form.dept_id}/`, form)
            } else {
              // 添加院系
              await axios.post('departments/', form)
            }
            dialogVisible.value = false
            await fetchDepartments()
          } catch (err) {
            console.error('Error saving department:', err)
            error.value = err.message || '保存院系数据失败'
          }
        }
      })
    }
    
    // 处理分页
    const handlePageChange = (page) => {
      currentPage.value = page
      fetchDepartments()
    }
    
    // 初始化
    onMounted(() => {
      fetchDepartments()
      fetchInstitutions()
    })
    
    return {
      departments,
      institutions,
      loading,
      error,
      currentPage,
      pageSize,
      totalItems,
      searchQuery,
      dialogVisible,
      deleteDialogVisible,
      isEdit,
      deleteItem,
      departmentForm,
      form,
      rules,
      staffOptions,
      staffsLoading,
      fetchDepartments,
      searchStaffs,
      showAddDialog,
      editDepartment,
      viewDepartment,
      confirmDelete,
      deleteDepartment,
      submitForm,
      handlePageChange
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