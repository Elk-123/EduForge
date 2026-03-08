<!-- AICourseGenerate.vue - 使用你的 iconfont 图标 -->
<template>
  <div class="gradient-container">
    <!-- 顶部返回按钮 -->
    <div class="button-group">
      <button class="back-button outline-button icon-button" @click="goBack">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
    </div>

    <!-- 主标题区域 -->
    <div class="page-title">
      <h1>使用 AI 创建</h1>
      <p>您希望如何开始？</p>
    </div>

    <!-- 卡片容器 -->
    <div class="card-container">
      <!-- 第一个卡片：生成 - 用 ✨ 表情符号（因为iconfont里没有合适的） -->
      <div class="card" @click="goToGenerate">
        <div class="card-img-wrapper">
          <div class="card-img card-img-1">
            <span class="iconfont icon-a-gongxiaoshanguangliangdian card-icon"></span>
          </div>
          <div class="card-img-stack stack-1"></div>
          <div class="card-img-stack stack-2"></div>
        </div>
        <h3>生成</h3>
        <p>在几秒钟内根据一行提示创建</p>
        <span class="badge recommend">⭐ 已推荐</span>
      </div>

      <!-- 第二个卡片：粘贴文本 - 使用 icon-niantiewenben -->
      <div class="card" @click="goToChatPage2">
        <div class="card-img-wrapper">
          <div class="card-img card-img-2">
            <span class="iconfont icon-niantiewenben card-icon"></span>
          </div>
          <div class="card-img-stack stack-1"></div>
          <div class="card-img-stack stack-2"></div>
        </div>
        <h3>粘贴文本</h3>
        <p>根据笔记、大纲或现有内容创建</p>
      </div>

      <!-- 第三个卡片：从模板创建 - 使用 icon-mobansheji -->
      <div class="card" @click="goToChatPage3">
        <div class="card-img-wrapper">
          <div class="card-img card-img-3">
            <span class="iconfont icon-mobansheji card-icon"></span>
          </div>
          <div class="card-img-stack stack-1"></div>
          <div class="card-img-stack stack-2"></div>
        </div>
        <h3>从模板创建</h3>
        <p>使用模板的结构或布局进行创建</p>
        <span class="badge new">新功能</span>
      </div>

      <!-- 第四个卡片：导入文件 - 使用 icon-daoru -->
      <div class="card" @click="goToImportPage"> <!-- 修改点击事件 -->
        <div class="card-img-wrapper">
          <div class="card-img card-img-4">
            <span class="iconfont icon-daoru card-icon"></span>
          </div>
          <div class="card-img-stack stack-1"></div>
          <div class="card-img-stack stack-2"></div>
        </div>
        <h3>导入文件或 URL</h3>
        <p>增强现有文档、演示文稿或网页的功能</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.back()
}

const goToGenerate = () => {
  router.push('/generate')
}

const goToChatPage2 = () => {
  router.push('/chat2')
}

const goToChatPage3 = () => {
  router.push('/chat3')
}

// 新增：跳转到 AI 导入页面的方法
const goToImportPage = () => {
  router.push('/import')
}
</script>

<style scoped>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* 渐变背景容器 */
.gradient-container {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(
    to bottom,
    rgba(212, 245, 245, 0.2),
    rgba(130, 212, 215, 0.5) 25%,
    rgba(174, 230, 231, 0.5) 50%,
    rgba(189, 236, 236, 0.3) 75%,
    rgba(189, 236, 236, 0.3)
  );
  overflow-y: auto;
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 按钮组样式 */
.button-group {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 99;
}

.outline-button {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 6px;
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #34495e;
  transition: all 0.2s ease;
}

.outline-button:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: scale(1.05);
}

/* 页面标题样式 */
.page-title {
  text-align: center;
  padding-top: 80px;
  margin-bottom: 30px;
}

.page-title h1 {
  font-size: 48px;
  color: #2c3e50;
  font-weight: 700;
  margin-bottom: 8px;
}

.page-title p {
  font-size: 18px;
  color: #34495e;
  text-align: center;
}

/* 卡片容器 */
.card-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  margin-top: 20px;
}

/* 卡片样式 */
.card {
  background: #ffffff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
  cursor: pointer;
  border: 2px solid transparent;
  height: 340px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(11, 167, 175, 0.5);
}

/* 彩色图案区堆叠容器 */
.card-img-wrapper {
  position: relative;
  width: 100%;
  height: 180px;
  margin-bottom: 12px;
  border-radius: 8px;
}

/* 主图案区（最上层） */
.card-img {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 字体图标样式 */
.card-icon {
  font-size: 60px;
  color: white;
  position: relative;
  z-index: 20;
}

/* 表情符号样式 */
.emoji-icon {
  font-size: 60px;
  color: white;
  position: relative;
  z-index: 20;
  line-height: 1;
}

/* 堆叠层通用样式 */
.card-img-stack {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
  z-index: 5;
}

/* 第一层堆叠 */
.stack-1 {
  top: 6px;
  left: 6px;
  opacity: 0.7;
  z-index: 8;
}

/* 第二层堆叠 */
.stack-2 {
  top: 12px;
  left: 12px;
  opacity: 0.4;
  z-index: 5;
}

/* 卡片1：生成（浅粉系） */
.card-img-1 {
  background: linear-gradient(135deg, #f7d2ea, #f9f0f4);
}
.card:nth-child(1) .stack-1 {
  background: linear-gradient(135deg, #f9d9ee, #faf4f7);
}
.card:nth-child(1) .stack-2 {
  background: linear-gradient(135deg, #fbe0f1, #fcf8fa);
}

/* 卡片2：粘贴文本（浅蓝紫系） */
.card-img-2 {
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
}
.card:nth-child(2) .stack-1 {
  background: linear-gradient(135deg, #a0b0ff, #e8f0ff);
}
.card:nth-child(2) .stack-2 {
  background: linear-gradient(135deg, #aeb9ff, #edf3ff);
}

/* 卡片3：从模板创建（浅黄系） */
.card-img-3 {
  background: linear-gradient(135deg, #f5e3bd, #fdf5e5);
}
.card:nth-child(3) .stack-1 {
  background: linear-gradient(135deg, #f7e8c8, #fef8ec);
}
.card:nth-child(3) .stack-2 {
  background: linear-gradient(135deg, #f9edd3, #fffbf2);
}

/* 卡片4：导入文件（浅青蓝系） */
.card-img-4 {
  background: linear-gradient(135deg, #9bcbed, #e1f6f7);
}
.card:nth-child(4) .stack-1 {
  background: linear-gradient(135deg, #a8d4ef, #e6f8f9);
}
.card:nth-child(4) .stack-2 {
  background: linear-gradient(135deg, #b5dcf1, #ebfafa);
}

/* 卡片文字样式 */
.card h3 {
  font-size: 18px;
  color: #1a365d;
  margin-bottom: 6px;
  font-weight: 600;
}

.card p {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.5;
  margin-bottom: 8px;
  flex: 1;
}

/* 徽章样式 */
.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.badge.recommend {
  background: #fef0f5;
  color: #b47289;
  border: 1px solid #f7d2ea33;
}

.badge.new {
  background: #fef9e7;
  color: #b58958;
  border: 1px solid #f5e3bd33;
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .card-container {
    grid-template-columns: repeat(2, 1fr);
    max-width: 800px;
  }
  
  .page-title h1 {
    font-size: 40px;
  }
  
  .page-title p {
    font-size: 16px;
  }

  .stack-1 {
    top: 4px;
    left: 4px;
  }
  .stack-2 {
    top: 8px;
    left: 8px;
  }
}

@media (max-width: 640px) {
  .card-container {
    grid-template-columns: 1fr;
    max-width: 400px;
  }
  
  .page-title h1 {
    font-size: 32px;
  }
  
  .page-title p {
    font-size: 14px;
  }

  .stack-1 {
    top: 3px;
    left: 3px;
  }
  .stack-2 {
    top: 6px;
    left: 6px;
  }
}
</style>