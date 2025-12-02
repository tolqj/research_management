// pages/statistics/index.js
const request = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    overview: {},
    loading: false
  },

  onLoad() {
    this.loadStatistics()
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadStatistics(() => {
      wx.stopPullDownRefresh()
    })
  },

  // 加载统计数据
  loadStatistics(callback) {
    this.setData({ loading: true })

    request.get('/statistics/overview').then(res => {
      this.setData({
        overview: res || {},
        loading: false
      })
      if (callback) callback()
    }).catch(err => {
      console.error('加载统计数据失败:', err)
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
      this.setData({ loading: false })
      if (callback) callback()
    })
  },

  // 格式化金额
  formatMoney: util.formatMoney
})