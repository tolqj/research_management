import request from './request'

// 登录
export const login = (data) => {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  })
}

// 注册
export const register = (data) => {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  })
}
