// pages/index/index.js
const app = getApp()
const request = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    userInfo: {},
    overview: {
      project_count: 0,
      paper_count: 0,
      achievement_count: 0,
      total_expense: 0
    },
    projects: [],
    loading: false
  },

  onLoad() {
    // 检查登录状态
    if (!app.globalData.token) {
      wx.redirectTo({
        url: '/pages/login/login'
      })
      return
    }

    // 获取用户信息
    this.setData({
      userInfo: app.globalData.userInfo || {}
    })

    // 加载数据
    this.loadData()
  },

  onShow() {
    // 每次显示页面时刷新用户信息
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo
      })
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadData(() => {
      wx.stopPullDownRefresh()
    })
  },

  // 加载数据
  loadData(callback) {
    this.setData({ loading: true })

    // 并行请求多个接口
    Promise.all([
      this.loadOverview(),
      this.loadRecentProjects()
    ]).then(() => {
      this.setData({ loading: false })
      if (callback) callback()
    }).catch(err => {
      this.setData({ loading: false })
      if (callback) callback()
    })
  },

  // 加载数据总览
  loadOverview() {
    return request.get('/statistics/overview').then(res => {
      this.setData({
        overview: res || {}
      })
    }).catch(err => {
      console.error('加载数据总览失败:', err)
    })
  },

  // 加载最新项目
  loadRecentProjects() {
    return request.get('/projects/', {
      skip: 0,
      limit: 5
    }).then(res => {
      const projects = Array.isArray(res) ? res : []
      this.setData({
        projects: projects
      })
    }).catch(err => {
      console.error('加载项目列表失败:', err)
    })
  },

  // 跳转到项目列表
  goToProjects() {
    wx.navigateTo({
      url: '/pages/projects/list'
    })
  },

  // 跳转到论文列表
  goToPapers() {
    wx.navigateTo({
      url: '/pages/papers/list'
    })
  },

  // 跳转到经费列表
  goToFunds() {
    wx.navigateTo({
      url: '/pages/funds/list'
    })
  },

  // 跳转到成果列表
  goToAchievements() {
    wx.navigateTo({
      url: '/pages/achievements/list'
    })
  },

  // 跳转到项目详情
  goToProjectDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/projects/detail?id=${id}`
    })
  },

  // 格式化金额
  formatMoney: util.formatMoney,

  // 获取状态类型
  getStatusType: util.getProjectStatusType
})
