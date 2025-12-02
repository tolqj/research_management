// pages/projects/detail.js
const request = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    project: {},
    loading: false,
    // Tab选项卡当前索引
    activeTab: 0,
    tabList: ['基本信息', '项目成员', '项目成果'],
    // 项目成员
    members: [],
    // 相关论文
    papers: [],
    // 相关成果
    achievements: []
  },

  onLoad(options) {
    const id = options.id
    if (id) {
      this.setData({ projectId: id })
      this.loadProjectDetail(id)
    } else {
      wx.showToast({
        title: '项目ID为空',
        icon: 'none'
      })
      setTimeout(() => {
        wx.navigateBack()
      }, 1500)
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadProjectDetail(this.data.projectId, () => {
      wx.stopPullDownRefresh()
    })
  },

  // 加载项目详情
  loadProjectDetail(id, callback) {
    this.setData({ loading: true })

    request.get(`/projects/${id}`).then(res => {
      // 如果没有budget_used字段，设置为0
      if (!res.budget_used && res.budget_used !== 0) {
        res.budget_used = 0
      }
      
      this.setData({
        project: res || {},
        loading: false
      })
      // 加载相关数据
      this.loadRelatedData(res || {})
      if (callback) callback()
    }).catch(err => {
      console.error('加载项目详情失败:', err)
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
      this.setData({ loading: false })
      if (callback) callback()
    })
  },

  // 加载相关数据
  loadRelatedData(project) {
    // 从项目对象中解析成员信息
    let members = [];
    if (project.members) {
      try {
        members = JSON.parse(project.members);
      } catch (e) {
        console.error('解析项目成员失败:', e);
      }
    }
    
    this.setData({
      members: Array.isArray(members) ? members : []
    });

    // 加载相关论文
    request.get('/papers/', { project_id: project.id, limit: 10 }).then(res => {
      this.setData({
        papers: Array.isArray(res) ? res : []
      })
    }).catch(err => {
      console.error('加载相关论文失败:', err)
    })

    // 加载相关成果
    request.get('/achievements/', { project_id: project.id, limit: 10 }).then(res => {
      this.setData({
        achievements: Array.isArray(res) ? res : []
      })
    }).catch(err => {
      console.error('加载相关成果失败:', err)
    })
  },

  // 切换Tab
  onTabChange(e) {
    const index = e.currentTarget.dataset.index
    this.setData({
      activeTab: index
    })
  },

  // 跳转到论文详情
  goToPaperDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/papers/detail?id=${id}`
    })
  },

  // 格式化金额
  formatMoney: util.formatMoney,

  // 格式化日期
  formatDate: util.formatDate,

  // 获取状态类型
  getStatusType: util.getProjectStatusType
})
