// pages/projects/list.js
const request = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    projects: [],
    loading: false,
    finished: false,
    page: 1,
    pageSize: 20,
    total: 0,
    
    // 筛选条件
    statusList: ['全部', '草稿', '已申报', '执行中', '已结题'],
    activeStatus: 0,
    keyword: ''
  },

  onLoad() {
    this.loadProjects()
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.setData({
      page: 1,
      projects: [],
      finished: false
    })
    this.loadProjects(() => {
      wx.stopPullDownRefresh()
    })
  },

  // 上拉加载更多
  onReachBottom() {
    if (!this.data.finished && !this.data.loading) {
      this.setData({
        page: this.data.page + 1
      })
      this.loadProjects()
    }
  },

  // 加载项目列表
  loadProjects(callback) {
    if (this.data.loading) return

    this.setData({ loading: true })

    const { page, pageSize, activeStatus, statusList } = this.data
    const params = {
      skip: (page - 1) * pageSize,
      limit: pageSize
    }

    // 添加状态筛选
    if (activeStatus > 0) {
      params.status = statusList[activeStatus]
    }

    request.get('/projects/', params).then(res => {
      const projects = Array.isArray(res) ? res : []
      const total = parseInt(res.headers ? res.headers['x-total-count'] : projects.length)

      this.setData({
        projects: page === 1 ? projects : this.data.projects.concat(projects),
        total: total,
        loading: false,
        finished: projects.length < pageSize
      })

      if (callback) callback()
    }).catch(err => {
      this.setData({ loading: false })
      if (callback) callback()
    })
  },

  // 切换状态筛选
  onStatusChange(e) {
    const index = e.currentTarget.dataset.index
    if (index === this.data.activeStatus) return

    this.setData({
      activeStatus: index,
      page: 1,
      projects: [],
      finished: false
    })
    this.loadProjects()
  },

  // 搜索
  onSearch(e) {
    this.setData({
      keyword: e.detail.value,
      page: 1,
      projects: [],
      finished: false
    })
    this.loadProjects()
  },

  // 跳转到详情页
  goToDetail(e) {
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
