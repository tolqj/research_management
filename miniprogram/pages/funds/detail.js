// pages/funds/detail.js
const request = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    fund: {},
    loading: false
  },

  onLoad(options) {
    const id = options.id
    if (id) {
      this.setData({ fundId: id })
      this.loadFundDetail(id)
    } else {
      wx.showToast({
        title: '经费ID为空',
        icon: 'none'
      })
      setTimeout(() => {
        wx.navigateBack()
      }, 1500)
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadFundDetail(this.data.fundId, () => {
      wx.stopPullDownRefresh()
    })
  },

  // 加载经费详情
  loadFundDetail(id, callback) {
    this.setData({ loading: true })

    request.get(`/funds/${id}`).then(res => {
      this.setData({
        fund: res || {},
        loading: false
      })
      if (callback) callback()
    }).catch(err => {
      console.error('加载经费详情失败:', err)
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
      this.setData({ loading: false })
      if (callback) callback()
    })
  },

  // 格式化金额
  formatMoney: util.formatMoney,

  // 格式化日期
  formatDate: util.formatDate
})
