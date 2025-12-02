<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>成果管理</span>
        <el-button type="primary" @click="handleAdd">新增成果</el-button>
      </div>
    </template>

    <!-- 筛选条件 -->
    <el-form :inline="true" :model="queryParams" class="search-form">
      <el-form-item label="成果类型">
        <el-select v-model="queryParams.achievement_type" placeholder="请选择成果类型" clearable style="width: 150px">
          <el-option key="PATENT" label="专利" value="PATENT" />
          <el-option key="AWARD" label="奖项" value="AWARD" />
          <el-option key="BOOK" label="著作" value="BOOK" />
          <el-option key="SOFTWARE" label="软件著作权" value="SOFTWARE" />
        </el-select>
      </el-form-item>
      <el-form-item label="所有人">
        <el-input v-model="queryParams.owner" placeholder="所有人" clearable style="width: 150px" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadAchievements">查询</el-button>
        <el-button @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 成果列表 -->
    <el-table :data="achievements" border style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="achievement_type" label="成果类型" width="120">
        <template #default="{ row }">
          <el-tag :type="getTypeTag(row.achievement_type)">{{ getTypeLabel(row.achievement_type) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="title" label="成果名称" width="300" show-overflow-tooltip />
      <el-table-column prop="owner" label="所有人" width="100" />
      <el-table-column prop="members" label="参与人员" width="200" show-overflow-tooltip />
      <el-table-column prop="completion_date" label="完成日期" width="120" />
      <el-table-column prop="certificate_no" label="证书编号" width="150" />
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="form.id ? '编辑成果' : '新增成果'"
      width="700px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="成果类型" prop="achievement_type">
          <el-select v-model="form.achievement_type" placeholder="请选择成果类型" style="width: 100%">
            <el-option key="PATENT" label="专利" value="PATENT" />
            <el-option key="AWARD" label="奖项" value="AWARD" />
            <el-option key="BOOK" label="著作" value="BOOK" />
            <el-option key="SOFTWARE" label="软件著作权" value="SOFTWARE" />
          </el-select>
        </el-form-item>
        <el-form-item label="成果名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入成果名称" />
        </el-form-item>
        <el-form-item label="所有人" prop="owner">
          <el-input v-model="form.owner" placeholder="请输入所有人" />
        </el-form-item>
        <el-form-item label="参与人员">
          <el-input v-model="form.members" placeholder="请输入参与人员，多人用逗号分隔" />
        </el-form-item>
        <el-form-item label="完成日期" prop="completion_date">
          <el-date-picker
            v-model="form.completion_date"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="证书编号" prop="certificate_no">
          <el-input v-model="form.certificate_no" placeholder="请输入证书编号" />
        </el-form-item>
        <el-form-item label="成果描述">
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请输入成果描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/services/request'

const loading = ref(false)
const achievements = ref([])
const dialogVisible = ref(false)
const formRef = ref(null)

const queryParams = reactive({
  skip: 0,
  limit: 100,
  achievement_type: '',
  owner: ''
})

const form = reactive({
  id: null,
  achievement_type: '',
  title: '',
  owner: '',
  members: '',
  completion_date: '',
  certificate_no: '',
  description: ''
})

const rules = {
  achievement_type: [{ required: true, message: '请选择成果类型', trigger: 'change' }],
  title: [{ required: true, message: '请输入成果名称', trigger: 'blur' }],
  owner: [{ required: true, message: '请输入所有人', trigger: 'blur' }]
}

// 获取类型标签颜色
const getTypeTag = (type) => {
  const tags = {
    PATENT: 'success',
    AWARD: 'warning',
    BOOK: 'primary',
    SOFTWARE: 'info'
  }
  return tags[type] || 'info'  // 默认返回 'info' 而不是空字符串
}

// 获取类型标签文本
const getTypeLabel = (type) => {
  const labels = {
    PATENT: '专利',
    AWARD: '奖项',
    BOOK: '著作',
    SOFTWARE: '软件著作权'
  }
  return labels[type] || type
}

// 加载成果列表
const loadAchievements = async () => {
  loading.value = true
  try {
    const params = { ...queryParams }
    if (!params.achievement_type) delete params.achievement_type
    if (!params.owner) delete params.owner
    
    const res = await request.get('/achievements/', { params })
    // 确保返回的是数组
    if (Array.isArray(res)) {
      achievements.value = res
    } else {
      console.error('成果数据格式错误:', res)
      achievements.value = []
      ElMessage.error('成果数据格式错误')
    }
  } catch (error) {
    ElMessage.error('加载成果列表失败')
    console.error(error)
    achievements.value = []
  } finally {
    loading.value = false
  }
}

// 重置查询
const resetQuery = () => {
  queryParams.achievement_type = ''
  queryParams.owner = ''
  loadAchievements()
}

// 新增
const handleAdd = () => {
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  Object.assign(form, row)
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这个成果吗？', '提示', {
      type: 'warning'
    })
    await request.delete(`/achievements/${row.id}`)
    ElMessage.success('删除成功')
    loadAchievements()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    
    if (form.id) {
      await request.put(`/achievements/${form.id}`, form)
      ElMessage.success('更新成功')
    } else {
      await request.post('/achievements/', form)
      ElMessage.success('新增成功')
    }
    
    dialogVisible.value = false
    resetForm()
    loadAchievements()
  } catch (error) {
    if (error !== false) {
      ElMessage.error(form.id ? '更新失败' : '新增失败')
    }
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    id: null,
    achievement_type: '',
    title: '',
    owner: '',
    members: '',
    completion_date: '',
    certificate_no: '',
    description: ''
  })
  formRef.value?.resetFields()
}

onMounted(() => {
  loadAchievements()
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
