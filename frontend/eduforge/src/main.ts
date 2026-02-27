import { createApp } from 'vue'
import App from './App.vue'
// 引入路由（关键：必须挂载路由）
import router from './router/index.ts'

// 创建App并挂载路由
const app = createApp(App)
app.use(router) // 没有这一行，路由完全不生效！
app.mount('#app')