import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import ForgotPasswordPage from '@/views/ForgotPasswordPage.vue'
import ChatInterface from '@/views/ChatInterface.vue'
import PreviewPage from '@/views/PreviewPage.vue'
import ProfilePage from '@/views/ProfilePage.vue'
import PPTEditor from '@/components/PPTEditor.vue'
import LessonEditor from '@/components/LessonEditor.vue'
import GifEditor from '@/components/GifEditor.fixed.vue'

const routes = [
  { path: '/', name: 'Login', component: LoginPage },
  { path: '/login', name: 'LoginPage', component: LoginPage },
  { path: '/register', name: 'RegisterPage', component: RegisterPage },
  { path: '/forgot-password', name: 'ForgotPasswordPage', component: ForgotPasswordPage },
  { path: '/chat', name: 'ChatInterface', component: ChatInterface },
  { path: '/preview', name: 'PreviewPage', component: PreviewPage },
  { path: '/editor', name: 'PPTEditor', component: PPTEditor },
  { path: '/lesson-editor', name: 'LessonEditor', component: LessonEditor },
  { path: '/gif-editor', name: 'GifEditor', component: GifEditor }, // 这里用的是修复版
  { path: '/profile', name: 'Profile', component: ProfilePage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router