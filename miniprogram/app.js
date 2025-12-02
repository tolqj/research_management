// app.js
App({
  globalData: {
    userInfo: null,
    token: null,
    // 开发环境：localhost（需在微信开发者工具中关闭域名校验）
    baseURL: 'http://localhost:8000/api'
    // 真机调试：改为电脑的局域网IP（用ipconfig查看）
    // baseURL: 'http://192.168.1.100:8000/api'
  },

  onLaunch() {
    // 检查登录状态
    const token = wx.getStorageSync('token')
    if (token) {
      this.globalData.token = token
      this.getUserInfo()
    }
  },

  // 获取用户信息
  getUserInfo() {
    const that = this
    wx.request({
      url: `${this.globalData.baseURL}/users/me`,
      method: 'GET',
      header: {
        'Authorization': `Bearer ${this.globalData.token}`
      },
      success(res) {
        if (res.statusCode === 200) {
          that.globalData.userInfo = res.data
        }
      }
    })
  },

  // 登录
  login(username, password, callback) {
    const that = this
    wx.request({
      url: `${this.globalData.baseURL}/auth/login`,
      method: 'POST',
      data: {
        username: username,
        password: password
      },
      success(res) {
        if (res.statusCode === 200) {
          const token = res.data.access_token
          that.globalData.token = token
          wx.setStorageSync('token', token)
          that.getUserInfo()
          callback(true, '登录成功')
        } else {
          callback(false, res.data.detail || '登录失败')
        }
      },
      fail() {
        callback(false, '网络错误')
      }
    })
  },

  // 登出
  logout() {
    this.globalData.token = null
    this.globalData.userInfo = null
    wx.removeStorageSync('token')
    wx.reLaunch({
      url: '/pages/login/login'
    })
  },

  // 检查登录状态
  checkLogin() {
    if (!this.globalData.token) {
      wx.showModal({
        title: '提示',
        content: '请先登录',
        showCancel: false,
        success() {
          wx.redirectTo({
            url: '/pages/login/login'
          })
        }
      })
      return false
    }
    return true
  }
})
