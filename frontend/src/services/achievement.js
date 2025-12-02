import request from './request'

// 获取成果列表
export const getAchievementList = (params) => {
  return request({
    url: '/achievements/',
    method: 'get',
    params
  })
}

// 获取成果详情
export const getAchievementDetail = (id) => {
  return request({
    url: `/achievements/${id}`,
    method: 'get'
  })
}

// 创建成果
export const createAchievement = (data) => {
  return request({
    url: '/achievements/',
    method: 'post',
    data
  })
}

// 更新成果
export const updateAchievement = (id, data) => {
  return request({
    url: `/achievements/${id}`,
    method: 'put',
    data
  })
}

// 删除成果
export const deleteAchievement = (id) => {
  return request({
    url: `/achievements/${id}`,
    method: 'delete'
  })
}

// 导出成果
export const exportAchievements = () => {
  return request({
    url: '/achievements/export',
    method: 'get',
    responseType: 'blob'
  })
}
