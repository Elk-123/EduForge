// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  // ===== 新增这部分配置 =====
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // 你的 FastAPI 后端运行地址
        changeOrigin: true, // 允许跨域
        // 因为你后端的路由本身就是以 /api 开头的（prefix="/api/auth"），
        // 所以直接转发即可，不需要路径重写 (rewrite)
      }
    }
  }
    // =========================
})