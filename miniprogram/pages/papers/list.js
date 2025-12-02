// pages/papers/list.js
const request = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    papers: [],
    loading: false,
    finished: false,
    page: 1,
    pageSize: 20,
    total: 0
  },

  onLoad() {
    this.loadPapers()
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.setData({
      page: 1,
      papers: [],
      finished: false
    })
    this.loadPapers(() => {
      wx.stopPullDownRefresh()
    })
  },

  // 上拉加载
  onReachBottom() {
    if (!this.data.finished && !this.data.loading) {
      this.setData({
        page: this.data.page + 1
      })
      this.loadPapers()
    }
  },

  // 加载论文列表
  loadPapers(callback) {
    if (this.data.loading) return

    this.setData({ loading: true })

    const { page, pageSize } = this.data
    const params = {
      skip: (page - 1) * pageSize,
      limit: pageSize
    }

    request.get('/papers/', params).then(res => {
      const papers = Array.isArray(res) ? res : []
      const total = parseInt(res.headers ? res.headers['x-total-count'] : papers.length)

      this.setData({
        papers: page === 1 ? papers : this.data.papers.concat(papers),
        total: total,
        loading: false,
        finished: papers.length < pageSize
      })

      if (callback) callback()
    }).catch(err => {
      console.error('加载论文列表失败:', err)
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
      url: `/pages/papers/detail?id=${id}`
    })
  },

  // 格式化日期
  formatDate: util.formatDate
})