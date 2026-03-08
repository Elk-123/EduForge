// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import GeneratePage from '@/views/GeneratePage.vue'
import Generateword from '@/views/Generateword.vue'
import Generateweb from '@/views/Generateweb.vue'
import Generatesocial from '@/views/Generatesocial.vue'  // 添加社媒页面导入

const routes = [
  {
    path: '/',
    name: 'home',
    component: GeneratePage
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
  {
    path: '/generate/web',
    name: 'generate-web',
    component: Generateweb
  },
  {
    path: '/generate/social',  // 添加社媒路由
    name: 'generate-social',
    component: Generatesocial
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router