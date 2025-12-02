import request from './request'

// 获取系统概览统计
export const getOverviewStatistics = () => {
  return request({
    url: '/statistics/overview',
    method: 'get'
  })
}

// 获取项目统计
export const getProjectStatistics = () => {
  return request({
    url: '/statistics/projects',
    method: 'get'
  })
}

// 获取论文统计
export const getPaperStatistics = () => {
  return request({
    url: '/statistics/papers',
    method: 'get'
  })
}

// 获取经费统计
export const getFundStatistics = () => {
  return request({
    url: '/statistics/funds',
    method: 'get'
  })
}

// 获取成果统计
export const getAchievementStatistics = () => {
  return request({
    url: '/statistics/achievements',
    method: 'get'
  })
}

// 获取仪表盘数据
export const getDashboardData = () => {
  return request({
    url: '/statistics/dashboard',
    method: 'get'
  })
}
