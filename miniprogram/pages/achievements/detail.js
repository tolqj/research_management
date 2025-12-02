// pages/achievements/detail.js
const request = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    achievement: {},
    loading: false
  },

  onLoad(options) {
    const id = options.id
    if (id) {
      this.setData({ achievementId: id })
      this.loadAchievementDetail(id)
    } else {
      wx.showToast({
        title: '成果ID为空',
        icon: 'none'
      })
      setTimeout(() => {
        wx.navigateBack()
      }, 1500)
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadAchievementDetail(this.data.achievementId, () => {
      wx.stopPullDownRefresh()
    })
  },

  // 加载成果详情
  loadAchievementDetail(id, callback) {
    this.setData({ loading: true })

    request.get(`/achievements/${id}`).then(res => {
      this.setData({
        achievement: res || {},
        loading: false
      })
      if (callback) callback()
    }).catch(err => {
      console.error('加载成果详情失败:', err)
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
      this.setData({ loading: false })
      if (callback) callback()
    })
  },

  // 格式化日期
  formatDate: util.formatDate
})
