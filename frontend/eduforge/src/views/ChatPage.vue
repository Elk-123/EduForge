<template>
  <div class="app">
    <div class="sidebar">
      <div class="logo">智构古韵</div>
      <button 
        class="new-chat-btn" 
        @click="createNewChat"
        :class="{ active: isNewChatActive }"
      >
        <!-- 👇 新对话图标：替换成你的黑色图标路径即可 -->
        <img src="/icons/new-chat.png" class="sidebar-icon" alt="新对话">
        新对话
      </button>

      <!-- 历史对话折叠栏：含标题、横线、展开/收起按钮 -->
      <div class="history-collapse-header" @click="toggleHistory">
        <!-- 统一样式的横线：和logo下横线同色、左右留边、长度更长 -->
        <div class="history-top-line"></div>
        <div class="history-title-wrapper">
          <div class="history-title">
            <img src="/icons/history.png" class="title-icon" alt="历史对话">
            历史对话
          </div>
          <!-- 👇 展开/收起：纯图标按钮（无文字、无阴影） -->
          <button class="collapse-btn">
            <img 
              :src="isHistoryOpen ? '/icons/collapse.png' : '/icons/expand.png'" 
              class="collapse-icon" 
              alt="展开/收起"
            >
          </button>
        </div>
      </div>

      <!-- 历史对话列表：恢复滚轮，仅在展开时显示 -->
      <div class="history-list" v-show="isHistoryOpen">
        <div 
          class="history-item" 
          v-for="item in historyList" 
          :key="item.id"
          :class="{ active: item.id === currentChatId }"
          @click="switchChat(item.id)"
        >
          {{ item.title }}
        </div>
      </div>
    </div>

    <div class="chat-main">
      <div class="background-container">
        <img src="/images/main-bg.jpg" class="main-bg" alt="主背景">
        <div class="bg-top-left-btn">
          <button class="back-btn" @click="goBackToHome">
           <img src="/icons/back.png" class="back-icon" alt="返回">
            首页
          </button>
        </div>
        <img src="/images/decor1.png" class="decor-item decor1" alt="装饰1">
        <img src="/images/decor2.png" class="decor-item decor2" alt="装饰2">
        <img src="/images/decor3.png" class="decor-item decor3" alt="装饰3">
        <img src="/images/decor4.png" class="decor-item decor4" alt="装饰4">
        <img src="/images/decor5.png" class="decor-item decor5" alt="装饰5">
        <img src="/images/decor6.png" class="decor-item decor6" alt="装饰6">
      </div>

      <div class="chat-messages" ref="chatMessagesRef">
        <div class="empty-state" v-if="messages.length === 0">
          <div class="empty-title">欢迎使用古建筑 AI 教学助手</div>
          <div class="empty-desc">请输入和【{{ currentTopic }}】相关的 PPT 具体要求～</div>
        </div>

        <div v-else>
          <div 
            class="message" 
            :class="{ userMessage: msg.isUser, aiMessage: !msg.isUser }"
            v-for="msg in messages" 
            :key="msg.id"
          >
            <div class="bubble">{{ msg.content }}</div>
          </div>
        </div>
      </div>

      <div class="chat-input-wrapper">
        <div class="chat-input">
          <div class="input-icons-row">
            <img src="/icons/icon1.png" class="func-icon" alt="附件">
            <img src="/icons/icon2.png" class="func-icon" alt="选择语言">
            <img src="/icons/icon3.png" class="func-icon" alt="传输文档">
          </div>
          <div class="input-bar">
            <input 
              type="text" 
              v-model="inputText" 
              :placeholder="`请输入和【${currentTopic}】相关的PPT要求`"
              @keyup.enter="sendMessage"
            >
            <div class="right-buttons">
              <button class="voice-btn">
                <img src="/icons/mic.png" class="btn-icon" alt="麦克风">
              </button>
              <button class="send-btn" @click="sendMessage" :disabled="!inputText">
                <img src="/icons/send.png" class="btn-icon" alt="发送">
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 新增：引入路由
import { useRouter } from 'vue-router'
import { ref, watch, nextTick } from 'vue'

// 初始化路由实例
const router = useRouter()

// 新增：返回首页函数
// ChatPage.vue - <script setup> 中的返回函数
// ChatPage.vue - <script setup> 内部
const goBackToHome = () => {
  router.push('/') // 根路径对应路由配置中的 AICourseGenerate 首页
}
const inputText = ref('')
const messages = ref([])
const isLoading = ref(false)
const chatMessagesRef = ref(null)
const isNewChatActive = ref(false)

// 新增：历史对话展开/收起状态（默认展开）
const isHistoryOpen = ref(true)

// 历史对话列表
const historyList = ref([
  { id: 1, title: '唐代建筑特点PPT' },
  { id: 2, title: '斗拱结构教学课件' },
  { id: 3, title: '故宫角楼结构拆解' },
  { id: 4, title: '宋代木构建筑解析' },
  { id: 5, title: '明清宫殿建筑特点' },
  { id: 6, title: '徽派建筑马头墙设计' },
  { id: 7, title: '山西古建斗拱工艺' },
  { id: 8, title: '江南园林建筑布局' },
  { id: 9, title: '长城建筑材料分析' },
  { id: 10, title: '敦煌石窟建筑特色' },
])

const currentChatId = ref(1)
const currentTopic = ref('唐代建筑')

// 发送消息逻辑
const sendMessage = () => {
  if (!inputText.value) return
  messages.value.push({ id: Date.now(), content: inputText.value, isUser: true })
  inputText.value = ''
  isLoading.value = true

  setTimeout(() => {
    messages.value.push({
      id: Date.now() + 1,
      content: `已收到【${currentTopic.value}】PPT需求，正在为你生成…`,
      isUser: false
    })
    isLoading.value = false
  }, 2000)
}

// 新建对话逻辑
const createNewChat = () => {
  const id = Date.now()
  historyList.value.unshift({ id, title: '新对话' })
  currentChatId.value = id
  messages.value = []
  currentTopic.value = '古建筑'
  isNewChatActive.value = true
}

// 切换对话逻辑
const switchChat = (id) => {
  currentChatId.value = id
  const item = historyList.value.find(i => i.id === id)
  currentTopic.value = item.title.replace('PPT','').replace('教学课件','')
  messages.value = []
  isNewChatActive.value = false
}

// 新增：展开/收起历史对话
const toggleHistory = () => {
  isHistoryOpen.value = !isHistoryOpen.value
}

// 消息滚动到底部
watch(messages, () => {
  nextTick(() => {
    if (chatMessagesRef.value) {
      chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
    }
  })
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "SimSun", "Source Han Serif", "思源宋体", serif;
}
.app {
  display: flex;
  height: 100vh;
  background: #fff;
}

/* 左侧边栏 */
.sidebar {
  width: 240px;
  background: #fff;
  display: flex;
  flex-direction: column;
  padding: 20px 0;
  z-index: 10;
}
.logo {
  padding: 0 25px 16px;
  font-size: 20px;
  font-weight: bold;
  color: #000;
  border-bottom: 1px solid #eee; /* 基准横线样式 */
}
.new-chat-btn {
  margin: 10px 15px 15px 15px;
  padding: 10px 12px 10px 10px;
  background: #fff;
  border: none;
  border-radius: 6px;
  text-align: left;
  cursor: pointer;
  font-size: 14px;
  color: #000;
  display: flex;
  align-items: center;
  gap: 8px;
}
.new-chat-btn:hover { background: #f2f2f2; }
.new-chat-btn.active { color: #B06A5A; }

/* 图标样式统一 */
.sidebar-icon, .title-icon, .back-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* 核心1：历史对话折叠头部（含横线+标题+折叠标签） */
.history-collapse-header {
  cursor: pointer;
  padding: 0 15px;
}

/* 核心2：横线样式统一：和logo下横线同色(#eee)、左右留边、长度更长 */
.history-top-line {
  height: 1px;
  background: #eee; /* 与logo下横线颜色一致 */
  margin: 0 10px 8px 10px; /* 左右留边，不接边界，长度更长 */
}

/* 标题+折叠标签容器 */
.history-title-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 5px;
}

/* 核心3：恢复历史对话标题样式：字小、颜色浅，与新对话区分 */
.history-title {
  font-size: 12px; /* 比新对话小 */
  color: #999; /* 浅灰色，做区分 */
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 👇 新增：展开/收起图标按钮样式（无背景、无阴影、纯图标） */
.collapse-btn {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important; /* 彻底去掉阴影 */
  padding: 0 !important;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
/* 展开/收起图标大小统一 */
.collapse-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* 核心5：恢复历史对话滚轮：独立容器、固定高度、超出滚动 */
.history-list {
  margin: 0 15px;
  max-height: 280px; /* 固定高度，保证滚轮出现 */
  overflow-y: auto; /* 恢复滚轮 */
  flex-shrink: 0;
}
/* 滚轮美化，与整体风格统一 */
.history-list::-webkit-scrollbar {
  width: 4px;
}
.history-list::-webkit-scrollbar-thumb {
  background-color: #eee;
  border-radius: 2px;
}

/* 历史对话项样式不变 */
.history-item {
  padding: 8px 12px 8px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  margin-bottom: 4px;
}
.history-item:hover { background: #f2f2f2; }
.history-item.active {
  background: rgba(176, 106, 90, 0.2);
  color: rgba(176, 106, 90, 1);
  font-weight: bold;
}

/* 右侧主区域（无修改，保留所有优化） */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  padding-bottom: 120px;
}

.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  background: #f2e0d6;
  overflow: hidden;
}
.main-bg {
  width: 100%;
  height: 100%;
  object-fit: cover;
  mix-blend-mode: multiply;
  opacity: 0.8;
}
.decor-item {
  position: absolute;
  pointer-events: none;
  mix-blend-mode: multiply;
  opacity: 0.9;
}
.decor1 { left:-80px; top: 180px; width: 539px; height: 718px; }
.decor2 { left: 300px; top: -20px; width: 320px; height: 420px; }
.decor3 { left: 400px; top: 350px; width: 340px; height: 400px; }
.decor4 { left: 700px; top: 140px; width: 239px; height: 297px; }
.decor5 { left: 750px; top: 318px; width: 611px; height: 811px; }
.decor6 { left: 1000px; top: 0px; width: 300px; height: 300px; }

.bg-top-left-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 99;
}
/* 新增：保证button样式和原a标签一致 */
.back-btn {
  border: none;
  background: none;
  font-size: 15px;
  font-weight: bold;
  color: #333;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.8);
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
}

.chat-messages {
  flex: 1;
  padding: 30px 50px;
  overflow-y: auto;
  position: relative;
  z-index: 1;
}
.chat-messages::-webkit-scrollbar {
  width: 6px;
}
.chat-messages::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.1);
  border-radius: 3px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  margin-bottom: 50px;
}
.empty-title {
  font-size: 24px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 10px;
}
.empty-desc {
  font-size: 16px;
  color: #fff;
}

.message {
  max-width: 65%;
  margin-bottom: 18px;
}
.bubble {
  padding: 12px 16px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
.userMessage { margin-left: auto; }
.aiMessage { margin-right: auto; }

.chat-input-wrapper {
  position: absolute;
  left: 50%;
  bottom: 100px;
  transform: translateX(-50%);
  width: 98%;
  max-width: 1400px;
  z-index: 1;
}
.chat-input {
  background: rgba(255,255,255,0.95);
  border-radius: 24px;
  padding: 16px 24px;
  border: 1px solid #FFD700;
}
.input-icons-row {
  padding: 0 20px 8px;
  display: flex;
  gap: 15px;
}
.func-icon {
  width: 20px;
  height: 20px;
  opacity: 0.7;
  cursor: pointer;
}
.input-bar {
  display: flex;
  align-items: center;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 20px;
  padding: 0 16px;
  height: 48px;
}
input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
}
.right-buttons {
  display: flex;
  gap: 12px;
  align-items: center;
}

.voice-btn,
.send-btn {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.2s ease;
}
.voice-btn:hover,
.send-btn:hover {
  opacity: 0.7;
}
.btn-icon {
  width: 20px;
  height: 20px;
}
</style>