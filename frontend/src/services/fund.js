import request from './request'

// 获取经费列表
export const getFundList = (params) => {
  return request({
    url: '/funds/',
    method: 'get',
    params
  })
}

// 获取项目经费汇总
export const getProjectFundSummary = (projectId) => {
  return request({
    url: `/funds/project/${projectId}/summary`,
    method: 'get'
  })
}

// 获取经费详情
export const getFundDetail = (id) => {
  return request({
    url: `/funds/${id}`,
    method: 'get'
  })
}

// 创建经费记录
export const createFund = (data) => {
  return request({
    url: '/funds/',
    method: 'post',
    data
  })
}

// 更新经费记录
export const updateFund = (id, data) => {
  return request({
    url: `/funds/${id}`,
    method: 'put',
    data
  })
}

// 删除经费记录
export const deleteFund = (id) => {
  return request({
    url: `/funds/${id}`,
    method: 'delete'
  })
}
