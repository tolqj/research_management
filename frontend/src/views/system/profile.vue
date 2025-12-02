<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>个人信息</span>
      </div>
    </template>
    
    <!-- 基本信息 -->
    <el-form
      ref="userFormRef"
      :model="userInfo"
      :rules="userRules"
      label-width="100px"
      style="max-width: 600px"
    >
      <el-form-item label="用户名" prop="username">
        <el-input v-model="userInfo.username" disabled />
      </el-form-item>
      <el-form-item label="姓名" prop="name">
        <el-input v-model="userInfo.name" placeholder="请输入姓名" />
      </el-form-item>
      <el-form-item label="角色">
        <el-tag :type="getRoleType(userInfo.role)">{{ userInfo.role }}</el-tag>
      </el-form-item>
      <el-form-item label="职称" prop="title">
        <el-input v-model="userInfo.title" placeholder="如：教授、副教授" />
      </el-form-item>
      <el-form-item label="学院" prop="college">
        <el-input v-model="userInfo.college" placeholder="请输入学院" />
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="userInfo.email" placeholder="请输入邮箱" />
      </el-form-item>
      <el-form-item label="电话" prop="phone">
        <el-input v-model="userInfo.phone" placeholder="请输入电话" />
      </el-form-item>
      <el-form-item label="研究方向" prop="research_field">
        <el-input
          v-model="userInfo.research_field"
          type="textarea"
          :rows="3"
          placeholder="请输入研究方向"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSave" :loading="saving">保存信息</el-button>
        <el-button @click="resetUserForm">重置</el-button>
      </el-form-item>
    </el-form>

    <el-divider />
    
    <!-- 修改密码 -->
    <h3 style="margin-bottom: 20px">修改密码</h3>
    <el-alert
      title="密码要求"
      type="info"
      :closable="false"
      style="max-width: 600px; margin-bottom: 20px"
    >
      <p style="margin: 5px 0">• 长度至少 8 位</p>
      <p style="margin: 5px 0">• 必须包含大写字母、小写字母、数字和特殊字符</p>
      <p style="margin: 5px 0">• 建议每 90 天更换一次密码</p>
    </el-alert>
    
    <el-form
      ref="passwordFormRef"
      :model="passwordForm"
      :rules="passwordRules"
      label-width="100px"
      style="max-width: 600px"
    >
      <el-form-item label="旧密码" prop="old_password">
        <el-input
          v-model="passwordForm.old_password"
          type="password"
          show-password
          placeholder="请输入旧密码"
        />
      </el-form-item>
      <el-form-item label="新密码" prop="new_password">
        <el-input
          v-model="passwordForm.new_password"
          type="password"
          show-password
          placeholder="请输入新密码"
          @input="checkPasswordStrength"
        />
        <div v-if="passwordForm.new_password" style="margin-top: 8px">
          <el-progress
            :percentage="passwordStrength.percentage"
            :color="passwordStrength.color"
            :format="() => passwordStrength.text"
          />
        </div>
      </el-form-item>
      <el-form-item label="确认密码" prop="confirm_password">
        <el-input
          v-model="passwordForm.confirm_password"
          type="password"
          show-password
          placeholder="请再次输入新密码"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleChangePassword" :loading="changingPassword">
          修改密码
        </el-button>
        <el-button @click="resetPasswordForm">重置</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/store/user'
import { getCurrentUser, updateCurrentUser, changePassword } from '@/services/user'

const router = useRouter()
const userStore = useUserStore()

const userFormRef = ref(null)
const passwordFormRef = ref(null)
const saving = ref(false)
const changingPassword = ref(false)

const userInfo = reactive({
  username: '',
  name: '',
  role: '',
  title: '',
  college: '',
  email: '',
  phone: '',
  research_field: ''
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const passwordStrength = reactive({
  percentage: 0,
  color: '#f56c6c',
  text: '弱'
})

// 表单验证规则
const userRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入新密码'))
  } else if (value.length < 8) {
    callback(new Error('密码长度至少为 8 位'))
  } else if (!/[A-Z]/.test(value)) {
    callback(new Error('密码必须包含至少一个大写字母'))
  } else if (!/[a-z]/.test(value)) {
    callback(new Error('密码必须包含至少一个小写字母'))
  } else if (!/[0-9]/.test(value)) {
    callback(new Error('密码必须包含至少一个数字'))
  } else if (!/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(value)) {
    callback(new Error('密码必须包含至少一个特殊字符'))
  } else {
    callback()
  }
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== passwordForm.new_password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  old_password: [
    { required: true, message: '请输入旧密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// 密码强度检测
const checkPasswordStrength = () => {
  const password = passwordForm.new_password
  let strength = 0
  
  if (password.length >= 8) strength += 20
  if (password.length >= 12) strength += 20
  if (/[a-z]/.test(password)) strength += 15
  if (/[A-Z]/.test(password)) strength += 15
  if (/[0-9]/.test(password)) strength += 15
  if (/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password)) strength += 15
  
  passwordStrength.percentage = strength
  
  if (strength < 40) {
    passwordStrength.color = '#f56c6c'
    passwordStrength.text = '弱'
  } else if (strength < 70) {
    passwordStrength.color = '#e6a23c'
    passwordStrength.text = '中'
  } else {
    passwordStrength.color = '#67c23a'
    passwordStrength.text = '强'
  }
}

// 角色标签颜色
const getRoleType = (role) => {
  const roleMap = {
    '管理员': 'danger',
    '普通教师': 'primary',
    '科研秘书': 'success'
  }
  return roleMap[role] || 'info'
}

// 加载用户信息
const loadUserInfo = async () => {
  try {
    const res = await getCurrentUser()
    Object.assign(userInfo, res.data)
  } catch (error) {
    ElMessage.error('加载用户信息失败')
  }
}

// 保存用户信息
const handleSave = async () => {
  if (!userFormRef.value) return
  
  await userFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      try {
        await updateCurrentUser(userInfo)
        // 更新store中的用户信息
        userStore.setUser(userInfo)
        ElMessage.success('保存成功')
        await loadUserInfo()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '保存失败')
      } finally {
        saving.value = false
      }
    }
  })
}

// 重置用户表单
const resetUserForm = () => {
  loadUserInfo()
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await ElMessageBox.confirm(
          '修改密码后需要重新登录，确认要修改吗？',
          '确认修改',
          {
            type: 'warning',
            confirmButtonText: '确定',
            cancelButtonText: '取消'
          }
        )
        
        changingPassword.value = true
        await changePassword({
          old_password: passwordForm.old_password,
          new_password: passwordForm.new_password
        })
        
        ElMessage.success('密码修改成功，请重新登录')
        
        // 延迟跳转，让用户看到成功提示
        setTimeout(() => {
          userStore.logout()
          router.push('/login')
        }, 1500)
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error(error.response?.data?.detail || '密码修改失败')
        }
      } finally {
        changingPassword.value = false
      }
    }
  })
}

// 重置密码表单
const resetPasswordForm = () => {
  passwordFormRef.value?.resetFields()
  passwordStrength.percentage = 0
}

onMounted(() => {
  loadUserInfo()
})
</script>
