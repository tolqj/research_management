// utils/util.js

/**
 * 格式化时间
 */
function formatTime(date) {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return `${[year, month, day].map(formatNumber).join('-')} ${[hour, minute, second].map(formatNumber).join(':')}`
}

/**
 * 格式化日期
 */
function formatDate(date) {
  if (!date) return ''
  
  // 如果已经是 YYYY-MM-DD 格式的字符串，直接返回
  if (typeof date === 'string') {
    // 匹配 YYYY-MM-DD 格式
    const match = date.match(/^(\d{4})-(\d{2})-(\d{2})/)
    if (match) {
      return match[0] // 返回 YYYY-MM-DD 部分
    }
    // 尝试转换其他格式
    date = new Date(date.replace(/-/g, '/'))
  } else if (!(date instanceof Date)) {
    // 如果不是Date对象，尝试转换
    date = new Date(date)
  }
  
  // 检查是否为有效日期
  if (!date || isNaN(date.getTime())) {
    return ''
  }
  
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  return [year, month, day].map(formatNumber).join('-')
}

function formatNumber(n) {
  n = n.toString()
  return n[1] ? n : `0${n}`
}

/**
 * 格式化金额
 */
function formatMoney(amount) {
  if (amount === null || amount === undefined) return '0.00'
  return Number(amount).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * 获取项目状态标签类型
 */
function getProjectStatusType(status) {
  const typeMap = {
    '草稿': 'info',
    '已申报': 'primary',
    '执行中': 'success',
    '已结题': 'warning'
  }
  return typeMap[status] || 'info'
}

/**
 * 获取论文分区颜色
 */
function getJcrZoneType(zone) {
  const typeMap = {
    'Q1': 'danger',
    'Q2': 'warning',
    'Q3': 'primary',
    'Q4': 'info'
  }
  return typeMap[zone] || 'info'
}

/**
 * 获取成果类型标签
 */
function getAchievementType(type) {
  const typeMap = {
    'PATENT': '专利',
    'AWARD': '奖项',
    'BOOK': '著作',
    'SOFTWARE': '软著'
  }
  return typeMap[type] || type
}

/**
 * 获取成果类型颜色
 */
function getAchievementTypeColor(type) {
  const colorMap = {
    'PATENT': 'success',
    'AWARD': 'warning',
    'BOOK': 'primary',
    'SOFTWARE': 'info'
  }
  return colorMap[type] || 'info'
}

/**
 * 节流函数
 */
function throttle(fn, delay = 500) {
  let timer = null
  return function (...args) {
    if (timer) return
    timer = setTimeout(() => {
      fn.apply(this, args)
      timer = null
    }, delay)
  }
}

/**
 * 防抖函数
 */
function debounce(fn, delay = 500) {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

module.exports = {
  formatTime,
  formatDate,
  formatMoney,
  getProjectStatusType,
  getJcrZoneType,
  getAchievementType,
  getAchievementTypeColor,
  throttle,
  debounce
}
