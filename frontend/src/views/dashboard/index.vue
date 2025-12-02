<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <!-- 统计卡片 -->
      <el-col :span="6" v-for="item in statsCards" :key="item.title">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon" :style="{ backgroundColor: item.color }">
              <el-icon :size="32"><component :is="item.icon" /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-title">{{ item.title }}</div>
              <div class="stats-value">{{ item.value }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <!-- 项目状态分布 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>项目状态分布</span>
          </template>
          <div ref="projectChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>

      <!-- 论文年份统计 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>论文年份统计</span>
          </template>
          <div ref="paperChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <!-- 经费支出统计 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>经费支出类型分布</span>
          </template>
          <div ref="fundChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>

      <!-- 成果类型统计 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>成果类型统计</span>
          </template>
          <div ref="achievementChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getDashboardData } from '@/services/statistics'

const statsCards = ref([
  { title: '项目总数', value: 0, icon: 'Management', color: '#409EFF' },
  { title: '论文总数', value: 0, icon: 'Document', color: '#67C23A' },
  { title: '成果总数', value: 0, icon: 'TrophyBase', color: '#E6A23C' },
  { title: '经费总额', value: '¥0', icon: 'Money', color: '#F56C6C' }
])

const projectChartRef = ref(null)
const paperChartRef = ref(null)
const fundChartRef = ref(null)
const achievementChartRef = ref(null)

// 加载仪表盘数据
const loadDashboardData = async () => {
  try {
    const data = await getDashboardData()
    
    // 更新统计卡片
    statsCards.value[0].value = data.overview.project_count
    statsCards.value[1].value = data.overview.paper_count
    statsCards.value[2].value = data.overview.achievement_count
    statsCards.value[3].value = `¥${data.overview.total_expense.toFixed(2)}`
    
    // 渲染图表
    await nextTick()
    renderProjectChart(data.projects.by_status)
    renderPaperChart(data.papers.by_year)
    renderFundChart(data.funds.by_type)
    renderAchievementChart(data.achievements.by_type)
  } catch (error) {
    console.error('加载仪表盘数据失败:', error)
  }
}

// 项目状态图表
const renderProjectChart = (data) => {
  const chart = echarts.init(projectChartRef.value)
  const option = {
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: '60%',
      data: Object.entries(data).map(([name, value]) => ({ name, value })),
      emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
    }]
  }
  chart.setOption(option)
}

// 论文年份图表
const renderPaperChart = (data) => {
  const chart = echarts.init(paperChartRef.value)
  const years = Object.keys(data).sort()
  const values = years.map(year => data[year])
  
  const option = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: years },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: values, itemStyle: { color: '#409EFF' } }]
  }
  chart.setOption(option)
}

// 经费图表
const renderFundChart = (data) => {
  const chart = echarts.init(fundChartRef.value)
  const option = {
    tooltip: { trigger: 'item', formatter: '{b}: ¥{c}' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: Object.entries(data).map(([name, value]) => ({ name, value }))
    }]
  }
  chart.setOption(option)
}

// 成果图表
const renderAchievementChart = (data) => {
  const chart = echarts.init(achievementChartRef.value)
  const option = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: Object.keys(data) },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: Object.values(data), itemStyle: { color: '#67C23A' } }]
  }
  chart.setOption(option)
}

onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stats-card {
  margin-bottom: 20px;
}

.stats-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stats-info {
  flex: 1;
}

.stats-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stats-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}
</style>
