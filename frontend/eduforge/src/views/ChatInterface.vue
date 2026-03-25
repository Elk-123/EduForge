<!-- ChatInterface.vue - 完整修改版，修复跳转路径 -->
<template>
  <div class="chat-interface">
    <!-- 左侧历史会话侧边栏 -->
    <div class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo-area">
          <span class="iconfont icon-a-gongxiaoshanguangliangdian logo-icon"></span>
          <span v-if="!sidebarCollapsed" class="logo-text">教学智能体</span>
        </div>
        <button class="collapse-btn" @click="sidebarCollapsed = !sidebarCollapsed">
          <span class="iconfont" :class="sidebarCollapsed ? 'icon-xiala' : 'icon-xiala'"></span>
        </button>
      </div>

      <div class="new-chat-section">
        <button class="new-chat-btn" @click="createNewChat">
          <span class="iconfont icon-jia"></span>
          <span v-if="!sidebarCollapsed">新的对话</span>
        </button>
      </div>
      
      <!-- 历史记录 - 分组滚动 -->
      <div class="history-list-container" v-if="!sidebarCollapsed">
        <div class="history-list">
          <!-- 今天 -->
          <div v-if="groupedHistory.today.length" class="history-group">
            <div class="group-title">今天</div>
            <div 
              v-for="chat in groupedHistory.today" 
              :key="chat.id"
              class="history-item"
              :class="{ active: currentChatId === chat.id }"
              @click="selectChat(chat.id)"
            >
              <span class="iconfont icon-wenjian"></span>
              <span class="history-title">{{ chat.title }}</span>
              <span class="history-time">{{ chat.time }}</span>
            </div>
          </div>

          <!-- 昨天 -->
          <div v-if="groupedHistory.yesterday.length" class="history-group">
            <div class="group-title">昨天</div>
            <div 
              v-for="chat in groupedHistory.yesterday" 
              :key="chat.id"
              class="history-item"
              :class="{ active: currentChatId === chat.id }"
              @click="selectChat(chat.id)"
            >
              <span class="iconfont icon-wenjian"></span>
              <span class="history-title">{{ chat.title }}</span>
              <span class="history-time">{{ chat.time }}</span>
            </div>
          </div>

          <!-- 7天内 -->
          <div v-if="groupedHistory.week.length" class="history-group">
            <div class="group-title">最近7天</div>
            <div 
              v-for="chat in groupedHistory.week" 
              :key="chat.id"
              class="history-item"
              :class="{ active: currentChatId === chat.id }"
              @click="selectChat(chat.id)"
            >
              <span class="iconfont icon-wenjian"></span>
              <span class="history-title">{{ chat.title }}</span>
              <span class="history-time">{{ chat.time }}</span>
            </div>
          </div>

          <!-- 更早 -->
          <div v-if="groupedHistory.earlier.length" class="history-group">
            <div class="group-title">更早</div>
            <div 
              v-for="chat in groupedHistory.earlier" 
              :key="chat.id"
              class="history-item"
              :class="{ active: currentChatId === chat.id }"
              @click="selectChat(chat.id)"
            >
              <span class="iconfont icon-wenjian"></span>
              <span class="history-title">{{ chat.title }}</span>
              <span class="history-time">{{ chat.date }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 底部用户信息 - 带三点菜单 -->
      <div class="user-info" v-if="!sidebarCollapsed">
        <div class="user-avatar" @dblclick="goToProfile">
          <img v-if="avatarUrl" :src="avatarUrl" alt="avatar" />
          <span v-else class="iconfont icon-touxiang"></span>
        </div>
        <div class="user-details">
          <div class="user-name">{{ username }}</div>
          <div class="user-role">教师</div>
        </div>
        <button class="user-menu-btn" @click.stop="toggleUserMenu">
          <span class="iconfont icon-gengduo"></span>
        </button>

        <!-- 用户下拉菜单 -->
        <div v-if="showUserMenu" class="dropdown-menu">
          <div class="menu-item" @click="goToProfile">
            <span class="iconfont icon-touxiang"></span>
            <span>个人中心</span>
          </div>
          <div class="menu-item" @click="showHelp">
            <span class="iconfont icon-kefu"></span>
            <span>帮助反馈</span>
          </div>
          <div class="menu-divider"></div>
          <div class="menu-item logout" @click="handleLogout">
            <span class="iconfont icon-tuichu"></span>
            <span>退出登录</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 主聊天区域 -->
    <div class="chat-main">
      <!-- 消息列表 -->
      <div class="messages-container" ref="messagesContainer">
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="page-title">
            <h1>教学智能体</h1>
            <p>您好，{{ username }}老师！我是您的教学助手</p>
          </div>
          
          <!-- 四个功能卡片：PPT、教案、GIF、教学全能包 -->
          <div class="feature-cards">
            <!-- 卡片1: 生成PPT课件 - 直接跳转到PPT编辑器 -->
            <div class="card" @click="goToPPTEditor">
              <div class="card-img-wrapper">
                <div class="card-img card-img-1">
                  <span class="iconfont icon-xinjian_PPTyanshiwengao card-icon"></span>
                </div>
                <div class="card-img-stack stack-1"></div>
                <div class="card-img-stack stack-2"></div>
              </div>
              <h3>生成PPT课件</h3>
              <p>上传教材或输入主题，自动生成精美课件</p>
            </div>
            
            <!-- 卡片2: 编写教案 - 直接跳转到教案编辑器 -->
            <div class="card" @click="goToLessonEditor">
              <div class="card-img-wrapper">
                <div class="card-img card-img-2">
                  <span class="iconfont icon-wendang card-icon"></span>
                </div>
                <div class="card-img-stack stack-1"></div>
                <div class="card-img-stack stack-2"></div>
              </div>
              <h3>编写教案</h3>
              <p>根据教学目标和内容，生成完整教案</p>
            </div>
            
            <!-- 卡片3: 制作教学GIF - 直接跳转到GIF编辑器 -->
            <div class="card" @click="goToGifEditor">
              <div class="card-img-wrapper">
                <div class="card-img card-img-3">
                  <span class="iconfont icon-gif card-icon"></span>
                </div>
                <div class="card-img-stack stack-1"></div>
                <div class="card-img-stack stack-2"></div>
              </div>
              <h3>制作教学GIF</h3>
              <p>将抽象概念转化为生动的动画演示</p>
            </div>
            
            <!-- 卡片4: 教学全能包 - 跳转到三合一预览页面 -->
            <div class="card card-all" @click="generateAllThree">
              <div class="card-img-wrapper">
                <div class="card-img card-img-4">
                  <span class="iconfont icon-jiaoxuekeyan card-icon"></span>
                </div>
                <div class="card-img-stack stack-1"></div>
                <div class="card-img-stack stack-2"></div>
              </div>
              <h3>教学全能包</h3>
              <p>同时生成PPT课件、教案和创意游戏，一步到位</p>
            </div>
          </div>
          
          <div class="example-section">
            <div class="example-title">试试这些示例</div>
            <div class="example-grid">
              <div 
                v-for="prompt in suggestionPrompts" 
                :key="prompt"
                class="example-card"
                @click="setPrompt(prompt)"
              >
                <div class="example-content">
                  <span class="iconfont icon-mobansheji example-icon"></span>
                  <span class="example-text">{{ prompt }}</span>
                </div>
                <div class="example-add">+</div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="message-list">
          <div 
            v-for="(message, index) in messages" 
            :key="index"
            class="message"
            :class="message.role"
          >
            <div class="message-avatar" :class="message.role">
              <span v-if="message.role === 'user'" class="iconfont icon-touxiang"></span>
              <span v-else class="iconfont icon-chuangxindian"></span>
            </div>
            <div class="message-content">
              <div class="message-sender">{{ message.role === 'user' ? '您' : '教学智能体' }}</div>
              <div class="message-text">{{ message.content }}</div>
              
              <!-- 文件预览 -->
              <div v-if="message.files && message.files.length" class="message-files">
                <div v-for="file in message.files" :key="file.name" class="file-item">
                  <span class="iconfont icon-wenjian"></span>
                  <span>{{ file.name }}</span>
                  <span class="file-size">{{ formatFileSize(file.size) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 加载中动画 -->
          <div v-if="isLoading" class="message assistant">
            <div class="message-avatar assistant">
              <span class="iconfont icon-chuangxindian"></span>
            </div>
            <div class="message-content">
              <div class="message-sender">教学智能体</div>
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <div class="input-wrapper" :class="{ 'listening': isListening }">
          <!-- 语音图标 -->
          <button
            class="voice-icon-btn"
            @click="toggleVoiceInput"
            :class="{ active: isListening }"
            :disabled="!isSpeechSupported || isLoading"
          >
            <span class="iconfont icon-yuyin"></span>
          </button>

          <!-- 输入框 -->
          <input
            type="text"
            v-model="userInput"
            :placeholder="isListening ? '正在聆听...' : '输入教学需求...'"
            @keyup.enter="handleSubmit"
            :disabled="isLoading || isListening"
            class="chat-input"
            ref="inputRef"
          />

          <!-- 语音状态指示 -->
          <div v-if="isListening" class="voice-status">
            <span class="voice-wave">
              <span></span><span></span><span></span>
            </span>
            <span class="voice-text">{{ interimTranscript || '聆听中...' }}</span>
          </div>

          <!-- 右侧按钮组 -->
          <div class="action-buttons">
            <!-- 附件按钮 -->
            <button class="action-btn" @click="triggerFileUpload" :disabled="isLoading">
              <span class="iconfont icon-attachment"></span>
            </button>
            <input
              type="file"
              ref="fileInput"
              class="file-input"
              @change="handleFileUpload"
              multiple
              accept=".pdf,.doc,.docx,.ppt,.pptx,.txt,.jpg,.png"
            />

            <!-- 发送按钮 -->
            <button class="send-btn" @click="handleSubmit" :disabled="isLoading || (!userInput.trim() && uploadedFiles.length === 0)">
              <span class="iconfont icon-jijianfasong-xianxing"></span>
            </button>
          </div>
        </div>

        <!-- 已上传文件列表 -->
        <div v-if="uploadedFiles.length" class="uploaded-files">
          <div v-for="(file, index) in uploadedFiles" :key="index" class="uploaded-file-item">
            <span class="iconfont icon-wenjian"></span>
            <span class="file-name">{{ file.name }}</span>
            <span class="file-size">{{ formatFileSize(file.size) }}</span>
            <button class="remove-file" @click="removeFile(index)">×</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 帮助按钮 -->
    <div class="help-button" @click="handleHelp">?</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'

interface ChatSession {
  id: number
  title: string
  time: string
  date: string
  timestamp: number
  messages: any[]
}

const router = useRouter()
const username = ref('用户')
const avatarUrl = ref('')
const sidebarCollapsed = ref(false)
const currentChatId = ref<number | null>(null)
const userInput = ref('')
const isLoading = ref(false)
const messages = ref<any[]>([])
const fileInput = ref<HTMLInputElement | null>(null)
const uploadedFiles = ref<File[]>([])
const messagesContainer = ref<HTMLElement | null>(null)
const inputRef = ref<HTMLInputElement | null>(null)
const showUserMenu = ref(false)

// 语音输入相关
const isListening = ref(false)
const isSpeechSupported = ref(true)
const interimTranscript = ref('')
let recognition: any = null

 // 定义固定剧本
 const conversationScript = [
    {
      step: 1,
      trigger: '操作系统进程调度',
      reply: 'ELK老师，您想讲进程调度的哪一部分？是调度级别（三级调度），经典的调度算法（如 RR 或 MLFQ），还是上下文切换的底层机制？'
    },
    {
      step: 2,
      trigger: '经典调度算法',
      reply: '这堂课是面向考研强化（侧重计算题和复杂推导），还是本科大二初次授课（侧重概念理解和直观演示）？'
    },
    {
      step: 3,
      trigger: '初次授课',
      reply: '正在生成，请稍后...',
      shouldJump: true // 最后一轮标志，准备跳转
    }
  ]

  // 当前进行到第几步
  const currentStep = ref(0)

// 模拟历史会话数据
const chatSessions = ref<ChatSession[]>([
  { id: 1, title: '分数教学课件', time: '10:30', date: '今天', timestamp: Date.now() - 2 * 60 * 60 * 1000, messages: [] },
  { id: 2, title: '光合作用教案', time: '昨天', date: '昨天', timestamp: Date.now() - 26 * 60 * 60 * 1000, messages: [] },
  { id: 3, title: '英语语法讲解', time: '昨天', date: '昨天', timestamp: Date.now() - 30 * 60 * 60 * 1000, messages: [] },
  { id: 4, title: '历史事件时间线', time: '5天前', date: '2024-03-20', timestamp: Date.now() - 5 * 24 * 60 * 60 * 1000, messages: [] },
  { id: 5, title: '数学几何公式', time: '一周前', date: '2024-03-15', timestamp: Date.now() - 8 * 24 * 60 * 60 * 1000, messages: [] }
])

// 按时间分组
const groupedHistory = computed(() => {
  const now = Date.now()
  const oneDay = 24 * 60 * 60 * 1000
  return {
    today: chatSessions.value.filter(chat => chat.timestamp > now - oneDay),
    yesterday: chatSessions.value.filter(chat => chat.timestamp <= now - oneDay && chat.timestamp > now - 2 * oneDay),
    week: chatSessions.value.filter(chat => chat.timestamp <= now - 2 * oneDay && chat.timestamp > now - 7 * oneDay),
    earlier: chatSessions.value.filter(chat => chat.timestamp <= now - 7 * oneDay)
  }
})

const suggestionPrompts = ref([
  '请帮我生成一份关于分数的PPT课件',
  '写一份小学语文《静夜思》的教案',
  '制作一个展示光合作用过程的教学GIF',
  '我需要讲解勾股定理的动画演示',
  '生成一份英语现在完成时的教案',
  '制作细胞分裂过程的教学动画'
])

onMounted(() => {
  const storedUsername = localStorage.getItem('username')
  if (storedUsername) {
    username.value = storedUsername
  }
  
  const savedAvatar = localStorage.getItem('userAvatar')
  if (savedAvatar) {
    avatarUrl.value = savedAvatar
  }

  initSpeechRecognition()
  document.addEventListener('click', handleClickOutside)
  
  // 使用两个图标库
  const link1 = document.createElement('link')
  link1.rel = 'stylesheet'
  link1.href = '//at.alicdn.com/t/c/font_5134397_sbsapm81i9.css'
  document.head.appendChild(link1)
  
  const link2 = document.createElement('link')
  link2.rel = 'stylesheet'
  link2.href = '//at.alicdn.com/t/c/font_5134397_a3b0j21bmu.css'
  document.head.appendChild(link2)
})

onUnmounted(() => {
  if (recognition && isListening.value) {
    recognition.stop()
  }
  document.removeEventListener('click', handleClickOutside)
})

const handleClickOutside = (e: MouseEvent) => {
  const target = e.target as HTMLElement
  if (!target.closest('.user-menu-btn') && !target.closest('.dropdown-menu')) {
    showUserMenu.value = false
  }
}

// 初始化语音识别
const initSpeechRecognition = () => {
  const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
  if (SpeechRecognition) {
    recognition = new SpeechRecognition()
    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = 'zh-CN'
    
    recognition.onstart = () => {
      isListening.value = true
      interimTranscript.value = ''
      console.log('语音识别已启动')
    }
    
    recognition.onend = () => {
      isListening.value = false
      interimTranscript.value = ''
      console.log('语音识别已结束')
    }
    
    recognition.onerror = (event: any) => {
      console.error('语音识别错误:', event.error)
      isListening.value = false
      if (event.error === 'not-allowed') {
        alert('请允许使用麦克风权限')
      }
    }
    
    recognition.onresult = (event: any) => {
      let finalTranscript = ''
      let interimTranscriptTemp = ''
      
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript
        if (event.results[i].isFinal) {
          finalTranscript += transcript
        } else {
          interimTranscriptTemp += transcript
        }
      }
      
      if (finalTranscript) {
        if (userInput.value) {
          userInput.value = userInput.value + ' ' + finalTranscript
        } else {
          userInput.value = finalTranscript
        }
      }
      interimTranscript.value = interimTranscriptTemp
    }
  } else {
    isSpeechSupported.value = false
    console.warn('当前浏览器不支持语音识别')
  }
}

const toggleVoiceInput = () => {
  if (!recognition) {
    alert('当前浏览器不支持语音输入')
    return
  }
  if (isListening.value) {
    recognition.stop()
  } else {
    try {
      recognition.start()
    } catch (error) {
      console.error('启动语音识别失败:', error)
    }
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 创建新对话
const createNewChat = () => {
  const newId = Math.max(...chatSessions.value.map(c => c.id), 0) + 1
  const newChat: ChatSession = {
    id: newId,
    title: '新对话',
    time: '刚刚',
    date: '今天',
    timestamp: Date.now(),
    messages: []
  }
  chatSessions.value.unshift(newChat)
  selectChat(newId)
}

// 选择历史记录功能
const selectChat = (chatId: number) => {
  currentChatId.value = chatId
  const chat = chatSessions.value.find(c => c.id === chatId)
  if (chat) {
    messages.value = chat.messages || []
  }
}

// 设置输入框内容
const setPrompt = (prompt: string) => {
  userInput.value = prompt
  inputRef.value?.focus()
}

// ========== 卡片直接跳转功能 ==========

// 卡片1: 生成PPT课件 - 直接跳转到PPT编辑器
const goToPPTEditor = () => {
  const title = userInput.value.trim() || '新课件'
  router.push({
    path: '/editor',
    query: {
      title: title,
      type: 'ppt',
      t: Date.now().toString()
    }
  })
}

// 卡片2: 编写教案 - 直接跳转到教案编辑器
const goToLessonEditor = () => {
  const title = userInput.value.trim() || '新教案'
  router.push({
    path: '/lesson-editor',
    query: {
      title: title,
      type: 'lesson',
      t: Date.now().toString()
    }
  })
}

// 卡片3: 制作教学GIF - 直接跳转到GIF编辑器
const goToGifEditor = () => {
  const title = userInput.value.trim() || '新动画'
  router.push({
    path: '/gif-editor',
    query: {
      title: title,
      type: 'gif',
      t: Date.now().toString()
    }
  })
}

// 卡片4: 教学全能包 - 跳转到三合一预览页面
const generateAllThree = () => {
  const title = userInput.value.trim() || '教学内容'
  router.push({
    path: '/preview-layout',
    query: {
      title: title,
      type: 'all',
      t: Date.now().toString()
    }
  })
}

// 文件上传相关
const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleFileUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files) {
    const newFiles = Array.from(input.files)
    uploadedFiles.value = [...uploadedFiles.value, ...newFiles]
  }
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const removeFile = (index: number) => {
  uploadedFiles.value.splice(index, 1)
}

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

// 提交消息 - 根据内容类型跳转到对应编辑器
  const handleSubmit = async () => {
  if (!userInput.value.trim() && uploadedFiles.value.length === 0) return
  
  // 1. 处理用户输入（展示在界面上，但不处理逻辑）
  const userMessage = {
    role: 'user',
    content: userInput.value,
    files: uploadedFiles.value.length ? [...uploadedFiles.value] : undefined
  }
  messages.value.push(userMessage)
  
  // 清空输入框
  userInput.value = ''
  uploadedFiles.value = []
  
  await scrollToBottom()
  isLoading.value = true
  if (currentStep.value === 0) {
  fetch('api/v1/generate-content', { // 确保路径正确
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      subject: userMessage.content, // 假设 content 就是主题
      stage: "generate",      // 后端需要这个字段，必须提供 
    })
  }).catch(err => {
    console.warn('静默初始化失败', err);
  });
}
  // 2. 获取当前步骤的剧本内容
  const scriptItem = conversationScript[currentStep.value]
  
  // 模拟 AI 思考延迟
  setTimeout(async () => {
    isLoading.value = false
    
    if (scriptItem) {
      // 推送写死的回复
      messages.value.push({
        role: 'assistant',
        content: scriptItem.reply
      })
      
      // 步骤加 1
      currentStep.value++
      
      await scrollToBottom()

      // 3. 判断是否需要跳转 (只有最后一步“初次授课”之后才跳转)
      if (scriptItem.shouldJump) {
        setTimeout(() => {
          generateAllThree()
        }, 1500)
      }
    } else {
      // 如果超出了剧本范围的保底处理
      messages.value.push({
        role: 'assistant',
        content: '内容已记录，请继续。'
      })
    }
  }, 1500)
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const goToProfile = () => {
  router.push('/profile')
  showUserMenu.value = false
}

const showHelp = () => {
  alert('教学智能体使用说明：\n1. 输入教学需求\n2. 可上传文件\n3. 点击语音按钮说话\n4. 点击卡片快速生成内容')
  showUserMenu.value = false
}

const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    localStorage.removeItem('isLoggedIn')
    localStorage.removeItem('username')
    localStorage.removeItem('userAvatar')
    router.push('/')
  }
}

const handleHelp = () => {
  alert('教学智能体使用说明：\n1. 输入您的教学需求\n2. 可上传教材或参考资料\n3. 点击输入框左侧语音按钮可语音输入\n4. 点击卡片快速生成内容')
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.iconfont {
  font-family: "iconfont" !important;
  font-size: 16px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.chat-interface {
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
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  overflow: hidden;
}

.sidebar {
  width: 280px;
  height: 100vh;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.5);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.sidebar.collapsed {
  width: 70px;
}

.sidebar-header {
  padding: 20px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  flex-shrink: 0;
}

.sidebar:not(.collapsed) .logo-area {
  flex: 1;
  justify-content: center;
}

.sidebar.collapsed .logo-area {
  justify-content: flex-start;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
  color: rgb(11, 167, 175);
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  color: #1e3c5c;
}

.collapse-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 255, 255, 0.7);
  color: #34495e;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  transform: rotate(90deg);
  flex-shrink: 0;
}

.collapse-btn:hover {
  background: white;
  color: rgb(11, 167, 175);
}

.new-chat-section {
  padding: 16px;
}

.new-chat-btn {
  width: 100%;
  height: 40px;
  background: rgb(11, 167, 175);
  border: none;
  border-radius: 20px;
  color: white;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.new-chat-btn:hover {
  background: rgb(8, 130, 136);
  transform: scale(1.02);
}

.history-list-container {
  flex: 1;
  overflow-y: auto;
  padding: 0 12px;
  margin: 0;
  scrollbar-gutter: stable;
}

.history-list-container::-webkit-scrollbar {
  width: 6px;
}

.history-list-container::-webkit-scrollbar-track {
  background: rgba(145, 167, 255, 0.1);
  border-radius: 10px;
}

.history-list-container::-webkit-scrollbar-thumb {
  background: #91a7ff;
  border-radius: 10px;
}

.history-list-container::-webkit-scrollbar-thumb:hover {
  background: #7c9eff;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-right: 2px;
}

.history-group {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.group-title {
  font-size: 12px;
  color: #999;
  padding: 8px 12px 4px;
  font-weight: 500;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.history-item:hover {
  background: rgba(11, 167, 175, 0.1);
}

.history-item.active {
  background: rgba(11, 167, 175, 0.15);
  border-left: 3px solid rgb(11, 167, 175);
}

.history-title {
  flex: 1;
  font-size: 14px;
  color: #34495e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-time {
  font-size: 12px;
  color: #999;
}

.user-info {
  padding: 20px 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-avatar:hover {
  transform: scale(1.05);
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar .iconfont {
  font-size: 24px;
  color: white;
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e3c5c;
}

.user-role {
  font-size: 12px;
  color: #6e7781;
}

.user-menu-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: #999;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.user-menu-btn:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #34495e;
}

.dropdown-menu {
  position: absolute;
  bottom: 70px;
  right: 16px;
  width: 160px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  padding: 8px 0;
  z-index: 100;
  animation: fadeIn 0.2s ease;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #34495e;
  font-size: 14px;
}

.menu-item:hover {
  background: rgba(11, 167, 175, 0.1);
  color: rgb(11, 167, 175);
}

.menu-item.logout:hover {
  background: rgba(255, 99, 99, 0.1);
  color: #ff6b6b;
}

.menu-divider {
  height: 1px;
  background: rgba(0, 0, 0, 0.05);
  margin: 8px 0;
}

.chat-main {
  flex: 1;
  height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
}

.welcome-message {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-title {
  text-align: center;
  margin-bottom: 40px;
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
}

/* 四个功能卡片 - 网格布局 */
.feature-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.card {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.3);
  height: 260px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  border-color: rgba(11, 167, 175, 0.3);
}

.card-all:hover {
  border-color: #9bc0d4;
  box-shadow: 0 12px 24px rgba(155, 192, 212, 0.2);
}

.card-img-wrapper {
  position: relative;
  width: 100%;
  height: 120px;
  margin-bottom: 12px;
  border-radius: 12px;
}

.card-img {
  width: 100%;
  height: 100%;
  border-radius: 12px;
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon {
  font-size: 48px;
  color: white;
  position: relative;
  z-index: 20;
}

.card-img-stack {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 12px;
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

/* 卡片1 - PPT渐变 */
.card-img-1 {
  background: linear-gradient(135deg, #f7d2ea, #f9f0f4);
}
.card:nth-child(1) .stack-1 {
  background: linear-gradient(135deg, #f9d9ee, #faf4f7);
}
.card:nth-child(1) .stack-2 {
  background: linear-gradient(135deg, #fbe0f1, #fcf8fa);
}

/* 卡片2 - 教案渐变 */
.card-img-2 {
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
}
.card:nth-child(2) .stack-1 {
  background: linear-gradient(135deg, #a0b0ff, #e8f0ff);
}
.card:nth-child(2) .stack-2 {
  background: linear-gradient(135deg, #aeb9ff, #edf3ff);
}

/* 卡片3 - GIF渐变 */
.card-img-3 {
  background: linear-gradient(135deg, #f5e3bd, #fdf5e5);
}
.card:nth-child(3) .stack-1 {
  background: linear-gradient(135deg, #f7e8c8, #fef8ec);
}
.card:nth-child(3) .stack-2 {
  background: linear-gradient(135deg, #f9edd3, #fffbf2);
}

/* 卡片4 - 教学全能包渐变（淡蓝色） */
.card-img-4 {
  background: linear-gradient(135deg, #96d1f4, #e6f5fe);
}
.card:nth-child(4) .stack-1 {
  background: linear-gradient(135deg, #b1ddf8, #f0faff);
}
.card:nth-child(4) .stack-2 {
  background: linear-gradient(135deg, #e1f5ff, #e7f6fb);
}

.card-all h3 {
  color: #47b5e0;
}

.card-all p {
  color: #7fb7d4;
}

.card h3 {
  font-size: 16px;
  color: #1a365d;
  margin-bottom: 8px;
  font-weight: 600;
}

.card p {
  font-size: 13px;
  color: #5a6e8a;
  line-height: 1.4;
}

.example-section {
  margin-top: 20px;
}

.example-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
  position: relative;
  text-align: center;
}

.example-title::before,
.example-title::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40%;
  height: 1px;
  background: #ddd;
}

.example-title::before {
  left: 0;
}

.example-title::after {
  right: 0;
}

.example-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.example-card {
  background: rgba(255,255,255,0.8);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 80px;
}

.example-card:hover {
  background: rgba(255,255,255,1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.example-content {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 14px;
  color: #34495e;
  line-height: 1.5;
  flex: 1;
}

.example-icon {
  color: #34495e;
  flex-shrink: 0;
  font-size: 16px;
  margin-top: 2px;
}

.example-add {
  font-size: 18px;
  color: #666;
  font-weight: bold;
  flex-shrink: 0;
  margin-left: 8px;
}

.message-list {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

.message {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  animation: fadeIn 0.3s ease;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message-avatar.user {
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
}

.message-avatar.assistant {
  background: linear-gradient(135deg, #f7d2ea, #f9f0f4);
}

.message-avatar .iconfont {
  font-size: 20px;
  color: white;
}

.message-content {
  max-width: calc(100% - 56px);
}

.message.user .message-content {
  text-align: right;
}

.message-sender {
  font-size: 14px;
  font-weight: 600;
  color: #1e3c5c;
  margin-bottom: 4px;
}

.message-text {
  font-size: 16px;
  color: #34495e;
  line-height: 1.6;
  background: white;
  padding: 12px 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: inline-block;
  max-width: 100%;
}

.message.user .message-text {
  background: rgb(11, 167, 175);
  color: white;
}

.message-files {
  margin-top: 8px;
}

.file-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 13px;
  color: #34495e;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.file-size {
  font-size: 11px;
  color: #999;
}

.input-area {
  max-width: 900px;
  margin: 0 auto 20px;
  width: 100%;
  padding: 0 20px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: white;
  border-radius: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 0 8px 0 4px;
  min-height: 48px;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}

.input-wrapper.listening {
  border-color: rgb(8, 130, 136);
  background: #f0f8ff;
}

.voice-icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: rgb(11, 167, 175);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.voice-icon-btn:hover:not(:disabled) {
  background: rgba(11, 167, 175, 0.1);
  color: rgb(8, 130, 136);
}

.voice-icon-btn.active {
  color: white;
  background: #ff6b6b;
  animation: pulse 1.5s infinite;
}

.voice-icon-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.chat-input {
  flex: 1;
  height: 48px;
  padding: 0 8px;
  border: none;
  outline: none;
  font-size: 16px;
  color: #34495e;
  background: transparent;
  min-width: 0;
}

.chat-input::placeholder {
  color: #999;
}

.chat-input:disabled {
  background: transparent;
  cursor: not-allowed;
}

.voice-status {
  position: absolute;
  left: 48px;
  right: 100px;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f0f8ff;
  border-radius: 30px;
  color: rgb(8, 130, 136);
  pointer-events: none;
  padding-left: 8px;
}

.voice-wave {
  display: flex;
  align-items: center;
  gap: 3px;
  height: 20px;
}

.voice-wave span {
  width: 3px;
  height: 100%;
  background: rgb(11, 167, 175);
  border-radius: 3px;
  animation: wave 1s ease-in-out infinite;
}

.voice-wave span:nth-child(2) {
  animation-delay: 0.2s;
}

.voice-wave span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes wave {
  0%, 100% { transform: scaleY(0.3); }
  50% { transform: scaleY(1); }
}

.voice-text {
  font-size: 14px;
  color: rgb(8, 130, 136);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.action-buttons {
  display: flex;
  gap: 4px;
  align-items: center;
  flex-shrink: 0;
  margin-left: auto;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: white;
  color: rgb(11, 167, 175);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.action-btn:hover:not(:disabled) {
  background: rgba(11, 167, 175, 0.1);
  color: rgb(8, 130, 136);
  transform: scale(1.05);
}

.send-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgb(11, 167, 175);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.send-btn:hover:not(:disabled) {
  background: rgb(8, 130, 136);
  transform: scale(1.05);
}

.send-btn:disabled,
.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.file-input {
  display: none;
}

.uploaded-files {
  margin-top: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.uploaded-file-item {
  background: white;
  border-radius: 20px;
  padding: 6px 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #34495e;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.file-name {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remove-file {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: none;
  background: #ff6b6b;
  color: white;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 4px;
  transition: all 0.2s ease;
}

.remove-file:hover {
  background: #ff5252;
  transform: scale(1.1);
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  width: fit-content;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #71cdd1;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.6;
  }
  30% {
    transform: translateY(-6px);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

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

.messages-container::-webkit-scrollbar,
.history-list-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track,
.history-list-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

.messages-container::-webkit-scrollbar-thumb,
.history-list-container::-webkit-scrollbar-thumb {
  background: rgba(11, 167, 175, 0.3);
  border-radius: 10px;
}

.messages-container::-webkit-scrollbar-thumb:hover,
.history-list-container::-webkit-scrollbar-thumb:hover {
  background: rgba(11, 167, 175, 0.5);
}

/* 响应式 */
@media (max-width: 1200px) {
  .feature-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .example-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .sidebar {
    position: absolute;
    z-index: 100;
  }
  
  .feature-cards {
    grid-template-columns: 1fr;
  }
  
  .example-grid {
    grid-template-columns: 1fr;
  }
  
  .page-title h1 {
    font-size: 36px;
  }
  
  .page-title p {
    font-size: 16px;
  }
}
</style>