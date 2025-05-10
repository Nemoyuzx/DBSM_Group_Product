<template>
  <div class="course-detail">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h2>{{ course ? course.title : '加载中...' }} <small v-if="course">(代码: {{ course.course_code }})</small></h2>
          <div>
            <el-button @click="$router.push('/courses')">返回列表</el-button>
            <el-button type="primary" @click="editCourse" v-if="course">编辑</el-button>
          </div>
        </div>
      </template>
      
      <div v-if="course">
        <el-tabs>
          <el-tab-pane label="基本信息">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="课程代码">{{ course.course_code }}</el-descriptions-item>
              <el-descriptions-item label="课程名称">{{ course.title }}</el-descriptions-item>
              <el-descriptions-item label="学分">{{ course.credit_value }}</el-descriptions-item>
              <el-descriptions-item label="课程级别">
                {{ getCourseLevel(course.level) }}
              </el-descriptions-item>
              <el-descriptions-item label="所属院系">{{ departmentName }}</el-descriptions-item>
              <el-descriptions-item label="课程描述" :span="2">
                {{ course.description || '暂无描述' }}
              </el-descriptions-item>
            </el-descriptions>
          </el-tab-pane>
          
          <el-tab-pane label="教师信息">
            <div v-if="instructors && instructors.length > 0">
              <el-table :data="instructors" style="width: 100%">
                <el-table-column prop="staff_id" label="工号" width="100" />
                <el-table-column prop="legal_name" label="姓名" width="150" />
                <el-table-column prop="email" label="邮箱" />
                <el-table-column prop="role" label="角色" width="100" />
              </el-table>
            </div>
            <el-empty v-else description="暂无教师信息" />
          </el-tab-pane>
          
          <el-tab-pane label="学生名单">
            <div v-if="students && students.length > 0">
              <el-table :data="students" style="width: 100%">
                <el-table-column prop="student_id" label="学号" width="100" />
                <el-table-column prop="legal_name" label="姓名" width="150" />
                <el-table-column prop="email" label="邮箱" />
                <el-table-column prop="enrollment_status" label="状态" width="100">
                  <template #default="scope">
                    {{ getEnrollmentStatus(scope.row.enrollment_status) }}
                  </template>
                </el-table-column>
              </el-table>
            </div>
            <el-empty v-else description="暂无学生信息" />
          </el-tab-pane>
        </el-tabs>
      </div>
      
      <div v-else-if="error" class="error-message">
        <el-alert
          title="获取数据失败"
          type="error"
          :description="error"
          show-icon
        />
      </div>
    </el-card>
    
    <!-- 编辑对话框 -->
    <el-dialog 
      title="编辑课程信息" 
      v-model="dialogVisible"
      width="50%"
    >
      <el-form :model="form" :rules="rules" ref="courseForm" label-width="100px">
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
          <el-button type="primary" @click="submitForm">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

export default {
  name: 'CourseDetail',
  props: {
    id: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const route = useRoute()
    const router = useRouter()
    const courseForm = ref(null)
    
    const course = ref(null)
    const instructors = ref([])
    const students = ref([])
    const departments = ref([])
    const loading = ref(true)
    const error = ref('')
    const dialogVisible = ref(false)
    
    const departmentName = computed(() => {
      if (!course.value || !departments.value.length) return '未知'
      const dept = departments.value.find(d => d.dept_id === course.value.dept_id)
      return dept ? dept.name : '未知'
    })
    
    const form = reactive({
      course_code: '',
      title: '',
      credit_value: 3,
      level: '',
      dept_id: '',
      description: ''
    })
    
    const rules = {
      title: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
      credit_value: [{ required: true, message: '请输入学分', trigger: 'change' }],
      level: [{ required: true, message: '请选择课程级别', trigger: 'change' }],
      dept_id: [{ required: true, message: '请选择所属院系', trigger: 'change' }]
    }
    
    const getCourseLevel = (level) => {
      const levels = {
        'undergraduate': '本科',
        'graduate': '研究生',
        'phd': '博士'
      }
      return levels[level] || level
    }
    
    const getEnrollmentStatus = (status) => {
      const statuses = {
        'active': '在读',
        'graduated': '已毕业',
        'leave': '休学',
        'withdrawn': '退学'
      }
      return statuses[status] || status
    }
    
    const fetchCourse = async () => {
      loading.value = true
      error.value = ''
      try {
        const response = await axios.get(`/api/courses/${props.id}/`)
        course.value = response.data
        // 填充表单数据
        Object.assign(form, response.data)
      } catch (err) {
        console.error('获取课程详情失败:', err)
        error.value = err.response?.data?.detail || '获取课程详情失败'
      } finally {
        loading.value = false
      }
    }
    
    const fetchInstructors = async () => {
      try {
        const response = await axios.get(`/api/courses/${props.id}/instructors/`)
        instructors.value = response.data
      } catch (err) {
        console.error('获取教师信息失败:', err)
      }
    }
    
    const fetchStudents = async () => {
      try {
        const response = await axios.get(`/api/courses/${props.id}/students/`)
        students.value = response.data
      } catch (err) {
        console.error('获取学生信息失败:', err)
      }
    }
    
    const fetchDepartments = async () => {
      try {
        const response = await axios.get('/api/departments/')
        departments.value = response.data
      } catch (err) {
        console.error('获取院系信息失败:', err)
      }
    }
    
    const editCourse = () => {
      Object.assign(form, course.value)
      dialogVisible.value = true
    }
    
    const submitForm = async () => {
      if (!courseForm.value) return
      
      await courseForm.value.validate(async (valid) => {
        if (valid) {
          try {
            await axios.put(`/api/courses/${props.id}/`, form)
            ElMessage.success('课程信息更新成功')
            dialogVisible.value = false
            fetchCourse() // 刷新数据
          } catch (err) {
            console.error('更新课程信息失败:', err)
            ElMessage.error(err.response?.data?.detail || '更新课程信息失败')
          }
        }
      })
    }
    
    onMounted(() => {
      fetchCourse()
      fetchInstructors()
      fetchStudents()
      fetchDepartments()
    })
    
    return {
      course,
      instructors,
      students,
      departments,
      departmentName,
      loading,
      error,
      dialogVisible,
      form,
      rules,
      courseForm,
      getCourseLevel,
      getEnrollmentStatus,
      editCourse,
      submitForm
    }
  }
}
</script>

<style scoped>
.course-detail {
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

.error-message {
  margin-top: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>