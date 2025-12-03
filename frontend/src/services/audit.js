import request from './request'

/**
 * 获取审计日志列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @param {string} params.username - 用户名
 * @param {string} params.operation - 操作类型
 * @param {string} params.module - 模块名称
 * @param {string} params.status - 操作结果
 * @param {string} params.start_date - 开始日期 YYYY-MM-DD
 * @param {string} params.end_date - 结束日期 YYYY-MM-DD
 * @returns {Promise}
 */
export const getAuditLogs = (params) => {
  return request({
    url: '/audit/logs',
    method: 'get',
    params
  })
}

/**
 * 获取审计日志详情
 * @param {number} id - 日志ID
 * @returns {Promise}
 */
export const getAuditLogDetail = (id) => {
  return request({
    url: `/audit/logs/${id}`,
    method: 'get'
  })
}

/**
 * 获取审计日志统计
 * @param {number} days - 统计最近N天，默认7天
 * @returns {Promise}
 */
export const getAuditStatistics = (days = 7) => {
  return request({
    url: '/audit/logs/statistics',
    method: 'get',
    params: { days }
  })
}
