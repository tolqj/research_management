// pages/funds/list.js
const request = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    funds: [],
    loading: false,
    finished: false,
    page: 1,
    pageSize: 20,
    total: 0
  },

  onLoad() {
    this.loadFunds()
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.setData({
      page: 1,
      funds: [],
      finished: false
    })
    this.loadFunds(() => {
      wx.stopPullDownRefresh()
    })
  },

  // 上拉加载
  onReachBottom() {
    if (!this.data.finished && !this.data.loading) {
      this.setData({
        page: this.data.page + 1
      })
      this.loadFunds()
    }
  },

  // 加载经费列表
  loadFunds(callback) {
    if (this.data.loading) return

    this.setData({ loading: true })

    const { page, pageSize } = this.data
    const params = {
      skip: (page - 1) * pageSize,
      limit: pageSize
    }

    request.get('/funds/', params).then(res => {
      const funds = Array.isArray(res) ? res : []
      const total = parseInt(res.headers ? res.headers['x-total-count'] : funds.length)

      this.setData({
        funds: page === 1 ? funds : this.data.funds.concat(funds),
        total: total,
        loading: false,
        finished: funds.length < pageSize
      })

      if (callback) callback()
    }).catch(err => {
      console.error('加载经费列表失败:', err)
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
      url: `/pages/funds/detail?id=${id}`
    })
  },

  // 格式化金额
  formatMoney: util.formatMoney,

  // 格式化日期
  formatDate: util.formatDate
})