<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>用户管理</span>
        <el-button type="primary" @click="handleAdd">新增用户</el-button>
      </div>
    </template>

    <!-- 搜索区域 -->
    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="用户名">
        <el-input v-model="searchForm.keyword" placeholder="请输入用户名" clearable />
      </el-form-item>
      <el-form-item label="角色">
        <el-select v-model="searchForm.role" placeholder="请选择角色" clearable>
          <el-option label="管理员" value="管理员" />
          <el-option label="普通教师" value="普通教师" />
          <el-option label="科研秘书" value="科研秘书" />
        </el-select>
      </el-form-item>
      <el-form-item label="学院">
        <el-input v-model="searchForm.college" placeholder="请输入学院" clearable />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSearch" :icon="Search">搜索</el-button>
        <el-button @click="handleReset" :icon="Refresh">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 表格 -->
    <el-table
      :data="tableData"
      v-loading="loading"
      stripe
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="name" label="姓名" width="100" />
      <el-table-column prop="role" label="角色" width="110">
        <template #default="{ row }">
          <el-tag :type="getRoleType(row.role)">{{ row.role }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="title" label="职称" width="100" />
      <el-table-column prop="college" label="学院" min-width="120" show-overflow-tooltip />
      <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
      <el-table-column prop="phone" label="电话" width="120" />
      <el-table-column prop="created_at" label="创建时间" width="160">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            @click="handleEdit(row)"
            :icon="Edit"
          >
            编辑
          </el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(row)"
            :icon="Delete"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      v-model:current-page="pagination.page"
      v-model:page-size="pagination.pageSize"
      :page-sizes="[10, 20, 50, 100]"
      :total="pagination.total"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handlePageChange"
      style="margin-top: 20px; justify-content: flex-end"
    />

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="formData.username"
            placeholder="请输入用户名"
            :disabled="isEdit"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input
            v-model="formData.password"
            type="password"
            show-password
            placeholder="请输入密码"
          />
          <div style="color: #909399; font-size: 12px; margin-top: 4px">
            密码要求：8位+大小写+数字+特殊字符
          </div>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="formData.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="formData.role" placeholder="请选择角色">
            <el-option label="管理员" value="管理员" />
            <el-option label="普通教师" value="普通教师" />
            <el-option label="科研秘书" value="科研秘书" />
          </el-select>
        </el-form-item>
        <el-form-item label="职称" prop="title">
          <el-input v-model="formData.title" placeholder="如：教授、副教授" />
        </el-form-item>
        <el-form-item label="学院" prop="college">
          <el-input v-model="formData.college" placeholder="请输入学院" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入电话" />
        </el-form-item>
        <el-form-item label="研究方向" prop="research_field">
          <el-input
            v-model="formData.research_field"
            type="textarea"
            :rows="3"
            placeholder="请输入研究方向"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Refresh, Edit, Delete } from '@element-plus/icons-vue'
import { getUserList, createUser, updateUser, deleteUser } from '@/services/user'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新增用户')
const isEdit = ref(false)
const formRef = ref(null)

const searchForm = reactive({
  keyword: '',
  role: '',
  college: ''
})

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const tableData = ref([])

const formData = reactive({
  id: null,
  username: '',
  password: '',
  name: '',
  role: '普通教师',
  title: '',
  college: '',
  email: '',
  phone: '',
  research_field: ''
})

// 密码验证规则
const validatePassword = (rule, value, callback) => {
  if (!isEdit.value) {
    if (!value) {
      callback(new Error('请输入密码'))
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
  } else {
    callback()
  }
}

const formRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在03-20个字符', trigger: 'blur' }
  ],
  password: [
    { validator: validatePassword, trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
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

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 加载用户列表
const loadUserList = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.page - 1) * pagination.pageSize,
      limit: pagination.pageSize
    }
    
    if (searchForm.role) {
      params.role = searchForm.role
    }
    if (searchForm.college) {
      params.college = searchForm.college
    }
    
    const res = await getUserList(params)
    // 后端直接返回数组，不需要 .data
    tableData.value = res
    pagination.total = res.length
  } catch (error) {
    console.error('加载用户列表失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载用户列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  loadUserList()
}

// 重置
const handleReset = () => {
  searchForm.keyword = ''
  searchForm.role = ''
  searchForm.college = ''
  pagination.page = 1
  loadUserList()
}

// 分页
const handleSizeChange = (val) => {
  pagination.pageSize = val
  pagination.page = 1
  loadUserList()
}

const handlePageChange = (val) => {
  pagination.page = val
  loadUserList()
}

// 新增
const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增用户'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑用户'
  Object.assign(formData, row)
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row) => {
  // 防止删除自己
  if (row.id === userStore.user?.id) {
    ElMessage.warning('不能删除当前登录的用户')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确认要删除用户“${row.name}”吗？`,
      '警告',
      {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }
    )
    
    await deleteUser(row.id)
    ElMessage.success('删除成功')
    loadUserList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (isEdit.value) {
          // 编辑
          const { id, created_at, updated_at, ...updateData } = formData
          await updateUser(formData.id, updateData)
          ElMessage.success('更新成功')
        } else {
          // 新增
          await createUser(formData)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadUserList()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  formData.id = null
  formData.username = ''
  formData.password = ''
  formData.name = ''
  formData.role = '普通教师'
  formData.title = ''
  formData.college = ''
  formData.email = ''
  formData.phone = ''
  formData.research_field = ''
  formRef.value?.clearValidate()
}

// 关闭对话框
const handleDialogClose = () => {
  resetForm()
}

onMounted(() => {
  loadUserList()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}
</style>
