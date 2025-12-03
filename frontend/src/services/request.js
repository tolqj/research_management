import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import router from '@/router'

// 创建 axios 实例
const request = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    
    // 过滤掉 params 中值为 undefined、null 或空字符串的参数
    if (config.params) {
      const originalParams = { ...config.params }
      const filteredParams = {}
      Object.keys(config.params).forEach(key => {
        const value = config.params[key]
        if (value !== undefined && value !== null && value !== '') {
          filteredParams[key] = value
        }
      })
      config.params = filteredParams
      
      // 调试日志：显示过滤后的参数
      console.log(`[Request] ${config.method.toUpperCase()} ${config.baseURL}${config.url}`)
      console.log('[Request] 原始参数:', originalParams)
      console.log('[Request] 过滤后:', filteredParams)
    }
    
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    // 为了向后兼容，保持返回data，但在data上附加headers属性
    const data = response.data
    // 如果是数组或对象，添加headers属性
    if (typeof data === 'object' && data !== null) {
      data.headers = response.headers
    }
    return data
  },
  error => {
    // 打印完整的错误信息
    console.error('[Response Error]', error.response)
    
    if (error.response) {
      const status = error.response.status
      const message = error.response.data?.detail || '请求失败'
      
      // 422 错误详细信息
      if (status === 422) {
        console.error('[422 Error Details]', error.response.data)
      }
      
      switch (status) {
        case 401:
          // 如果是登录接口返回401，不显示“登录已过期”提示
          if (!error.config.url.includes('/auth/login')) {
            ElMessage.error('登录已过期，请重新登录')
            const userStore = useUserStore()
            userStore.logout()
            router.push('/login')
          }
          // 登录接口的401错误交给登录页面处理
          break
        case 403:
          ElMessage.error('权限不足')
          break
        case 404:
          ElMessage.error('资源不存在')
          break
        case 422:
          // 422 不显示错误消息，只在控制台打印
          console.error('[422] Validation Error:', message)
          break
        case 500:
          ElMessage.error('服务器错误')
          break
        default:
          ElMessage.error(message)
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }
    return Promise.reject(error)
  }
)

export default request
