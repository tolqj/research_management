<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>安全审计日志</span>
        <div>
          <el-button @click="handleExport">导出Excel</el-button>
          <el-button type="primary" @click="loadStatistics" :icon="TrendCharts">查看统计</el-button>
        </div>
      </div>
    </template>

    <!-- 搜索区域 -->
    <el-form :model="searchForm" class="search-form">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
          <el-form-item label="用户名">
            <el-input 
              v-model="searchForm.username" 
              placeholder="请输入用户名" 
              clearable 
              prefix-icon="User"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
          <el-form-item label="操作类型">
            <el-input 
              v-model="searchForm.operation" 
              placeholder="如：登录、创建项目" 
              clearable 
              prefix-icon="Operation"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
          <el-form-item label="模块">
            <el-select 
              v-model="searchForm.module" 
              placeholder="请选择模块" 
              clearable 
              style="width: 100%"
            >
              <el-option label="认证" value="auth" />
              <el-option label="用户" value="user" />
              <el-option label="项目" value="project" />
              <el-option label="论文" value="paper" />
              <el-option label="经费" value="fund" />
              <el-option label="成果" value="achievement" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
          <el-form-item label="状态">
            <el-select 
              v-model="searchForm.status" 
              placeholder="请选择状态" 
              clearable 
              style="width: 100%"
            >
              <el-option label="成功" value="SUCCESS" />
              <el-option label="失败" value="FAILED" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
          <el-form-item label="日期范围">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              style="width: 100%"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
          <el-form-item label=" " class="button-group">
            <el-button type="primary" @click="handleSearch" :icon="Search">搜索</el-button>
            <el-button @click="handleReset" :icon="Refresh">重置</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <!-- 表格 -->
    <el-table
      :data="tableData"
      v-loading="loading"
      stripe
      border
      style="width: 100%"
      :height="500"
    >
      <el-table-column prop="id" label="ID" width="70" align="center" />
      <el-table-column prop="username" label="用户名" min-width="100" show-overflow-tooltip />
      <el-table-column prop="operation" label="操作类型" min-width="150" show-overflow-tooltip />
      <el-table-column prop="module" label="模块" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="getModuleType(row.module)" size="small">{{ getModuleName(row.module) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80" align="center">
        <template #default="{ row }">
          <el-tag :type="row.status === 'SUCCESS' ? 'success' : 'danger'" size="small">
            {{ row.status === 'SUCCESS' ? '成功' : '失败' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="ip_address" label="IP地址" min-width="140" show-overflow-tooltip />
      <el-table-column prop="created_at" label="操作时间" min-width="170" show-overflow-tooltip>
        <template #default="{ row }">
          {{ row.created_at }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="90" fixed="right" align="center">
        <template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            @click="handleViewDetail(row)"
            link
          >
            详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      v-model:current-page="pagination.page"
      v-model:page-size="pagination.pageSize"
      :page-sizes="[20, 50, 100, 200]"
      :total="pagination.total"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handlePageChange"
      style="margin-top: 20px; justify-content: flex-end"
    />

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="日志详情"
      width="800px"
    >
      <el-descriptions :column="2" border v-if="currentLog" size="default">
        <el-descriptions-item label="日志ID" label-width="100px">{{ currentLog.id }}</el-descriptions-item>
        <el-descriptions-item label="用户ID" label-width="100px">{{ currentLog.user_id || '-' }}</el-descriptions-item>
        <el-descriptions-item label="用户名" label-width="100px">{{ currentLog.username }}</el-descriptions-item>
        <el-descriptions-item label="操作类型" label-width="100px">{{ currentLog.operation }}</el-descriptions-item>
        <el-descriptions-item label="模块名称" label-width="100px">{{ getModuleName(currentLog.module) }}</el-descriptions-item>
        <el-descriptions-item label="操作状态" label-width="100px">
          <el-tag :type="currentLog.status === 'SUCCESS' ? 'success' : 'danger'">
            {{ currentLog.status === 'SUCCESS' ? '成功' : '失败' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="请求方法" label-width="100px">{{ currentLog.method }}</el-descriptions-item>
        <el-descriptions-item label="IP地址" label-width="100px">{{ currentLog.ip_address }}</el-descriptions-item>
        <el-descriptions-item label="执行时间" label-width="100px">{{ currentLog.duration }}ms</el-descriptions-item>
        <el-descriptions-item label="操作时间" label-width="100px">{{ currentLog.created_at }}</el-descriptions-item>
        <el-descriptions-item label="请求路径" label-width="100px" :span="2">{{ currentLog.path }}</el-descriptions-item>
        <el-descriptions-item label="用户代理" label-width="100px" :span="2" v-if="currentLog.user_agent">
          <div style="word-break: break-all; font-size: 12px">{{ currentLog.user_agent }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="操作详情" label-width="100px" :span="2" v-if="currentLog.details">
          <pre style="max-height: 300px; overflow: auto; background: #f5f7fa; padding: 10px; border-radius: 4px; font-size: 12px">{{ formatJSON(currentLog.details) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="错误信息" label-width="100px" :span="2" v-if="currentLog.error_msg">
          <div style="color: #f56c6c">{{ currentLog.error_msg }}</div>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 统计对话框 -->
    <el-dialog
      v-model="statsVisible"
      title="审计日志统计"
      width="900px"
    >
      <el-form :inline="true" style="margin-bottom: 20px">
        <el-form-item label="统计范围">
          <el-select v-model="statsDays" @change="loadStatistics" style="width: 120px">
            <el-option label="最近7天" :value="7" />
            <el-option label="最近30天" :value="30" />
            <el-option label="最近90天" :value="90" />
          </el-select>
        </el-form-item>
      </el-form>

      <el-row :gutter="20" v-if="statistics">
        <el-col :span="12">
          <el-card shadow="hover">
            <template #header>操作类型TOP10</template>
            <el-table :data="statistics.operation_stats" size="small" :show-header="false">
              <el-table-column prop="operation" label="操作" />
              <el-table-column prop="count" label="次数" width="80" align="right">
                <template #default="{ row }">
                  <el-tag>{{ row.count }}</el-tag>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="hover">
            <template #header>活跃用户TOP10</template>
            <el-table :data="statistics.user_stats" size="small" :show-header="false">
              <el-table-column prop="username" label="用户" />
              <el-table-column prop="count" label="次数" width="80" align="right">
                <template #default="{ row }">
                  <el-tag type="success">{{ row.count }}</el-tag>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
        <el-col :span="24" style="margin-top: 20px">
          <el-card shadow="hover">
            <template #header>操作结果统计</template>
            <el-row :gutter="20">
              <el-col :span="12" v-for="item in statistics.status_stats" :key="item.status">
                <el-statistic :title="item.status === 'SUCCESS' ? '成功操作' : '失败操作'" :value="item.count">
                  <template #suffix>次</template>
                </el-statistic>
              </el-col>
            </el-row>
          </el-card>
        </el-col>
      </el-row>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Refresh, View, TrendCharts } from '@element-plus/icons-vue'
import { getAuditLogs, getAuditStatistics } from '@/services/audit'
import { exportToExcel, formatDateTime } from '@/utils/export'

const loading = ref(false)
const detailVisible = ref(false)
const statsVisible = ref(false)
const currentLog = ref(null)
const statistics = ref(null)
const statsDays = ref(7)
const dateRange = ref([])

const searchForm = reactive({
  username: '',
  operation: '',
  module: '',
  status: ''
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const tableData = ref([])

// 获取审计日志列表
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm
    }

    // 处理日期范围
    if (dateRange.value && dateRange.value.length === 2) {
      params.start_date = formatDateStr(dateRange.value[0])
      params.end_date = formatDateStr(dateRange.value[1])
    }

    const response = await getAuditLogs(params)
    tableData.value = response.data
    pagination.total = response.total
  } catch (error) {
    ElMessage.error('获取审计日志失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 格式化日期为 YYYY-MM-DD
const formatDateStr = (date) => {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

// 重置
const handleReset = () => {
  searchForm.username = ''
  searchForm.operation = ''
  searchForm.module = ''
  searchForm.status = ''
  dateRange.value = []
  pagination.page = 1
  fetchData()
}

// 分页
const handleSizeChange = () => {
  fetchData()
}

const handlePageChange = () => {
  fetchData()
}

// 查看详情
const handleViewDetail = (row) => {
  currentLog.value = row
  detailVisible.value = true
}

// 加载统计数据
const loadStatistics = async () => {
  try {
    const response = await getAuditStatistics(statsDays.value)
    statistics.value = response
    statsVisible.value = true
  } catch (error) {
    ElMessage.error('获取统计数据失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 格式化JSON
const formatJSON = (jsonStr) => {
  try {
    const obj = typeof jsonStr === 'string' ? JSON.parse(jsonStr) : jsonStr
    return JSON.stringify(obj, null, 2)
  } catch {
    return jsonStr
  }
}

// 获取模块名称
const getModuleName = (module) => {
  const moduleMap = {
    'auth': '认证',
    'user': '用户',
    'project': '项目',
    'paper': '论文',
    'fund': '经费',
    'achievement': '成果'
  }
  return moduleMap[module] || module
}

// 获取模块标签类型
const getModuleType = (module) => {
  const typeMap = {
    'auth': 'warning',
    'user': 'danger',
    'project': 'primary',
    'paper': 'success',
    'fund': 'info',
    'achievement': ''
  }
  return typeMap[module] || ''
}

// 导出功能
const handleExport = () => {
  if (tableData.value.length === 0) {
    ElMessage.warning('没有可导出的数据')
    return
  }
  
  const columns = [
    { label: 'ID', prop: 'id', width: 10 },
    { label: '用户名', prop: 'username', width: 15 },
    { label: '操作类型', prop: 'operation', width: 20 },
    { 
      label: '模块', 
      prop: 'module', 
      width: 12,
      formatter: (value) => getModuleName(value)
    },
    { label: '请求方法', prop: 'method', width: 12 },
    { label: '请求路径', prop: 'path', width: 30 },
    { 
      label: '操作状态', 
      prop: 'status', 
      width: 12,
      formatter: (value) => value === 'SUCCESS' ? '成功' : '失败'
    },
    { label: 'IP地址', prop: 'ip_address', width: 18 },
    { label: '执行时间(ms)', prop: 'duration', width: 15 },
    { 
      label: '操作时间', 
      prop: 'created_at', 
      width: 20,
      formatter: (value) => formatDateTime(value)
    },
    { label: '错误信息', prop: 'error_msg', width: 30 }
  ]
  
  const success = exportToExcel(tableData.value, columns, '审计日志数据')
  if (success) {
    ElMessage.success('导出成功！')
  } else {
    ElMessage.error('导出失败，请重试')
  }
}

onMounted(() => {
  fetchData()
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
  padding: 24px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.search-form :deep(.el-form-item) {
  margin-bottom: 18px;
}

.search-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
  line-height: 32px;
}

.search-form :deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
  transition: all 0.2s;
}

.search-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #c0c4cc inset;
}

.search-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #409eff inset;
}

.search-form .button-group {
  text-align: left;
}

.search-form .button-group :deep(.el-form-item__content) {
  justify-content: flex-start;
}

.search-form .el-button {
  padding: 8px 20px;
  font-weight: 500;
}

.el-table {
  font-size: 13px;
}

:deep(.el-table__body-wrapper) {
  font-size: 13px;
}

pre {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.5;
}

/* 响应式优化 */
@media (max-width: 768px) {
  .search-form {
    padding: 16px;
  }
  
  .search-form :deep(.el-form-item) {
    margin-bottom: 12px;
  }
}</style>
