<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>经费管理</span>
        <el-button type="primary" @click="dialogVisible = true">新增经费</el-button>
      </div>
    </template>

    <!-- 筛选条件 -->
    <el-form :inline="true" :model="queryParams" class="search-form">
      <el-form-item label="项目">
        <el-select v-model="queryParams.project_id" placeholder="请选择项目" clearable style="width: 200px">
          <el-option
            v-for="project in projects"
            :key="project.id"
            :label="project.project_name"
            :value="project.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="支出类型">
        <el-input v-model="queryParams.expense_type" placeholder="支出类型" clearable style="width: 150px" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadFunds">查询</el-button>
        <el-button @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 经费列表 -->
    <el-table :data="funds" border style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="project_id" label="项目" width="300">
        <template #default="{ row }">
          {{ getProjectName(row.project_id) }}
        </template>
      </el-table-column>
      <el-table-column prop="expense_type" label="支出类型" width="150" />
      <el-table-column prop="amount" label="金额（元）" width="120" align="right">
        <template #default="{ row }">
          ¥{{ row.amount.toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column prop="expense_date" label="支出日期" width="120" />
      <el-table-column prop="handler" label="经办人" width="100" />
      <el-table-column prop="notes" label="备注" show-overflow-tooltip />
      <el-table-column prop="created_at" label="创建时间" width="180" />
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
      :title="form.id ? '编辑经费' : '新增经费'"
      width="600px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="项目" prop="project_id">
          <el-select v-model="form.project_id" placeholder="请选择项目" style="width: 100%">
            <el-option
              v-for="project in projects"
              :key="project.id"
              :label="project.project_name"
              :value="project.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="支出类型" prop="expense_type">
          <el-select v-model="form.expense_type" placeholder="请选择支出类型" style="width: 100%">
            <el-option key="equipment" label="设备费" value="设备费" />
            <el-option key="material" label="材料费" value="材料费" />
            <el-option key="travel" label="差旅费" value="差旅费" />
            <el-option key="conference" label="会议费" value="会议费" />
            <el-option key="labor" label="劳务费" value="劳务费" />
            <el-option key="testing" label="测试化验加工费" value="测试化验加工费" />
            <el-option key="other" label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="金额" prop="amount">
          <el-input-number v-model="form.amount" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="支出日期" prop="expense_date">
          <el-date-picker
            v-model="form.expense_date"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="经办人" prop="handler">
          <el-input v-model="form.handler" placeholder="请输入经办人" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.notes" type="textarea" :rows="3" placeholder="请输入备注" />
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
const funds = ref([])
const projects = ref([])
const dialogVisible = ref(false)
const formRef = ref(null)

const queryParams = reactive({
  skip: 0,
  limit: 100,
  project_id: null,
  expense_type: ''
})

const form = reactive({
  id: null,
  project_id: null,
  expense_type: '',
  amount: 0,
  expense_date: '',
  handler: '',
  notes: ''
})

const rules = {
  project_id: [{ required: true, message: '请选择项目', trigger: 'change' }],
  expense_type: [{ required: true, message: '请选择支出类型', trigger: 'change' }],
  amount: [{ required: true, message: '请输入金额', trigger: 'blur' }],
  expense_date: [{ required: true, message: '请选择支出日期', trigger: 'change' }]
}

// 加载项目列表
const loadProjects = async () => {
  try {
    // 不传递 status 参数，获取所有项目
    const res = await request.get('/projects/', { 
      params: { 
        skip: 0, 
        limit: 1000
      } 
    })
    // 确保返回的是数组
    if (Array.isArray(res)) {
      projects.value = res
      console.log(`[Fund] 成功加载 ${res.length} 个项目`)
    } else {
      console.error('项目数据格式错误:', res)
      projects.value = []
    }
  } catch (error) {
    // 加载项目失败不影响页面使用，只是不能筛选项目
    console.warn('加载项目列表失败，项目筛选功能将不可用:', error.message)
    projects.value = []
    // 不显示错误消息，避免打扰用户
  }
}

// 加载经费列表
const loadFunds = async () => {
  loading.value = true
  try {
    const params = { ...queryParams }
    if (!params.project_id) delete params.project_id
    if (!params.expense_type) delete params.expense_type
    
    const res = await request.get('/funds/', { params })
    // 确保返回的是数组
    if (Array.isArray(res)) {
      funds.value = res
    } else {
      console.error('经费数据格式错误:', res)
      funds.value = []
      ElMessage.error('经费数据格式错误')
    }
  } catch (error) {
    ElMessage.error('加载经费列表失败')
    console.error(error)
    funds.value = []
  } finally {
    loading.value = false
  }
}

// 获取项目名称
const getProjectName = (projectId) => {
  const project = projects.value.find(p => p.id === projectId)
  return project ? project.project_name : '未知项目'
}

// 重置查询
const resetQuery = () => {
  queryParams.project_id = null
  queryParams.expense_type = ''
  loadFunds()
}

// 编辑
const handleEdit = (row) => {
  Object.assign(form, row)
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这条经费记录吗？', '提示', {
      type: 'warning'
    })
    await request.delete(`/funds/${row.id}`)
    ElMessage.success('删除成功')
    loadFunds()
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
      await request.put(`/funds/${form.id}`, form)
      ElMessage.success('更新成功')
    } else {
      await request.post('/funds/', form)
      ElMessage.success('新增成功')
    }
    
    dialogVisible.value = false
    resetForm()
    loadFunds()
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
    project_id: null,
    expense_type: '',
    amount: 0,
    expense_date: '',
    handler: '',
    notes: ''
  })
  formRef.value?.resetFields()
}

onMounted(() => {
  loadProjects()
  loadFunds()
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
