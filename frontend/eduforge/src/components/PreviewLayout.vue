<!-- PreviewLayout.vue - 修正A4纸比例，添加语音输入和附件 -->
<template>
  <div class="preview-layout">
    <!-- 三栏主体布局 -->
    <div class="main-layout">
      <!-- 左侧：切换按钮栏 -->
      <div class="left-sidebar">
        <button 
          class="preview-tab-btn"
          :class="{ active: activeTab === 'ppt' }"
          @click="activeTab = 'ppt'"
        >
          <span class="iconfont icon-PPT"></span>
          <span>PPT预览</span>
        </button>
        <button 
          class="preview-tab-btn"
          :class="{ active: activeTab === 'lesson' }"
          @click="activeTab = 'lesson'"
        >
          <span>教案预览</span>
        </button>
        <button 
          class="preview-tab-btn"
          :class="{ active: activeTab === 'game' }"
          @click="activeTab = 'game'"
        >
          <span class="iconfont icon-youxi"></span>
          <span>游戏互动</span>
        </button>
      </div>

      <!-- 中间：预览区域 -->
      <div class="preview-area">
        <!-- PPT预览 -->
        <div v-show="activeTab === 'ppt'" class="preview-content">
          <div class="preview-header-tip">
            <h3>PPT课件预览</h3>
            <span class="tip-badge"></span>
          </div>
          <div class="white-frame" ref="pptFrameRef"></div>
        </div>

        <!-- 教案预览 - A4纸标准比例 -->
        <div v-show="activeTab === 'lesson'" class="preview-content">
          <div class="preview-header-tip">
            <h3>教案预览</h3>
            <span class="tip-badge"></span>
          </div>
          <div class="lesson-canvas" ref="lessonCanvasRef">
            <div class="lesson-pages">
              <div v-for="(page, pageIndex) in (lessonPages.length ? lessonPages : [''])" :key="pageIndex" class="lesson-page">
                <div class="lesson-page-content" v-html="page"></div>
                <div class="lesson-page-num">{{ pageIndex + 1 }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 游戏互动 -->
        <div v-show="activeTab === 'game'" class="preview-content">
          <div class="preview-header-tip">
            <h3>游戏互动：操作系统进程调度算法演示</h3>
            <span class="tip-badge">交互式动画</span>
          </div>
          <div class="white-frame">
            <iframe 
              src="/1.html" 
              style="width: 100%; height: 100%; border: none; border-radius: 16px;"
              title="游戏互动演示"
            ></iframe>
          </div>
        </div>
      </div>

      <!-- 右侧：AI对话聊天框 -->
      <div class="chat-sidebar">
        <div class="chat-header">
          <span class="iconfont icon-chuangxindian"></span>
          <h3>AI 教学助手</h3>
          <span class="current-tab">当前: {{ currentTabName }}</span>
        </div>
        
        <div class="chat-messages" ref="chatMessagesRef">
          <div v-for="(msg, idx) in chatMessages" :key="idx" class="chat-message" :class="msg.role">
            <div class="message-avatar">
              <span v-if="msg.role === 'user'" class="iconfont icon-touxiang"></span>
              <span v-else class="iconfont icon-chuangxindian"></span>
            </div>
            <div class="message-content">
              <div class="message-text">{{ msg.content }}</div>
            </div>
          </div>
          <div v-if="isAILoading" class="chat-message assistant">
            <div class="message-avatar">
              <span class="iconfont icon-chuangxindian"></span>
            </div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入区域 - 添加语音和附件按钮 -->
        <div class="chat-input-area">
          <div class="input-wrapper" :class="{ 'listening': isListening }">
            <!-- 语音按钮 -->
            <button
              class="voice-icon-btn"
              @click="toggleVoiceInput"
              :class="{ active: isListening }"
              :disabled="!isSpeechSupported"
            >
              <span class="iconfont icon-yuyin"></span>
            </button>

            <!-- 输入框 -->
            <textarea
              v-model="userInput"
              :placeholder="isListening ? '正在聆听...' : `修改当前${currentTabName}的内容...`"
              @keyup.enter.exact="sendMessage"
              rows="2"
              class="chat-textarea"
            ></textarea>

            <!-- 语音状态指示 -->
            <div v-if="isListening" class="voice-status">
              <span class="voice-wave">
                <span></span><span></span><span></span>
              </span>
              <span class="voice-text">{{ interimTranscript || '聆听中...' }}</span>
            </div>

            <!-- 附件按钮 -->
            <button class="attachment-btn" @click="triggerFileUpload" :disabled="isAILoading">
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
            <button class="send-btn" @click="sendMessage" :disabled="!userInput.trim() || isAILoading">
              <span class="iconfont icon-jijianfasong-xianxing"></span>
            </button>
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

          <div class="input-tip">
            💡 提示：输入"修改标题为..."、"增加一页"、"添加步骤"等指令
          </div>
        </div>
      </div>
    </div>
    <button 
      class="fixed-download-btn"
      @click="downloadFile"
    >
      <span class="iconfont icon-xiazai"></span>
      <span>下载课件/教案</span>
    </button>
  </div>
  <button 
    class="preview-tab-btn"
    @click="openGame"
  >
    <span class="iconfont icon-youxi"></span>
    <span>游戏互动</span>
  </button>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { renderAsync } from 'docx-preview'

const router = useRouter()
const route = useRoute()

const activeTab = ref<'ppt' | 'lesson' | 'game'>('ppt')
const pageTitle = ref('')
const pptData = ref<string | null>(null)
const lessonData = ref<string | null>(null)
const gameData = ref<string | null>(null)

const lessonPages = ref<string[]>([])
const lessonCanvasRef = ref<HTMLElement | null>(null)

// 输入框相关
const userInput = ref('')
const isAILoading = ref(false)
const chatMessages = ref<Array<{ role: 'user' | 'assistant'; content: string }>>([])
const chatMessagesRef = ref<HTMLElement | null>(null)

// 语音相关
const isListening = ref(false)
const isSpeechSupported = ref(true)
const interimTranscript = ref('')
let recognition: any = null

// 附件相关
const fileInput = ref<HTMLInputElement | null>(null)
const uploadedFiles = ref<File[]>([])

const pptFrameRef = ref<HTMLElement | null>(null)
const gameFrameRef = ref<HTMLElement | null>(null)

const currentTabName = computed(() => {
  switch (activeTab.value) {
    case 'ppt': return 'PPT'
    case 'lesson': return '教案'
    case 'game': return '游戏互动'
    default: return '内容'
  }
})

// 在 script 部分添加处理函数

const openGame = () => {
  // 使用 window.open 会在新标签页打开
  window.open('/1.html', '_blank');
};

// 格式化文件大小
const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

// 触发文件上传
const triggerFileUpload = () => {
  fileInput.value?.click()
}

// 处理文件上传
const handleFileUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    const newFiles = Array.from(input.files)
    uploadedFiles.value = [...uploadedFiles.value, ...newFiles]
    
    // --- 核心逻辑：获取最新上传的文件进行判断 ---
    const file = newFiles[0]
    const ext = file.name.split('.').pop()?.toLowerCase()

    if (ext === 'pdf') {
      handlePDFPreview(file)
    } else if (ext === 'docx') {
      await handleWordPreview(file)
    }
    // ----------------------------------------

    chatMessages.value.push({
      role: 'assistant',
      content: `已收到 ${newFiles.length} 个文件，正在为您开启预览...`
    })
    scrollChatToBottom()
  }
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// 移除文件
const removeFile = (index: number) => {
  uploadedFiles.value.splice(index, 1)
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
    }
    
    recognition.onend = () => {
      isListening.value = false
      interimTranscript.value = ''
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
  }
}

// 切换语音输入
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

// 分页函数
const splitIntoPages = (htmlContent: string): string[] => {
  if (!htmlContent) return []
  
  const tempDiv = document.createElement('div')
  tempDiv.style.cssText = `
    position: absolute;
    visibility: hidden;
    width: 210mm;
    padding: 2.54cm 3.17cm;
    font-size: 12pt;
    line-height: 1.5;
    font-family: '宋体', 'SimSun', serif;
    box-sizing: border-box;
  `
  document.body.appendChild(tempDiv)
  
  const pages: string[] = []
  let remainingHtml = htmlContent
  
  while (remainingHtml.trim()) {
    let left = 0
    let right = remainingHtml.length
    let splitPoint = 0
    
    while (left <= right) {
      const mid = Math.floor((left + right) / 2)
      tempDiv.innerHTML = remainingHtml.substring(0, mid)
      
      if (tempDiv.scrollHeight <= 1050) {
        splitPoint = mid
        left = mid + 1
      } else {
        right = mid - 1
      }
    }
    
    let finalSplit = splitPoint
    for (let i = splitPoint; i >= Math.max(0, splitPoint - 100); i--) {
      const c = remainingHtml[i]
      if (c === '\n' || c === '。' || c === '！' || c === '？' || c === '；' || c === '：' || 
          c === '</p>' || c === '</div>' || c === '</h1>' || c === '</h2>' || c === '</h3>') {
        finalSplit = i + 1
        break
      }
    }
    
    pages.push(remainingHtml.substring(0, finalSplit))
    remainingHtml = remainingHtml.substring(finalSplit)
  }
  
  document.body.removeChild(tempDiv)
  return pages
}

const setLessonData = (data: string) => {
  lessonData.value = data
  lessonPages.value = splitIntoPages(data)
}

const setPPTData = (data: string) => {
  pptData.value = data
  if (pptFrameRef.value) {
    pptFrameRef.value.innerHTML = ''
    const contentDiv = document.createElement('div')
    contentDiv.className = 'rendered-content'
    contentDiv.innerHTML = data
    pptFrameRef.value.appendChild(contentDiv)
  }
}

const setGameData = (data: string) => {
  gameData.value = data
  if (gameFrameRef.value) {
    gameFrameRef.value.innerHTML = ''
    const contentDiv = document.createElement('div')
    contentDiv.className = 'rendered-content'
    contentDiv.innerHTML = data
    gameFrameRef.value.appendChild(contentDiv)
  }
}

const scrollChatToBottom = async () => {
  await nextTick()
  if (chatMessagesRef.value) {
    chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
  }
}
const handlePDFPreview = (file: File) => {
  const url = URL.createObjectURL(file)
  activeTab.value = 'ppt' // 切换到 PPT 标签页展示 PDF
  nextTick(() => {
    if (pptFrameRef.value) {
      pptFrameRef.value.innerHTML = `
        <iframe src="${url}" width="100%" height="100%" 
          style="border:none; border-radius:16px;"></iframe>
      `
    }
  })
}

// 处理 Word 预览：利用你现有的 A4 分页逻辑 (splitIntoPages)
const handleWordPreview = async (file: File | Blob) => {
  await nextTick()
  
  // 获取 A4 纸容器（由于你有多页，我们默认渲染到第一页或创建一个总容器）
  const container = document.querySelector('.lesson-page-content') as HTMLElement
  
  if (container) {
    container.innerHTML = '' // 清空原有 AI 生成的内容
    try {
      await renderAsync(file, container, undefined, {
        className: "docx-inner", // 对应下方的 CSS
        ignoreWidth: true,       // 适配 A4 容器宽度
        debug: false
      })
      // 如果你想让 Word 也支持你的 A4 自动分页，可以在这里提取 HTML
      // setLessonData(container.innerHTML) 
    } catch (e) {
      console.error('Word 渲染失败:', e)
    }
  }
}
const showPdfNext = ref(true)
const downloadFileNext = ref(true)
const sendMessage = async () => {
  if ((!userInput.value.trim() && uploadedFiles.value.length === 0) || isAILoading.value) return
  
  if (isListening.value) {
    recognition?.stop()
  }

  const userMsg = userInput.value
  const currentFiles = [...uploadedFiles.value]
  
  chatMessages.value.push({ 
    role: 'user', 
    content: userMsg || (currentFiles.length ? `上传了 ${currentFiles.length} 个文件` : '')
  })
  userInput.value = ''
  uploadedFiles.value = []
  await scrollChatToBottom()

  isAILoading.value = true

  setTimeout(async () => {
    isAILoading.value = false
    
    let reply = `收到您的指令！已为您更新了关于“${userMsg}”的课件内容。`
    chatMessages.value.push({ role: 'assistant', content: reply })
    scrollChatToBottom()

    // ==============================================
    // ✅ 修复：PDF用iframe，DOCX用你原有渲染函数（不下载）
    // ==============================================
    if (showPdfNext.value) {
      // 第一次：显示 2.pdf → PPT标签
      activeTab.value = 'ppt'
      nextTick(() => {
        if (pptFrameRef.value) {
          pptFrameRef.value.innerHTML = `
            <iframe src="/2.pdf" width="100%" height="100%" style="border:none; border-radius:16px;"></iframe>
          `
        }
      })
    } else {
      // 第二次：显示 2.docx → 教案标签（用你原生方法，不下载！）
      activeTab.value = 'lesson' // 教案标签
      nextTick(async () => {
        const response = await fetch('/2.docx')
        const blob = await response.blob()
        const docxFile = new File([blob], '2.docx', { type: blob.type })
        await handleWordPreview(docxFile) // ✅ 你原来的渲染方法，不会下载
      })
    }

    // 切换状态
    showPdfNext.value = !showPdfNext.value

  }, 1000)
}
const downloadFile = async () => {
  let fileName, fileUrl

  if (downloadFileNext.value) {
    fileName = '课件.pdf'
    fileUrl = '/2.pdf' // 你的文件夹里的PDF
  } else {
    fileName = '教案.docx'
    fileUrl = '/2.docx' // 你的文件夹里的Word
  }
  // 下次切换
  downloadFileNext.value = !downloadFileNext.value

  try {
    // 下载文件
    const res = await fetch(fileUrl)
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = fileName
    a.click()
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error('下载失败：', err)
    alert('下载失败，请重试')
  }
}
defineExpose({ setPPTData, setLessonData, setGameData })

onMounted(async () => {
  // 1. 基础初始化
  const title = route.query.title as string
  if (title) pageTitle.value = title
  initSpeechRecognition()

  // 2. 核心：强制触发首次展示
  await nextTick()
  
  setTimeout(async () => {
    // --- 保持原有 PDF 展示逻辑 ---
    const defaultPdfUrl = '/1.pdf' 
    activeTab.value = 'ppt' // 确保初始标签依然是 PPT
    if (pptFrameRef.value) {
      pptFrameRef.value.innerHTML = `<iframe src="${defaultPdfUrl}" width="100%" height="100%" style="border:none;"></iframe>`
    }

    // --- 新增：初始化教案预览 (静默加载) ---
    try {
      // 假设你的默认教案文件也放在 public 目录下，名为 1.docx
      const response = await fetch('/1.docx')
      if (response.ok) {
        const blob = await response.blob()
        const defaultDocx = new File([blob], '1.docx', { type: blob.type })
        
        // 调用处理函数，内部会通过 setLessonData 填充 A4 纸
        // 注意：为避免干扰用户，请确保 handleWordPreview 内部没有强制切换 Tab 的语句
        await handleWordPreview(defaultDocx)
      }
    } catch (error) {
      console.error('初始化教案失败:', error)
    }
  }, 300)

  // 3. 显式添加欢迎消息
  chatMessages.value.push({
    role: 'assistant',
    content: '🚀 系统初始化完毕！PDF 课件与 Word 教案已同步加载就绪。'
  })
  scrollChatToBottom()
})

onUnmounted(() => {
  if (recognition && isListening.value) {
    recognition.stop()
  }
})
</script>

<style scoped>
:deep(.docx-wrapper) {
  background: transparent !important; /* 强制透明，不再显示灰色背景 */
  padding: 0 !important;
  display: block !important;
  box-shadow: none !important;        /* 预防万一，也加上阴影抹除 */
}

/* 2. 抹除内容容器的所有边框、阴影和多余边距 */
:deep(.docx-wrapper > section.docx) {
  width: 100% !important; 
  min-height: 100% !important;
  padding: 0 !important;             /* 设为0，由外层 A4 容器 padding 控制 */
  margin: 0 !important;
  
  /* 核心修复：彻底去掉灰色边框阴影 */
  box-shadow: none !important;        
  border: none !important;            
  outline: none !important;           /* 增加一行，防止 focus 时的蓝色边框 */
  
  background: white !important;       /* 确保背景是纯白 */
  box-sizing: border-box !important;
}

/* 3. 强制 Word 内部元素不再产生位移 */
:deep(.docx-inner) {
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
}

:deep(.docx-inner p) {
  margin-top: 0 !important;
  line-height: 1.6 !important; /* 优化阅读感 */
}

/* 4. 解决图片过大的问题 */
:deep(.docx-inner img) {
  max-width: 100% !important;
  height: auto !important;
}

/* 针对 PDF iframe 的适配 */
.white-frame iframe {
  background: #f8fafc;
}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.preview-layout {
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
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
}

.main-layout {
  flex: 1;
  display: flex;
  overflow: hidden;
  gap: 1px;
  background: rgba(0, 0, 0, 0.05);
}

.left-sidebar {
  width: 140px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.5);
  display: flex;
  flex-direction: column;
  padding: 20px 12px;
  gap: 12px;
}

.preview-tab-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: none;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
  color: #1e3c5c;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.preview-tab-btn .iconfont {
  font-size: 18px;
}

.preview-tab-btn:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateX(4px);
}

.preview-tab-btn.active {
  background: #7c9eff;
  color: white;
}

.preview-area {
  flex: 1;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(5px);
  padding: 20px;
  overflow-y: auto;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.preview-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.preview-header-tip {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(124, 158, 255, 0.3);
  flex-shrink: 0;
}

.preview-header-tip h3 {
  font-size: 18px;
  color: #1e3c5c;
  font-weight: 600;
  margin: 0;
}

.tip-badge {
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  background: rgba(124, 158, 255, 0.2);
  color: #7c9eff;
  font-weight: 500;
}

/* 白色背景板 - 统一用于PPT和游戏互动 */
.white-frame {
  flex: 1;
  width: 100%;
  max-width: 1000px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  overflow: auto;
  margin: 0 auto;
  min-height: 0;
}

/* 教案预览 - 标准A4纸比例 210mm × 297mm */
.lesson-canvas {
  flex: 1;
  overflow-y: auto;
  padding: 32px 24px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 8px;
}

.lesson-pages {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
  padding-bottom: 32px;
}

/* 标准A4纸尺寸 */
.lesson-page {
  width: 210mm;
  height: 297mm;
  background: white;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

/* 标准页边距：上下2.54cm，左右3.17cm */
.lesson-page-content {
  height: 100%;
  padding: 0cm 0cm;
  font-size: 12pt;
  line-height: 1.5;
  font-family: '宋体', 'SimSun', serif;
  outline: none;
  white-space: pre-wrap;
  word-wrap: break-word;
  word-break: break-word;
  overflow-y: auto;
  background: white;
  color: #1e293b;
}

.lesson-page-num {
  position: absolute;
  bottom: 1.5cm;
  right: 3.17cm;
  font-size: 10pt;
  color: #94a3b8;
  font-family: '宋体', 'SimSun', serif;
  pointer-events: none;
}

.rendered-content {
  width: 100%;
  height: auto;
  min-height: 100%;
  padding: 20px;
}

/* 右侧AI对话栏 */
.chat-sidebar {
  width: 340px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  border-left: 1px solid rgba(255, 255, 255, 0.5);
}

.chat-header {
  padding: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.chat-header .iconfont {
  font-size: 20px;
  color: #7c9eff;
}

.chat-header h3 {
  flex: 1;
  font-size: 16px;
  color: #1e3c5c;
  margin: 0;
  font-weight: 600;
}

.current-tab {
  font-size: 12px;
  padding: 4px 8px;
  background: rgba(124, 158, 255, 0.1);
  border-radius: 12px;
  color: #7c9eff;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chat-message {
  display: flex;
  gap: 12px;
}

.chat-message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.chat-message.user .message-avatar {
  background: #7c9eff;
}

.message-avatar .iconfont {
  font-size: 18px;
  color: white;
}

.message-content {
  max-width: 260px;
}

.message-text {
  background: white;
  padding: 8px 12px;
  border-radius: 12px;
  font-size: 13px;
  line-height: 1.5;
  color: #34495e;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.chat-message.user .message-text {
  background: #7c9eff;
  color: white;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 8px 12px;
  background: white;
  border-radius: 12px;
  width: fit-content;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background: #7c9eff;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

/* 输入区域 */
.chat-input-area {
  padding: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  flex-shrink: 0;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 24px;
  padding: 8px 12px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  gap: 4px;
}

.input-wrapper.listening {
  border-color: rgb(8, 130, 136);
  background: #f0f8ff;
}

.voice-icon-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: #7c9eff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.voice-icon-btn:hover:not(:disabled) {
  background: rgba(124, 158, 255, 0.1);
  color: #5f7fd9;
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

.chat-textarea {
  flex: 1;
  border: none;
  outline: none;
  resize: none;
  font-size: 13px;
  font-family: inherit;
  max-height: 80px;
  background: transparent;
  color: #34495e;
  min-width: 0;
}

.chat-textarea::placeholder {
  color: #94a3b8;
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
  border-radius: 24px;
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
  background: #7c9eff;
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
  font-size: 13px;
  color: rgb(8, 130, 136);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.attachment-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: #7c9eff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.attachment-btn:hover:not(:disabled) {
  background: rgba(124, 158, 255, 0.1);
  color: #5f7fd9;
}

.send-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #7c9eff;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  background: #5f7fd9;
  transform: scale(1.05);
}

.send-btn:disabled {
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
  font-size: 12px;
  color: #34495e;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.file-name {
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-size {
  font-size: 10px;
  color: #999;
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
}

.remove-file:hover {
  background: #ff5252;
  transform: scale(1.1);
}

.input-tip {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 8px;
  text-align: center;
}

@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.6; }
  30% { transform: translateY(-6px); opacity: 1; }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* 滚动条 */
.lesson-canvas::-webkit-scrollbar,
.chat-messages::-webkit-scrollbar,
.white-frame::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.lesson-canvas::-webkit-scrollbar-track,
.chat-messages::-webkit-scrollbar-track,
.white-frame::-webkit-scrollbar-track {
  background: rgba(124, 158, 255, 0.1);
  border-radius: 10px;
}

.lesson-canvas::-webkit-scrollbar-thumb,
.chat-messages::-webkit-scrollbar-thumb,
.white-frame::-webkit-scrollbar-thumb {
  background: #7c9eff;
  border-radius: 10px;
}

/* 响应式 */
@media (max-width: 1200px) {
  .lesson-page {
    width: 180mm;
    height: 254mm;
  }
  .white-frame {
    max-width: 800px;
  }
}

@media (max-width: 900px) {
  .chat-sidebar {
    width: 280px;
  }
  .lesson-page {
    width: 160mm;
    height: 226mm;
  }
}
/* 固定在左下角的下载按钮 */
.fixed-download-btn {
  position: fixed;
  left: 24px;
  bottom: 24px;
  z-index: 999;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 24px;
  font-size: 14px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transition: all 0.3s ease;
}
.fixed-download-btn:hover {
  background: #337ecc;
  transform: translateY(-2px);
}
</style>