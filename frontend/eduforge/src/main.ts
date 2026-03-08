import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // 引入路由

createApp(App).use(router).mount('#app') // 必须调用 .use(router)