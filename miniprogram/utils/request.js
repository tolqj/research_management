// utils/request.js
const app = getApp()

/**
 * 封装wx.request
 */
function request(options) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${app.globalData.baseURL}${options.url}`,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        'Authorization': app.globalData.token ? `Bearer ${app.globalData.token}` : '',
        ...options.header
      },
      success(res) {
        if (res.statusCode === 200) {
          // 返回数据，并附加headers信息
          const result = res.data
          // 如果是数组，添加headers属性
          if (Array.isArray(result)) {
            result.headers = res.header
          }
          resolve(result)
        } else if (res.statusCode === 401) {
          // 未授权，跳转到登录页
          wx.showToast({
            title: '登录已过期',
            icon: 'none'
          })
          setTimeout(() => {
            app.logout()
          }, 1500)
          reject(res)
        } else {
          wx.showToast({
            title: res.data.detail || '请求失败',
            icon: 'none'
          })
          reject(res)
        }
      },
      fail(err) {
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

// GET请求
function get(url, data = {}) {
  return request({
    url,
    method: 'GET',
    data
  })
}

// POST请求
function post(url, data = {}) {
  return request({
    url,
    method: 'POST',
    data
  })
}

// PUT请求
function put(url, data = {}) {
  return request({
    url,
    method: 'PUT',
    data
  })
}

// DELETE请求
function del(url, data = {}) {
  return request({
    url,
    method: 'DELETE',
    data
  })
}

module.exports = {
  request,
  get,
  post,
  put,
  delete: del
}
