/**
 * 数据导出工具
 * 使用 xlsx 库导出Excel文件
 */
import * as XLSX from 'xlsx'

/**
 * 导出数据到Excel
 * @param {Array} data - 要导出的数据数组
 * @param {Array} columns - 列配置 [{label: '列名', prop: '字段名'}]
 * @param {String} filename - 文件名（不含扩展名）
 */
export const exportToExcel = (data, columns, filename = '导出数据') => {
  try {
    // 构建表头
    const headers = columns.map(col => col.label)
    
    // 构建数据行
    const rows = data.map(item => {
      return columns.map(col => {
        // 处理嵌套属性
        const value = getNestedValue(item, col.prop)
        // 格式化函数
        return col.formatter ? col.formatter(value, item) : value
      })
    })
    
    // 合并表头和数据
    const sheetData = [headers, ...rows]
    
    // 创建工作表
    const worksheet = XLSX.utils.aoa_to_sheet(sheetData)
    
    // 设置列宽
    const colWidths = columns.map(col => ({
      wch: col.width || 15
    }))
    worksheet['!cols'] = colWidths
    
    // 创建工作簿
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1')
    
    // 生成文件名（带时间戳）
    const timestamp = new Date().toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    }).replace(/[/:]/g, '-').replace(/\s/g, '_')
    
    const fullFilename = `${filename}_${timestamp}.xlsx`
    
    // 导出文件
    XLSX.writeFile(workbook, fullFilename)
    
    return true
  } catch (error) {
    console.error('导出Excel失败:', error)
    return false
  }
}

/**
 * 获取嵌套对象的值
 * @param {Object} obj - 对象
 * @param {String} path - 属性路径，如 'user.name'
 */
const getNestedValue = (obj, path) => {
  if (!path) return ''
  
  const keys = path.split('.')
  let value = obj
  
  for (const key of keys) {
    if (value && typeof value === 'object' && key in value) {
      value = value[key]
    } else {
      return ''
    }
  }
  
  return value !== null && value !== undefined ? value : ''
}

/**
 * 格式化日期
 * @param {String|Date} date - 日期
 */
export const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  if (isNaN(d.getTime())) return date
  
  return d.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

/**
 * 格式化日期时间
 * @param {String|Date} datetime - 日期时间
 */
export const formatDateTime = (datetime) => {
  if (!datetime) return ''
  const d = new Date(datetime)
  if (isNaN(d.getTime())) return datetime
  
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

/**
 * 格式化金额
 * @param {Number} amount - 金额
 */
export const formatAmount = (amount) => {
  if (amount === null || amount === undefined) return ''
  return `¥${Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })}`
}
