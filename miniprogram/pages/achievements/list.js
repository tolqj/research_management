// pages/achievements/list.js
const request = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    achievements: [],
    loading: false,
    finished: false,
    page: 1,
    pageSize: 20,
    total: 0
  },

  onLoad() {
    this.loadAchievements()
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.setData({
      page: 1,
      achievements: [],
      finished: false
    })
    this.loadAchievements(() => {
      wx.stopPullDownRefresh()
    })
  },

  // 上拉加载
  onReachBottom() {
    if (!this.data.finished && !this.data.loading) {
      this.setData({
        page: this.data.page + 1
      })
      this.loadAchievements()
    }
  },

  // 加载成果列表
  loadAchievements(callback) {
    if (this.data.loading) return

    this.setData({ loading: true })

    const { page, pageSize } = this.data
    const params = {
      skip: (page - 1) * pageSize,
      limit: pageSize
    }

    request.get('/achievements/', params).then(res => {
      const achievements = Array.isArray(res) ? res : []
      const total = parseInt(res.headers ? res.headers['x-total-count'] : achievements.length)

      this.setData({
        achievements: page === 1 ? achievements : this.data.achievements.concat(achievements),
        total: total,
        loading: false,
        finished: achievements.length < pageSize
      })

      if (callback) callback()
    }).catch(err => {
      console.error('加载成果列表失败:', err)
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
      this.setData({ loading: false })
      if (callback) callback()
    })
  },

  // 跳转到详情
  goToDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/achievements/detail?id=${id}`
    })
  },

  // 格式化日期
  formatDate: util.formatDate
})