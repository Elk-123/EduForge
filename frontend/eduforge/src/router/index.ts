import { createRouter, createWebHistory } from 'vue-router'

// 忽略TS对Vue文件的类型警告（避免报错）
// @ts-ignore
import AICourseGenerate from '../views/AICourseGenerate.vue'
// @ts-ignore
import ChatPage from '../views/ChatPage.vue'

const routes = [
  // 根路径 → 默认显示AI生成页（你要看到的页面）
  {
    path: '/',
    name: 'AICourseGenerate',
    component: AICourseGenerate
  },
  // /chat路径 → 显示聊天页
  {
    path: '/chat',
    name: 'ChatPage',
    component: ChatPage
  }
]

const router = createRouter({
  history: createWebHistory(), // 必须用createWebHistory
  routes
})

export default router