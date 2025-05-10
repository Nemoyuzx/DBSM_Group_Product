<template>
  <div class="person-detail">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h2>{{ person ? person.legal_name : '加载中...' }} <small v-if="person">(ID: {{ person.person_id }})</small></h2>
          <div>
            <el-button @click="$router.push('/persons')">返回列表</el-button>
            <el-button type="primary" @click="editPerson" v-if="person">编辑</el-button>
          </div>
        </div>
      </template>
      
      <div v-if="person">
        <el-tabs>
          <el-tab-pane label="基本信息">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="身份证/护照号">{{ person.national_id }}</el-descriptions-item>
              <el-descriptions-item label="法定姓名">{{ person.legal_name }}</el-descriptions-item>
              <el-descriptions-item label="常用名">{{ person.preferred_name }}</el-descriptions-item>
              <el-descriptions-item label="性别">
                {{ person.sex_at_birth === 'M' ? '男' : person.sex_at_birth === 'F' ? '女' : '未定义' }}
              </el-descriptions-item>
              <el-descriptions-item label="性别认同">{{ person.gender_identity || '未指定' }}</el-descriptions-item>
              <el-descriptions-item label="出生日期">{{ person.birth_date }}</el-descriptions-item>
              <el-descriptions-item label="电话">{{ person.phone_number }}</el-descriptions-item>
              <el-descriptions-item label="电子邮箱">{{ person.email }}</el-descriptions-item>
              <el-descriptions-item label="主要地址" :span="2">
                {{ personAddress || '未指定' }}
              </el-descriptions-item>
            </el-descriptions>
          </el-tab-pane>
          
          <el-tab-pane label="学生信息" v-if="studentInfo">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="学号">{{ studentInfo.student_id }}</el-descriptions-item>
              <el-descriptions-item label="入学年份">{{ studentInfo.admission_year }}</el-descriptions-item>
              <el-descriptions-item label="注册状态">{{ getEnrollmentStatus(studentInfo.enrollment_status) }}</el-descriptions-item>
              <el-descriptions-item label="预计毕业学期">{{ studentInfo.expected_grad_term }}</el-descriptions-item>
              <el-descriptions-item label="残障登记">{{ studentInfo.disability_flag ? '是' : '否' }}</el-descriptions-item>
            </el-descriptions>
          </el-tab-pane>
          
          <el-tab-pane label="教职工信息" v-if="staffInfo">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="工号">{{ staffInfo.staff_id }}</el-descriptions-item>
              <el-descriptions-item label="入职日期">{{ staffInfo.hire_date }}</el-descriptions-item>
              <el-descriptions-item label="雇佣类型">{{ getEmploymentType(staffInfo.employment_type) }}</el-descriptions-item>
              <el-descriptions-item label="状态">{{ getStaffStatus(staffInfo.staff_status) }}</el-descriptions-item>
            </el-descriptions>
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
      title="编辑人员信息" 
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
  name: 'PersonDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      person: null,
      studentInfo: null,
      staffInfo: null,
      personAddress: null,
      dialogVisible: false,
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
      'loading',
      'error'
    ])
  },
  created() {
    this.fetchPersonDetail()
  },
  methods: {
    ...mapActions([
      'fetchItemDetail',
      'updateItem'
    ]),
    async fetchPersonDetail() {
      try {
        this.$store.commit('SET_LOADING', true)
        // 获取人员详细信息
        const response = await this.$axios.get(`persons/${this.id}/full_info/`)
        this.person = response.data
        this.studentInfo = response.data.student
        this.staffInfo = response.data.staff
        
        // 如果有地址ID，获取地址信息
        if (this.person.primary_address_id) {
          const addressResponse = await this.$axios.get(`addresses/${this.person.primary_address_id}/`)
          this.personAddress = `${addressResponse.data.line1}, ${addressResponse.data.city}, ${addressResponse.data.province}, ${addressResponse.data.country}`
        }
      } catch (error) {
        this.$store.commit('SET_ERROR', error.message || '获取人员详情失败')
        console.error('获取人员详情失败:', error)
      } finally {
        this.$store.commit('SET_LOADING', false)
      }
    },
    getEnrollmentStatus(status) {
      const statusMap = {
        'active': '在读',
        'leave': '休学',
        'graduate': '毕业',
        'dismissed': '退学'
      }
      return statusMap[status] || status
    },
    getEmploymentType(type) {
      const typeMap = {
        'full-time': '全职',
        'part-time': '兼职',
        'adjunct': '客座',
        'GTA': '助教'
      }
      return typeMap[type] || type
    },
    getStaffStatus(status) {
      const statusMap = {
        'active': '在职',
        'leave': '休假',
        'retired': '退休'
      }
      return statusMap[status] || status
    },
    editPerson() {
      this.form = { ...this.person }
      this.dialogVisible = true
    },
    async submitForm() {
      this.$refs.personForm.validate(async (valid) => {
        if (valid) {
          try {
            await this.updateItem({
              endpoint: 'persons/',
              id: this.person.person_id,
              data: this.form
            })
            this.$message.success('人员信息更新成功')
            this.dialogVisible = false
            this.fetchPersonDetail()
          } catch (error) {
            this.$message.error(error.message || '更新失败')
          }
        }
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
.error-message {
  margin: 20px 0;
}
</style>