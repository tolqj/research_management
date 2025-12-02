// pages/login/login.js
const app = getApp()

Page({
  data: {
    username: '',
    password: '',
    loading: false
  },

  // 输入用户名
  onUsernameInput(e) {
    this.setData({
      username: e.detail.value
    })
  },

  // 输入密码
  onPasswordInput(e) {
    this.setData({
      password: e.detail.value
    })
  },

  // 登录
  handleLogin() {
    const { username, password } = this.data

    // 表单验证
    if (!username) {
      wx.showToast({
        title: '请输入用户名',
        icon: 'none'
      })
      return
    }

    if (!password) {
      wx.showToast({
        title: '请输入密码',
        icon: 'none'
      })
      return
    }

    // 显示加载状态
    this.setData({ loading: true })

    // 调用登录接口
    app.login(username, password, (success, message) => {
      this.setData({ loading: false })

      if (success) {
        wx.showToast({
          title: message,
          icon: 'success'
        })
        
        // 跳转到首页
        setTimeout(() => {
          wx.redirectTo({
            url: '/pages/index/index'
          })
        }, 1500)
      } else {
        wx.showToast({
          title: message,
          icon: 'none'
        })
      }
    })
  },

  // 快速登录（测试用）
  quickLogin(e) {
    const role = e.currentTarget.dataset.role
    let username, password

    switch (role) {
      case 'admin':
        username = 'admin'
        password = 'Admin@123'
        break
      case 'secretary':
        username = 'secretary'
        password = 'Sec@2024'
        break
      case 'teacher':
        username = 'teacher'
        password = 'Teacher@123'
        break
    }

    this.setData({ username, password })
  }
})
