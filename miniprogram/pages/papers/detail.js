// pages/papers/detail.js
const request = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    paper: {},
    loading: false
  },

  onLoad(options) {
    const id = options.id
    if (id) {
      this.setData({ paperId: id })
      this.loadPaperDetail(id)
    } else {
      wx.showToast({
        title: '论文ID为空',
        icon: 'none'
      })
      setTimeout(() => {
        wx.navigateBack()
      }, 1500)
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadPaperDetail(this.data.paperId, () => {
      wx.stopPullDownRefresh()
    })
  },

  // 加载论文详情
  loadPaperDetail(id, callback) {
    this.setData({ loading: true })

    request.get(`/papers/${id}`).then(res => {
      this.setData({
        paper: res || {},
        loading: false
      })
      if (callback) callback()
    }).catch(err => {
      console.error('加载论文详情失败:', err)
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
