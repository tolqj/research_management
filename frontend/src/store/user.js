import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi } from '@/services/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  // 登录
  const login = async (username, password) => {
    try {
      const res = await loginApi({ username, password })
      token.value = res.access_token
      user.value = res.user
      
      // 保存到本地存储
      localStorage.setItem('token', res.access_token)
      localStorage.setItem('user', JSON.stringify(res.user))
      
      return true
    } catch (error) {
      return false
    }
  }

  // 登出
  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // 更新用户信息
  const updateUser = (newUser) => {
    user.value = newUser
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  return {
    token,
    user,
    login,
    logout,
    updateUser
  }
})
