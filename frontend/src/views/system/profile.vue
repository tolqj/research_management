<template>
  <el-card>
    <template #header>
      <span>个人信息</span>
    </template>
    
    <el-form :model="userInfo" label-width="100px" style="max-width: 600px">
      <el-form-item label="用户名">
        <el-input v-model="userInfo.username" disabled />
      </el-form-item>
      <el-form-item label="姓名">
        <el-input v-model="userInfo.name" />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="userInfo.email" />
      </el-form-item>
      <el-form-item label="电话">
        <el-input v-model="userInfo.phone" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </el-form-item>
    </el-form>

    <el-divider />
    
    <h3>修改密码</h3>
    <el-form :model="passwordForm" label-width="100px" style="max-width: 600px">
      <el-form-item label="旧密码">
        <el-input v-model="passwordForm.old_password" type="password" />
      </el-form-item>
      <el-form-item label="新密码">
        <el-input v-model="passwordForm.new_password" type="password" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleChangePassword">修改密码</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import { updateCurrentUser, changePassword } from '@/services/user'

const userStore = useUserStore()

const userInfo = reactive({
  username: '',
  name: '',
  email: '',
  phone: ''
})

const passwordForm = reactive({
  old_password: '',
  new_password: ''
})

const handleSave = async () => {
  try {
    await updateCurrentUser(userInfo)
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const handleChangePassword = async () => {
  try {
    await changePassword(passwordForm)
    ElMessage.success('密码修改成功，请重新登录')
    userStore.logout()
    router.push('/login')
  } catch (error) {
    ElMessage.error('密码修改失败')
  }
}

onMounted(() => {
  if (userStore.user) {
    Object.assign(userInfo, userStore.user)
  }
})
</script>
