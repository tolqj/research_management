import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/',
    component: () => import('@/views/layout.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '工作台', icon: 'DataAnalysis' }
      },
      {
        path: 'project',
        name: 'Project',
        component: () => import('@/views/project/index.vue'),
        meta: { title: '项目管理', icon: 'Management' }
      },
      {
        path: 'project/detail/:id',
        name: 'ProjectDetail',
        component: () => import('@/views/project/detail.vue'),
        meta: { title: '项目详情', hidden: true }
      },
      {
        path: 'paper',
        name: 'Paper',
        component: () => import('@/views/paper/index.vue'),
        meta: { title: '论文管理', icon: 'Document' }
      },
      {
        path: 'fund',
        name: 'Fund',
        component: () => import('@/views/fund/index.vue'),
        meta: { title: '经费管理', icon: 'Money' }
      },
      {
        path: 'achievement',
        name: 'Achievement',
        component: () => import('@/views/achievement/index.vue'),
        meta: { title: '成果管理', icon: 'TrophyBase' }
      },
      {
        path: 'system',
        name: 'System',
        redirect: '/system/user',
        meta: { title: '系统管理', icon: 'Setting' },
        children: [
          {
            path: 'user',
            name: 'UserManagement',
            component: () => import('@/views/system/user.vue'),
            meta: { title: '用户管理', requiresAdmin: true }
          },
          {
            path: 'profile',
            name: 'Profile',
            component: () => import('@/views/system/profile.vue'),
            meta: { title: '个人信息' }
          }
        ]
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 科研管理系统` : '科研管理系统'
  
  // 检查是否需要登录
  if (to.meta.requiresAuth && !userStore.token) {
    next('/login')
    return
  }
  
  // 检查管理员权限
  if (to.meta.requiresAdmin && userStore.user?.role !== '管理员') {
    ElMessage.error('权限不足')
    next(false)
    return
  }
  
  next()
})

export default router
