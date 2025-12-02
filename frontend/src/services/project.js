import request from './request'

// 获取项目列表
export const getProjectList = (params) => {
  return request({
    url: '/projects/',
    method: 'get',
    params
  })
}

// 获取我的项目
export const getMyProjects = (params) => {
  return request({
    url: '/projects/my',
    method: 'get',
    params
  })
}

// 获取项目详情
export const getProjectDetail = (id) => {
  return request({
    url: `/projects/${id}`,
    method: 'get'
  })
}

// 创建项目
export const createProject = (data) => {
  return request({
    url: '/projects/',
    method: 'post',
    data
  })
}

// 更新项目
export const updateProject = (id, data) => {
  return request({
    url: `/projects/${id}`,
    method: 'put',
    data
  })
}

// 删除项目
export const deleteProject = (id) => {
  return request({
    url: `/projects/${id}`,
    method: 'delete'
  })
}

// 导出项目
export const exportProjects = () => {
  return request({
    url: '/projects/export',
    method: 'get',
    responseType: 'blob'
  })
}
