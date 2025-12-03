<template>
  <div class="project-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>项目管理</span>
          <el-button type="primary" @click="handleAdd">新建项目</el-button>
        </div>
      </template>

      <!-- 搜索表单 -->
      <el-form :model="searchForm" inline>
        <el-form-item label="项目状态">
          <el-select v-model="searchForm.status" clearable placeholder="全部">
            <el-option label="草稿" value="草稿" />
            <el-option label="已申报" value="已申报" />
            <el-option label="执行中" value="执行中" />
            <el-option label="已结题" value="已结题" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadProjects">查询</el-button>
          <el-button @click="handleExport">导出Excel</el-button>
        </el-form-item>
      </el-form>

      <!-- 项目列表 -->
      <el-table :data="projects" border stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="project_name" label="项目名称" min-width="200" />
        <el-table-column prop="pi_name" label="负责人" width="100" />
        <el-table-column prop="project_type" label="项目类型" width="150" />
        <el-table-column prop="budget_total" label="总预算(元)" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag>{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="handleView(row)">查看</el-button>
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.size"
        :total="pagination.total"
        layout="total, prev, pager, next"
        @current-change="loadProjects"
        style="margin-top: 20px"
      />
    </el-card>

    <!-- 项目表单对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
      <el-form :model="form" label-width="120px">
        <el-form-item label="项目名称" required>
          <el-input v-model="form.project_name" />
        </el-form-item>
        <el-form-item label="负责人ID" required>
          <el-input-number v-model="form.pi_id" :min="1" />
        </el-form-item>
        <el-form-item label="负责人姓名" required>
          <el-input v-model="form.pi_name" />
        </el-form-item>
        <el-form-item label="项目类型">
          <el-input v-model="form.project_type" />
        </el-form-item>
        <el-form-item label="总预算(元)">
          <el-input-number v-model="form.budget_total" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker v-model="form.start_date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="form.end_date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="项目状态">
          <el-select v-model="form.status">
            <el-option label="草稿" value="草稿" />
            <el-option label="已申报" value="已申报" />
            <el-option label="执行中" value="执行中" />
            <el-option label="已结题" value="已结题" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getProjectList, createProject, updateProject, deleteProject } from '@/services/project'
import { exportToExcel, formatDate, formatAmount } from '@/utils/export'

const projects = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('新建项目')
const searchForm = reactive({ status: '' })
const pagination = reactive({ page: 1, size: 20, total: 0 })
const form = reactive({
  id: null,
  project_name: '',
  pi_id: 1,
  pi_name: '',
  project_type: '',
  budget_total: 0,
  start_date: '',
  end_date: '',
  status: '草稿'
})

const loadProjects = async () => {
  try {
    const res = await getProjectList({ skip: (pagination.page - 1) * pagination.size, limit: pagination.size, status: searchForm.status })
    projects.value = res
  } catch (error) {
    ElMessage.error('加载项目列表失败')
  }
}

const handleAdd = () => {
  Object.assign(form, { id: null, project_name: '', pi_id: 1, pi_name: '', project_type: '', budget_total: 0, start_date: '', end_date: '', status: '草稿' })
  dialogTitle.value = '新建项目'
  dialogVisible.value = true
}

const handleEdit = (row) => {
  Object.assign(form, row)
  dialogTitle.value = '编辑项目'
  dialogVisible.value = true
}

const handleView = (row) => {
  ElMessage.info(`查看项目：${row.project_name}`)
}

const handleSave = async () => {
  try {
    if (form.id) {
      await updateProject(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createProject(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadProjects()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定删除该项目吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await deleteProject(row.id)
      ElMessage.success('删除成功')
      loadProjects()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const handleExport = () => {
  if (projects.value.length === 0) {
    ElMessage.warning('没有可导出的数据')
    return
  }
  
  const columns = [
    { label: 'ID', prop: 'id', width: 10 },
    { label: '项目名称', prop: 'project_name', width: 30 },
    { label: '负责人', prop: 'pi_name', width: 15 },
    { label: '项目类型', prop: 'project_type', width: 20 },
    { label: '项目来源', prop: 'source', width: 20 },
    { 
      label: '总预算', 
      prop: 'budget_total', 
      width: 15,
      formatter: (value) => formatAmount(value)
    },
    { 
      label: '开始日期', 
      prop: 'start_date', 
      width: 15,
      formatter: (value) => formatDate(value)
    },
    { 
      label: '结束日期', 
      prop: 'end_date', 
      width: 15,
      formatter: (value) => formatDate(value)
    },
    { label: '项目状态', prop: 'status', width: 12 },
    { label: '项目目标', prop: 'objectives', width: 35 },
    { label: '项目描述', prop: 'description', width: 35 }
  ]
  
  const success = exportToExcel(projects.value, columns, '项目管理数据')
  if (success) {
    ElMessage.success('导出成功！')
  } else {
    ElMessage.error('导出失败，请重试')
  }
}

onMounted(() => {
  loadProjects()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
