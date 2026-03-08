<!-- ImportPage.vue - 无任何滚动条版本 -->
<template>
  <div class="import-container">
    <!-- 返回按钮 - 与 GeneratePage 完全一致 -->
    <div class="button-group">
      <button class="back-button outline-button icon-button" @click="goBack">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
    </div>

    <!-- 标题区域 - 与 GeneratePage 完全一致 -->
    <div class="title-main">使用 AI 导入</div>
    <div class="title-sub">选择要转换的文件</div>

    <!-- 卡片容器 - 三列布局，自适应高度 -->
    <div class="card-container">
      <!-- 卡片 1：上传文件 -->
      <div class="card" @click="handleUpload">
        <div class="card-img-wrapper">
          <div class="card-img card-img-upload">
            <span class="iconfont icon-wenjian card-icon"></span>
          </div>
          <div class="card-img-stack stack-1"></div>
          <div class="card-img-stack stack-2"></div>
        </div>
        <h3>上传文件</h3>
        <ul class="support-list">
          <li><span class="check-icon">✓</span> Powerpoint PPTX</li>
          <li><span class="check-icon">✓</span> Word 文档</li>
          <li><span class="check-icon">✓</span> PDFs</li>
        </ul>
        <div class="card-footer">
          <span class="iconfont icon-wenjian footer-icon"></span>
        </div>
      </div>

      <!-- 卡片 2：从 Drive 导入 -->
      <div class="card" @click="handleDriveImport">
        <div class="card-img-wrapper">
          <div class="card-img card-img-drive">
            <span class="iconfont icon-drive card-icon"></span>
          </div>
          <div class="card-img-stack stack-1"></div>
          <div class="card-img-stack stack-2"></div>
        </div>
        <h3>从 Drive 导入</h3>
        <ul class="support-list">
          <li><span class="check-icon">✓</span> Google 幻灯片</li>
          <li><span class="check-icon">✓</span> Google 文档</li>
        </ul>
        <div class="card-footer">
          <span class="iconfont icon-drive footer-icon"></span>
        </div>
      </div>

      <!-- 卡片 3：从 URL 导入 -->
      <div class="card" @click="handleUrlImport">
        <div class="card-img-wrapper">
          <div class="card-img card-img-url">
            <span class="iconfont icon-URLguanli card-icon"></span>
          </div>
          <div class="card-img-stack stack-1"></div>
          <div class="card-img-stack stack-2"></div>
        </div>
        <h3>从 URL 导入</h3>
        <ul class="support-list">
          <li><span class="check-icon">✓</span> 网页</li>
          <li><span class="check-icon">✓</span> 博客帖子或文章</li>
          <li><span class="check-icon">✓</span> 概念文档（仅公开）</li>
        </ul>
        <div class="card-footer">
          <span class="iconfont icon-URLguanli footer-icon"></span>
        </div>
      </div>
    </div>

    <!-- 底部提示 - 与整体风格统一 -->
    <div class="bottom-tip">
      如果您的文件不受支持，也可以
      <a href="#" @click.prevent="goToPasteText" class="tip-link">粘贴文本</a>
      <span class="iconfont icon-niantiewenben tip-icon"></span>
    </div>

    <!-- 帮助按钮 - 与 GeneratePage 一致 -->
    <div class="help-button" @click="handleHelp">?</div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.back()
}

const handleUpload = () => {
  // 打开文件选择器
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.pptx,.docx,.pdf'
  input.onchange = (e) => {
    const file = (e.target as HTMLInputElement).files?.[0]
    if (file) {
      console.log('选择文件:', file.name)
      // TODO: 处理文件上传
    }
  }
  input.click()
}

const handleDriveImport = () => {
  alert('跳转到 Google Drive 授权/选择页面')
  // TODO: 实现 Google Drive 导入
}

const handleUrlImport = () => {
  const url = prompt('请输入网页 URL:')
  if (url) {
    console.log('导入 URL:', url)
    // TODO: 处理 URL 导入
  }
}

const goToPasteText = () => {
  router.push('/chat2')
}

const handleHelp = () => {
  alert('使用 AI 导入：支持从本地上传、Drive 或 URL 导入文件并转换')
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

/* 主容器 - 关键：禁止所有滚动，高度100vh，flex自适应内容 */
.import-container {
  width: 100vw;
  height: 100vh; /* 固定高度为视口高度 */
  background: linear-gradient(
    to bottom,
    rgba(212, 245, 245, 0.2),
    rgba(130, 212, 215, 0.5) 25%,
    rgba(174, 230, 231, 0.5) 50%,
    rgba(189, 236, 236, 0.3) 75%,
    rgba(189, 236, 236, 0.3)
  );
  overflow: hidden; /* 彻底禁止所有滚动（水平+垂直） */
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0 60px; /* 调整上下内边距，适配视口 */
}

/* 按钮组 - 与 GeneratePage 完全一致 */
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

/* 主标题 - 调整间距，适配无滚动布局 */
.title-main {
  font-size: 48px;
  color: #2c3e50;
  font-weight: bold;
  margin-top: 10px; /* 减少上边距 */
  margin-bottom: 16px; /* 减少下边距 */
}

/* 副标题 - 调整间距 */
.title-sub {
  font-size: 18px;
  color: #34495e;
  margin-bottom: 25px; /* 减少下边距 */
}

/* 卡片容器 - 关键：flex-grow自适应剩余高度，限制最大高度 */
.card-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px; /* 减少卡片间距 */
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 0 20px;
  flex-grow: 1; /* 自动填充剩余空间 */
  align-items: center; /* 垂直居中卡片 */
  max-height: calc(100vh - 220px); /* 限制最大高度，避免溢出 */
}

/* 卡片样式 - 调整高度，适配无滚动布局 */
.card {
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
  cursor: pointer;
  border: 2px solid transparent;
  height: 340px; /* 降低卡片高度 */
  display: flex;
  flex-direction: column;
  width: 100%;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(11, 167, 175, 0.5);
}

/* 彩色图案区堆叠容器 - 调整高度 */
.card-img-wrapper {
  position: relative;
  width: 100%;
  height: 140px; /* 降低图片区高度 */
  border-radius: 12px 12px 0 0;
  overflow: hidden;
}

/* 主图案区 */
.card-img {
  width: 100%;
  height: 100%;
  border-radius: 12px 12px 0 0;
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 图标样式 */
.card-icon {
  font-size: 50px; /* 缩小图标 */
  color: white;
  position: relative;
  z-index: 20;
}

/* 堆叠层 */
.card-img-stack {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 12px 12px 0 0;
  z-index: 5;
}

.stack-1 {
  top: 6px;
  left: 6px;
  opacity: 0.7;
  z-index: 8;
}

.stack-2 {
  top: 12px;
  left: 12px;
  opacity: 0.4;
  z-index: 5;
}

/* 卡片1：上传文件（浅紫渐变） */
.card-img-upload {
  background: linear-gradient(135deg, #b8a0ff, #d4c2ff);
}
.card:nth-child(1) .stack-1 {
  background: linear-gradient(135deg, #c5b0ff, #ddd0ff);
}
.card:nth-child(1) .stack-2 {
  background: linear-gradient(135deg, #d2c0ff, #e6ddff);
}

/* 卡片2：Drive（浅蓝渐变） */
.card-img-drive {
  background: linear-gradient(135deg, #73b9ff, #9ecfff);
}
.card:nth-child(2) .stack-1 {
  background: linear-gradient(135deg, #88c4ff, #b1d9ff);
}
.card:nth-child(2) .stack-2 {
  background: linear-gradient(135deg, #9dcfff, #c3e4ff);
}

/* 卡片3：URL（浅青渐变） */
.card-img-url {
  background: linear-gradient(135deg, #5fd9cc, #8de6db);
}
.card:nth-child(3) .stack-1 {
  background: linear-gradient(135deg, #7ae0d5, #a1ece3);
}
.card:nth-child(3) .stack-2 {
  background: linear-gradient(135deg, #94e7de, #b5f1ea);
}

/* 卡片内容 - 调整间距 */
.card h3 {
  font-size: 18px; /* 缩小标题 */
  color: #1a365d;
  font-weight: 600;
  margin: 12px 20px 6px; /* 减少间距 */
}

.support-list {
  list-style: none;
  margin: 0 20px;
  flex: 1;
}

.support-list li {
  font-size: 13px; /* 缩小文字 */
  color: #4a5568;
  margin-bottom: 4px; /* 减少间距 */
  display: flex;
  align-items: center;
  gap: 6px;
}

.check-icon {
  color: #10b981;
  font-weight: bold;
  font-size: 14px; /* 缩小对勾 */
}

/* 卡片底部 - 调整间距 */
.card-footer {
  padding: 12px 20px; /* 减少内边距 */
  text-align: right;
  border-top: 1px solid #f0f0f0;
}

.footer-icon {
  font-size: 18px; /* 缩小图标 */
  color: #71cdd1;
  transition: all 0.2s ease;
}

.card:hover .footer-icon {
  color: rgb(11, 167, 175);
  transform: scale(1.1);
}

/* 底部提示 - 调整位置 */
.bottom-tip {
  margin-top: 10px;
  font-size: 16px;
  color: #34495e;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding-bottom: 10px; /* 减少底部间距 */
}

.tip-link {
  color: rgb(11, 167, 175);
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tip-link:hover {
  color: rgb(8, 130, 136);
  text-decoration: underline;
}

.tip-icon {
  font-size: 18px;
  color: #71cdd1;
}

/* 帮助按钮 - 与 GeneratePage 一致 */
.help-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #34495e;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
  z-index: 1000;
}

.help-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 响应式适配 - 同步调整尺寸 */
@media (max-width: 1024px) {
  .card-container {
    grid-template-columns: repeat(2, 1fr);
    max-width: 800px;
    max-height: calc(100vh - 200px);
  }
  .card {
    height: 320px;
  }
}

@media (max-width: 768px) {
  .title-main {
    font-size: 40px;
    margin-top: 20px;
  }
  .title-sub {
    font-size: 16px;
    margin-bottom: 20px;
  }
  .card-container {
    grid-template-columns: 1fr;
    max-width: 400px;
    max-height: calc(100vh - 180px);
  }
  .card {
    height: 300px;
  }
}

@media (max-width: 480px) {
  .title-main {
    font-size: 32px;
    margin-top: 20px;
  }
  .card-img-wrapper {
    height: 120px;
  }
  .card-icon {
    font-size: 44px;
  }
}
</style>