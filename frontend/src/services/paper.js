import request from './request'

// 获取论文列表
export const getPaperList = (params) => {
  return request({
    url: '/papers/',
    method: 'get',
    params
  })
}

// 搜索论文
export const searchPapers = (params) => {
  return request({
    url: '/papers/search',
    method: 'get',
    params
  })
}

// 获取论文详情
export const getPaperDetail = (id) => {
  return request({
    url: `/papers/${id}`,
    method: 'get'
  })
}

// 创建论文
export const createPaper = (data) => {
  return request({
    url: '/papers/',
    method: 'post',
    data
  })
}

// 更新论文
export const updatePaper = (id, data) => {
  return request({
    url: `/papers/${id}`,
    method: 'put',
    data
  })
}

// 删除论文
export const deletePaper = (id) => {
  return request({
    url: `/papers/${id}`,
    method: 'delete'
  })
}

// 导出论文
export const exportPapers = () => {
  return request({
    url: '/papers/export',
    method: 'get',
    responseType: 'blob'
  })
}
