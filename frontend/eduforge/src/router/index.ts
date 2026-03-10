import { createRouter, createWebHistory } from 'vue-router'

// 导入所有页面
import AICourseGenerate from '@/views/AICourseGenerate.vue'
import ChatPage2 from '@/views/ChatPage2.vue'
import ChatPage3 from '@/views/ChatPage3.vue'
import GeneratePage from '@/views/GeneratePage.vue'
import Generateword from '@/views/Generateword.vue'
// 新增导入 AI 导入页面
import ImportPage from '@/views/ImportPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: AICourseGenerate
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
    path: '/generate',
    name: 'generate',
    component: GeneratePage
  },
  {
    path: '/generate/word',
    name: 'generate-word',
    component: Generateword
  },
  // 新增 AI 导入页面路由
  {
    path: '/import',
    name: 'import',
    component: ImportPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router