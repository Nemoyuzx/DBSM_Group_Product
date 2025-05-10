<template>
  <div class="courses">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>课程管理</h2>
          <el-button type="primary" @click="showAddDialog">添加课程</el-button>
        </div>
      </template>
      
      <!-- 搜索栏 -->
      <el-row :gutter="20" class="search-row">
        <el-col :span="6">
          <el-input v-model="searchQuery" placeholder="搜索课程..." clearable @clear="fetchCourses">
            <template #append>
              <el-button @click="fetchCourses">搜索</el-button>
            </template>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-select v-model="levelFilter" placeholder="课程级别" clearable @change="fetchCourses">
            <el-option label="本科" value="undergraduate" />
            <el-option label="研究生" value="graduate" />
            <el-option label="博士" value="phd" />
          </el-select>
        </el-col>
      </el-row>
      
      <!-- 数据表格 -->
      <el-table 
        :data="courses" 
        style="width: 100%" 
        v-loading="loading"
        border
      >
        <el-table-column prop="course_code" label="课程代码" width="120" />
        <el-table-column prop="title" label="课程名称" />
        <el-table-column prop="credit_value" label="学分" width="80" />
        <el-table-column prop="level" label="课程级别" width="100">
          <template #default="scope">
            {{ getCourseLevel(scope.row.level) }}
          </template>
        </el-table-column>
        <el-table-column prop="dept_id" label="所属院系" width="120" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="viewCourse(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="editCourse(scope.row)">编辑</el-button>
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
      :title="isEdit ? '编辑课程' : '添加课程'" 
      v-model="dialogVisible"
      width="50%"
    >
      <el-form :model="form" :rules="rules" ref="courseForm" label-width="100px">
        <el-form-item label="课程代码" prop="course_code">
          <el-input v-model="form.course_code" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="课程名称" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="学分" prop="credit_value">
          <el-input-number v-model="form.credit_value" :min="0" :max="10" :precision="1" :step="0.5" />
        </el-form-item>
        <el-form-item label="课程级别" prop="level">
          <el-select v-model="form.level" placeholder="请选择课程级别">
            <el-option label="本科" value="undergraduate" />
            <el-option label="研究生" value="graduate" />
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
        <el-form-item label="课程描述" prop="description">
          <el-input type="textarea" v-model="form.description" rows="4" />
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
      <p>确定要删除课程 {{ deleteItem?.title || '' }} 吗？此操作不可恢复。</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="deleteCourse">确定删除</el-button>
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
  name: 'Courses',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    // 状态变量
    const courses = ref([])
    const departments = ref([])
    const loading = ref(false)
    const error = ref(null)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalItems = ref(0)
    const searchQuery = ref('')
    const levelFilter = ref('')
    
    // 对话框状态
    const dialogVisible = ref(false)
    const deleteDialogVisible = ref(false)
    const isEdit = ref(false)
    const deleteItem = ref(null)
    const courseForm = ref(null)
    
    // 表单数据
    const form = reactive({
      course_code: '',
      title: '',
      credit_value: 3,
      level: 'undergraduate',
      dept_id: null,
      description: ''
    })
    
    // 表单验证规则
    const rules = {
      course_code: [
        { required: true, message: '请输入课程代码', trigger: 'blur' },
        { pattern: /^[A-Z]{2,4}\d{3,4}$/, message: '格式应为2-4个大写字母+3-4个数字，如CS101', trigger: 'blur' }
      ],
      title: [
        { required: true, message: '请输入课程名称', trigger: 'blur' }
      ],
      credit_value: [
        { required: true, message: '请输入学分', trigger: 'blur' },
        { type: 'number', message: '学分必须为数字', trigger: 'blur' }
      ],
      level: [
        { required: true, message: '请选择课程级别', trigger: 'change' }
      ],
      dept_id: [
        { required: true, message: '请选择所属院系', trigger: 'change' }
      ]
    }
    
    // 获取课程列表
    const fetchCourses = async () => {
      loading.value = true
      error.value = null
      try {
        let url = `courses/?page=${currentPage.value}`
        
        if (searchQuery.value) {
          url += `&search=${searchQuery.value}`
        }
        
        if (levelFilter.value) {
          url += `&level=${levelFilter.value}`
        }
        
        const response = await axios.get(url)
        courses.value = response.data.results || response.data
        totalItems.value = response.data.count || courses.value.length
      } catch (err) {
        error.value = err.message || '获取课程数据失败'
        console.error('Error fetching courses:', err)
      } finally {
        loading.value = false
      }
    }
    
    // 获取院系列表
    const fetchDepartments = async () => {
      try {
        const response = await axios.get('departments/')
        departments.value = response.data.results || response.data
      } catch (err) {
        console.error('Error fetching departments:', err)
      }
    }
    
    // 显示添加对话框
    const showAddDialog = () => {
      isEdit.value = false
      Object.assign(form, {
        course_code: '',
        title: '',
        credit_value: 3,
        level: 'undergraduate',
        dept_id: null,
        description: ''
      })
      dialogVisible.value = true
    }
    
    // 编辑课程
    const editCourse = (course) => {
      isEdit.value = true
      Object.assign(form, {
        course_code: course.course_code,
        title: course.title,
        credit_value: course.credit_value,
        level: course.level,
        dept_id: course.dept_id,
        description: course.description || ''
      })
      dialogVisible.value = true
    }
    
    // 查看课程详情
    const viewCourse = (course) => {
      router.push(`/courses/${course.course_code}`)
    }
    
    // 确认删除对话框
    const confirmDelete = (course) => {
      deleteItem.value = course
      deleteDialogVisible.value = true
    }
    
    // 删除课程
    const deleteCourse = async () => {
      try {
        await axios.delete(`courses/${deleteItem.value.course_code}/`)
        await fetchCourses()
        deleteDialogVisible.value = false
        deleteItem.value = null
      } catch (err) {
        console.error('Error deleting course:', err)
        error.value = err.message || '删除课程失败'
      }
    }
    
    // 提交表单
    const submitForm = async () => {
      if (!courseForm.value) return
      
      await courseForm.value.validate(async (valid) => {
        if (valid) {
          try {
            if (isEdit.value) {
              // 更新课程
              await axios.put(`courses/${form.course_code}/`, form)
            } else {
              // 添加课程
              await axios.post('courses/', form)
            }
            dialogVisible.value = false
            await fetchCourses()
          } catch (err) {
            console.error('Error saving course:', err)
            error.value = err.message || '保存课程数据失败'
          }
        }
      })
    }
    
    // 处理分页
    const handlePageChange = (page) => {
      currentPage.value = page
      fetchCourses()
    }
    
    // 获取课程级别显示文本
    const getCourseLevel = (level) => {
      const levelMap = {
        'undergraduate': '本科',
        'graduate': '研究生',
        'phd': '博士'
      }
      return levelMap[level] || level
    }
    
    // 初始化
    onMounted(() => {
      fetchCourses()
      fetchDepartments()
    })
    
    return {
      courses,
      departments,
      loading,
      error,
      currentPage,
      pageSize,
      totalItems,
      searchQuery,
      levelFilter,
      dialogVisible,
      deleteDialogVisible,
      isEdit,
      deleteItem,
      courseForm,
      form,
      rules,
      fetchCourses,
      showAddDialog,
      editCourse,
      viewCourse,
      confirmDelete,
      deleteCourse,
      submitForm,
      handlePageChange,
      getCourseLevel
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