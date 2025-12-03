<template>
  <div class="paper-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>论文管理</span>
          <div>
            <el-button @click="handleExport">导出Excel</el-button>
            <el-button type="primary" @click="handleAdd">新建论文</el-button>
          </div>
        </div>
      </template>

      <el-table :data="papers" border stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="title" label="论文标题" min-width="250" show-overflow-tooltip />
        <el-table-column prop="authors" label="作者" width="150" show-overflow-tooltip />
        <el-table-column prop="journal" label="期刊" width="200" show-overflow-tooltip />
        <el-table-column prop="jcr_zone" label="JCR分区" width="100" />
        <el-table-column prop="cas_zone" label="中科院分区" width="120" />
        <el-table-column prop="publication_date" label="发表日期" width="120" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.size"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadPapers"
        @current-change="loadPapers"
        style="margin-top: 20px"
      />
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
      <el-form :model="form" label-width="120px">
        <el-form-item label="论文标题" required>
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="作者" required>
          <el-input v-model="form.authors" />
        </el-form-item>
        <el-form-item label="期刊名称">
          <el-input v-model="form.journal" />
        </el-form-item>
        <el-form-item label="发表日期">
          <el-date-picker v-model="form.publication_date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="JCR分区">
          <el-input v-model="form.jcr_zone" placeholder="如: Q1" />
        </el-form-item>
        <el-form-item label="中科院分区">
          <el-input v-model="form.cas_zone" placeholder="如: 一区" />
        </el-form-item>
        <el-form-item label="影响因子">
          <el-input-number v-model="form.impact_factor" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="DOI">
          <el-input v-model="form.doi" />
        </el-form-item>
        <el-form-item label="录入人ID" required>
          <el-input-number v-model="form.creator_id" :min="1" />
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
import { getPaperList, createPaper, updatePaper, deletePaper } from '@/services/paper'
import { exportToExcel, formatDate } from '@/utils/export'

const papers = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('新建论文')
const pagination = reactive({ page: 1, size: 20, total: 0 })
const form = reactive({
  id: null,
  title: '',
  authors: '',
  journal: '',
  publication_date: '',
  doi: '',
  jcr_zone: '',
  cas_zone: '',
  impact_factor: 0,
  creator_id: 1
})

const loadPapers = async () => {
  try {
    const res = await getPaperList({ skip: (pagination.page - 1) * pagination.size, limit: pagination.size })
    // 处理响应数据
    if (Array.isArray(res)) {
      papers.value = res
      // 从响应头中获取总数
      pagination.total = parseInt(res.headers?.['x-total-count'] || 0)
    } else {
      papers.value = []
      pagination.total = 0
    }
  } catch (error) {
    ElMessage.error('加载论文列表失败')
  }
}

const handleAdd = () => {
  Object.assign(form, { id: null, title: '', authors: '', journal: '', publication_date: '', doi: '', jcr_zone: '', cas_zone: '', impact_factor: 0, creator_id: 1 })
  dialogTitle.value = '新建论文'
  dialogVisible.value = true
}

const handleEdit = (row) => {
  Object.assign(form, row)
  dialogTitle.value = '编辑论文'
  dialogVisible.value = true
}

const handleSave = async () => {
  try {
    if (form.id) {
      await updatePaper(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createPaper(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadPapers()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定删除该论文吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await deletePaper(row.id)
      ElMessage.success('删除成功')
      loadPapers()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

// 导出功能
const handleExport = () => {
  if (papers.value.length === 0) {
    ElMessage.warning('没有可导出的数据')
    return
  }
  
  const columns = [
    { label: 'ID', prop: 'id', width: 10 },
    { label: '论文标题', prop: 'title', width: 40 },
    { label: '作者', prop: 'authors', width: 20 },
    { label: '期刊名称', prop: 'journal', width: 30 },
    { 
      label: '发表日期', 
      prop: 'publication_date', 
      width: 15,
      formatter: (value) => formatDate(value)
    },
    { label: 'DOI', prop: 'doi', width: 25 },
    { label: 'JCR分区', prop: 'jcr_zone', width: 12 },
    { label: '中科院分区', prop: 'cas_zone', width: 15 },
    { label: '影响因子', prop: 'impact_factor', width: 12 }
  ]
  
  const success = exportToExcel(papers.value, columns, '论文管理数据')
  if (success) {
    ElMessage.success('导出成功！')
  } else {
    ElMessage.error('导出失败，请重试')
  }
}

onMounted(() => {
  loadPapers()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
