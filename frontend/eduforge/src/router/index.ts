// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import AICourseGenerate from '@/views/AICourseGenerate.vue'
import LoginPage from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import ProfilePage from '@/views/ProfilePage.vue'
// 导入其他页面组件
import ChatPage2 from '@/views/ChatPage2.vue'
import ChatPage3 from '@/views/ChatPage3.vue'
import GeneratePage from '@/views/GeneratePage.vue'
import Generateword from '@/views/Generateword.vue'
import ImportPage from '@/views/ImportPage.vue'
import EditorView from '@/views/EditorView.vue'
// 导入忘记密码页面
import ForgotPasswordPage from '@/views/ForgotPasswordPage.vue'  // 新增

const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
  // 新增忘记密码路由
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPasswordPage
  },
  {
    path: '/home',
    name: 'home',
    component: AICourseGenerate
  },
  // 个人中心路由
  {
    path: '/profile',
    name: 'profile',
    component: ProfilePage
  },
  // AICourseGenerate 页面的四个卡片路由
  {
    path: '/generate',
    name: 'generate',
    component: GeneratePage
  },
  {
    path: '/generate/word',
    name: 'generate-word',
    component: Generateword
  },
  {
    path: '/chat2',
    name: 'chat2',
    component: ChatPage2
  },
  {
    path: '/chat3',
    name: 'chat3',
    component: ChatPage3
  },
  {
    path: '/import',
    name: 'import',
    component: ImportPage
  },
  // 新增编辑器路由
  {
    path: '/editor',
    name: 'editor',
    component: EditorView
  },
  // 编辑特定PPT的路由（带ID参数）
  {
    path: '/editor/:id',
    name: 'editor-detail',
    component: EditorView
  },
  // 重定向：如果访问不存在的路径，跳转到登录页
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：检查是否需要登录
router.beforeEach((to, from, next) => {
  // 不需要登录验证的页面（登录页、注册页和忘记密码页）
  const publicPages = ['/', '/register', '/forgot-password']  // 修改这里，添加忘记密码页
  
  // 检查当前路径是否需要登录
  const authRequired = !publicPages.includes(to.path)
  
  // 检查是否已登录
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  
  if (authRequired && !isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router