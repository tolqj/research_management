import request from './request'

// 获取当前用户信息
export const getCurrentUser = () => {
  return request({
    url: '/users/me',
    method: 'get'
  })
}

// 更新当前用户信息
export const updateCurrentUser = (data) => {
  return request({
    url: '/users/me',
    method: 'put',
    data
  })
}

// 修改密码
export const changePassword = (data) => {
  return request({
    url: '/users/me/change-password',
    method: 'post',
    data
  })
}

// 获取用户列表（管理员）
export const getUserList = (params) => {
  return request({
    url: '/users/',
    method: 'get',
    params
  })
}

// 创建用户（管理员）
export const createUser = (data) => {
  return request({
    url: '/users/',
    method: 'post',
    data
  })
}

// 更新用户（管理员）
export const updateUser = (id, data) => {
  return request({
    url: `/users/${id}`,
    method: 'put',
    data
  })
}

// 删除用户（管理员）
export const deleteUser = (id) => {
  return request({
    url: `/users/${id}`,
    method: 'delete'
  })
}
