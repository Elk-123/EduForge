<!-- ChatPage2.vue - 粘贴文本页面，与GeneratePage风格统一 -->
<template>
  <div class="chat2-container">
    <!-- 返回按钮 - 与GeneratePage完全一致 -->
    <div class="button-group">
      <button class="back-button outline-button icon-button" @click="goBack">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
    </div>

    <!-- 主标题区域 - 与GeneratePage风格统一 -->
    <div class="title-main">粘贴文本</div>
    <div class="title-sub">您想要创建什么？</div>

    <!-- 类型选择区 - 改为方块样式，与GeneratePage的方块一致 -->
    <div class="block-container">
      <div class="white-block block-item" 
           :class="{ active: selectedType === 'presentation' }"
           @click="selectedType = 'presentation'">
        <div class="icon-wrapper">
          <span class="iconfont icon-xinjian_PPTyanshiwengao block-icon"></span>
        </div>
        <div class="block-text">演示文稿</div>
      </div>

      <div class="white-block block-item" 
           :class="{ active: selectedType === 'document' }"
           @click="selectedType = 'document'">
        <div class="icon-wrapper">
          <span class="iconfont icon-wendang block-icon"></span>
        </div>
        <div class="block-text">文档</div>
      </div>
    </div>

    <!-- 下拉选择栏 - 与GeneratePage一致 -->
    <div class="select-bar">
      <div class="select-item" @click.stop="toggleDropdown('orientation')">
        <span class="iconfont icon-bili-ziyoubili select-icon"></span>
        <span>{{ selectedOrientation }}</span>
        <span class="iconfont icon-xiala select-arrow" :class="{ rotated: dropdownOpen.orientation }"></span>
        <div v-if="dropdownOpen.orientation" class="dropdown-menu">
          <div class="dropdown-item" @click.stop="selectOrientation('纵向')">纵向</div>
          <div class="dropdown-item" @click.stop="selectOrientation('横向')">横向</div>
          <div class="dropdown-item" @click.stop="selectOrientation('方形')">方形</div>
        </div>
      </div>

      <div class="select-item" @click.stop="toggleDropdown('language')">
        <span class="iconfont icon-yuyan select-icon"></span>
        <span>{{ selectedLanguage }}</span>
        <span class="iconfont icon-xiala select-arrow" :class="{ rotated: dropdownOpen.language }"></span>
        <div v-if="dropdownOpen.language" class="dropdown-menu">
          <div class="dropdown-item" @click.stop="selectLanguage('简体中文')">简体中文</div>
          <div class="dropdown-item" @click.stop="selectLanguage('繁体中文')">繁体中文</div>
          <div class="dropdown-item" @click.stop="selectLanguage('English')">English</div>
          <div class="dropdown-item" @click.stop="selectLanguage('日本語')">日本語</div>
        </div>
      </div>
    </div>

    <!-- 内容粘贴区 - 重新设计，与整体风格统一 -->
    <div class="content-section">
      <div class="content-label">粘贴您要使用的笔记、大纲或文本内容</div>
      <div class="textarea-container">
        <textarea 
          v-model="pastedText" 
          placeholder="在此处键入或粘贴内容..."
          class="main-textarea"
        ></textarea>
      </div>
    </div>

    <!-- 功能选择区 - 改为卡片样式 -->
    <div class="action-section">
      <div class="action-label">您想用这些内容做什么呢？</div>
      <div class="action-grid">
        <div class="action-card" 
             :class="{ active: selectedAction === 'generate' }"
             @click="selectedAction = 'generate'">
          <span class="iconfont icon-xinjian_PPTyanshiwengao action-icon"></span>
          <div class="action-text">
            <div class="action-title">根据笔记或大纲生成</div>
            <div class="action-desc">将粗略的想法、要点或大纲转化为精美的内容</div>
          </div>
        </div>

        <div class="action-card" 
             :class="{ active: selectedAction === 'summarize' }"
             @click="selectedAction = 'summarize'">
          <span class="iconfont icon-wendang action-icon"></span>
          <div class="action-text">
            <div class="action-title">总结长文本或文档</div>
            <div class="action-desc">非常适合将详细内容浓缩成更易于呈现的内容</div>
          </div>
        </div>

        <div class="action-card" 
             :class="{ active: selectedAction === 'keep' }"
             @click="selectedAction = 'keep'">
          <span class="iconfont icon-niantiewenben action-icon"></span>
          <div class="action-text">
            <div class="action-title">保持此文本的原样</div>
            <div class="action-desc">使用您的文字进行创作，完全按照您所写的内容进行创作</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部按钮 - 与GeneratePage的发送按钮风格一致 -->
    <div class="bottom-actions">
      <button class="next-btn" @click="goToGenerate">
        <span>继续前往提示编辑器</span>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-left: 8px;">
          <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      <div class="import-tip">
        <span class="iconfont icon-daoru" style="margin-right: 4px;"></span>
        您还可以导入文件
      </div>
    </div>

    <!-- 帮助按钮 - 与GeneratePage一致 -->
    <div class="help-button" @click="handleHelp">?</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const pastedText = ref('')
const selectedType = ref('presentation')
const selectedAction = ref('generate')
const selectedOrientation = ref('纵向')
const selectedLanguage = ref('简体中文')

// 下拉菜单状态
const dropdownOpen = ref({
  orientation: false,
  language: false
})

// 点击其他地方关闭下拉菜单
onMounted(() => {
  document.addEventListener('click', () => {
    Object.keys(dropdownOpen.value).forEach(key => {
      dropdownOpen.value[key as keyof typeof dropdownOpen.value] = false
    })
  })
})

const goBack = () => {
  router.back()
}

const toggleDropdown = (menu: string) => {
  Object.keys(dropdownOpen.value).forEach(key => {
    if (key !== menu) {
      dropdownOpen.value[key as keyof typeof dropdownOpen.value] = false
    }
  })
  dropdownOpen.value[menu as keyof typeof dropdownOpen.value] = !dropdownOpen.value[menu as keyof typeof dropdownOpen.value]
}

const selectOrientation = (orientation: string) => {
  selectedOrientation.value = orientation
  dropdownOpen.value.orientation = false
}

const selectLanguage = (language: string) => {
  selectedLanguage.value = language
  dropdownOpen.value.language = false
}

const goToGenerate = () => {
  router.push({
    path: '/generate',
    query: { 
      text: pastedText.value,
      type: selectedType.value,
      action: selectedAction.value 
    }
  })
}

const handleHelp = () => {
  alert('选择内容类型和操作，粘贴文本后点击继续')
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

/* 主容器 - 与GeneratePage完全一致 */
.chat2-container {
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
  padding: 20px 0;
}

/* 按钮组 - 与GeneratePage完全一致 */
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

/* 标题 - 与GeneratePage完全一致 */
.title-main {
  font-size: 48px;
  color: #2c3e50;
  font-weight: bold;
  margin-bottom: 16px;
  margin-top: 10px;
}

.title-sub {
  font-size: 18px;
  color: #34495e;
  margin-bottom: 40px;
}

/* 方块容器 - 与GeneratePage一致 */
.block-container {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  align-items: center;
  justify-content: center;
}

/* 方块样式 - 与GeneratePage完全一致 */
.white-block {
  width: 180px;
  height: 100px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.white-block.active {
  border: 2px solid rgb(11, 167, 175);
  background-color: #f0f8ff;
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.2);
}

.icon-wrapper {
  margin-top: -10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.block-icon {
  font-size: 40px;
  color: #71cdd1;
}

.white-block.active .block-icon {
  color: #4ad0e2;
}

.block-text {
  margin-top: 5px;
  font-size: 14px;
  color: #34495e;
}

.white-block.active .block-text {
  color: #4ad0e2;
}

/* 下拉选择栏 - 与GeneratePage一致 */
.select-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 30px;
  position: relative;
  z-index: 100;
}

.select-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  color: #34495e;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
}

.select-item:hover {
  background: #f8f9fa;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.select-arrow {
  transition: transform 0.3s ease;
  font-size: 12px;
}

.select-arrow.rotated {
  transform: rotate(180deg);
}

.select-icon {
  color: #34495e;
  font-size: 16px;
}

/* 下拉菜单 - 与GeneratePage一致 */
.dropdown-menu {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  min-width: 120px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  overflow: hidden;
  z-index: 1000;
  animation: dropdownFade 0.2s ease;
}

@keyframes dropdownFade {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  padding: 10px 16px;
  font-size: 14px;
  color: #34495e;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.dropdown-item:hover {
  background: #f0f8ff;
  color: rgb(11, 167, 175);
}

/* 内容粘贴区 */
.content-section {
  width: 60%;
  max-width: 900px;
  margin-bottom: 30px;
}

.content-label {
  font-size: 14px;
  color: #34495e;
  margin-bottom: 12px;
  text-align: center;
}

.textarea-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  width: 100%;
}

.main-textarea {
  width: 100%;
  height: 200px;
  border: none;
  outline: none;
  resize: none;
  font-size: 16px;
  color: #34495e;
  line-height: 1.6;
  font-family: inherit;
}

.main-textarea::placeholder {
  color: #999;
}

/* 功能选择区 */
.action-section {
  width: 60%;
  max-width: 900px;
  margin-bottom: 30px;
}

.action-label {
  font-size: 14px;
  color: #34495e;
  margin-bottom: 16px;
  text-align: center;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.action-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(11, 167, 175, 0.5);
}

.action-card.active {
  border: 2px solid rgb(11, 167, 175);
  background-color: #f0f8ff;
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.2);
}

.action-icon {
  font-size: 32px;
  color: #71cdd1;
}

.action-card.active .action-icon {
  color: #4ad0e2;
}

.action-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.action-title {
  font-size: 16px;
  color: #1a365d;
  font-weight: 600;
}

.action-desc {
  font-size: 12px;
  color: #4a5568;
  line-height: 1.5;
}

.action-card.active .action-title {
  color: #1a365d;
}

/* 底部按钮 */
.bottom-actions {
  width: 60%;
  max-width: 900px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.next-btn {
  background: rgb(11, 167, 175);
  color: white;
  border: none;
  border-radius: 30px;
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.next-btn:hover {
  background: rgb(8, 130, 136);
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.3);
}

.next-btn:active {
  transform: scale(0.98);
}

.import-tip {
  font-size: 14px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 帮助按钮 - 与GeneratePage一致 */
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

/* 响应式适配 */
@media (max-width: 1024px) {
  .action-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .content-section,
  .action-section,
  .bottom-actions {
    width: 80%;
  }
}

@media (max-width: 768px) {
  .title-main {
    font-size: 40px;
  }
  
  .title-sub {
    font-size: 16px;
  }
  
  .block-container {
    flex-direction: column;
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
  
  .content-section,
  .action-section,
  .bottom-actions {
    width: 90%;
  }
}

@media (max-width: 480px) {
  .title-main {
    font-size: 32px;
  }
  
  .select-bar {
    flex-direction: column;
    align-items: center;
  }
}
</style>