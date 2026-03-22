<!-- PreviewPage.vue - 预览生成的PPT、教案、GIF等 -->
<template>
  <div class="preview-container">
    <!-- 顶部导航 -->
    <div class="preview-header">
      <div class="header-left">
        <button class="back-button" @click="goBack">
          <span class="iconfont icon-arrow-left"></span>
          <span>返回对话</span>
        </button>
      </div>
      <div class="header-center">
        <h1>生成的内容预览</h1>
      </div>
      <div class="header-right">
        <button class="download-btn" @click="downloadAll">
          <span class="iconfont icon-xiazai"></span>
          下载全部
        </button>
      </div>
    </div>

    <!-- 内容选项卡 -->
    <div class="content-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        class="tab-btn"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        <span :class="['iconfont', tab.icon]"></span>
        {{ tab.name }}
      </button>
    </div>

    <!-- PPT预览区域 -->
    <div v-if="activeTab === 'ppt'" class="ppt-preview">
      <div class="ppt-toolbar">
        <button class="ppt-tool-btn" @click="prevSlide" :disabled="currentSlideIndex === 0">
          <span class="iconfont icon-arrow-left"></span>
        </button>
        <span class="slide-info">{{ currentSlideIndex + 1 }} / {{ pptData.length }}</span>
        <button class="ppt-tool-btn" @click="nextSlide" :disabled="currentSlideIndex === pptData.length - 1">
          <span class="iconfont icon-arrow-right"></span>
        </button>
        <button class="ppt-tool-btn download" @click="downloadPPT">
          <span class="iconfont icon-xiazai"></span>
          下载PPT
        </button>
      </div>

      <div v-if="currentSlide" class="ppt-slide" :style="{ background: currentSlide.bgColor || '#ffffff' }">
        <div class="slide-content">
          <h1 class="slide-title">{{ currentSlide.title || '无标题' }}</h1>
          <div v-if="currentSlide.content" class="slide-text" v-html="currentSlide.content"></div>
          
          <div v-if="currentSlide.steps && currentSlide.steps.length" class="slide-steps">
            <div v-for="(step, idx) in currentSlide.steps" :key="idx" class="step-item">
              <span class="step-num">{{ idx + 1 }}</span>
              <span class="step-text">{{ step.title || '步骤' }}</span>
            </div>
          </div>

          <div v-if="currentSlide.image" class="slide-image" :style="{
            left: (currentSlide.image.x || 0) + 'px',
            top: (currentSlide.image.y || 0) + 'px',
            width: (currentSlide.image.width || 200) + 'px',
            height: (currentSlide.image.height || 150) + 'px'
          }">
            <img :src="currentSlide.image.url" alt="slide image" />
          </div>
        </div>
      </div>

      <div class="ppt-thumbnails">
        <div 
          v-for="(slide, index) in pptData" 
          :key="index"
          class="thumbnail"
          :class="{ active: currentSlideIndex === index }"
          @click="currentSlideIndex = index"
        >
          <div class="thumb-preview" :style="{ background: slide.bgColor || '#ffffff' }">
            <span class="thumb-title">{{ slide.title || '幻灯片' }}</span>
          </div>
          <span class="thumb-index">{{ index + 1 }}</span>
        </div>
      </div>
    </div>

    <!-- 教案预览区域 -->
    <div v-if="activeTab === 'lesson'" class="lesson-preview">
      <div class="lesson-actions">
        <button class="action-btn" @click="downloadLesson">
          <span class="iconfont icon-xiazai"></span>
          下载教案
        </button>
        <button class="action-btn" @click="printLesson">
          <span class="iconfont icon-dayin"></span>
          打印
        </button>
      </div>

      <div class="lesson-content" ref="lessonContent">
        <div class="lesson-header">
          <h1 class="lesson-title">{{ lessonData.title || '教案' }}</h1>
          <div class="lesson-meta">
            <span>科目：{{ lessonData.subject || '无' }}</span>
            <span>年级：{{ lessonData.grade || '无' }}</span>
            <span>课时：{{ lessonData.duration || '无' }}</span>
            <span>教师：{{ lessonData.teacher || '无' }}</span>
          </div>
        </div>

        <div class="lesson-section">
          <h2>教学目标</h2>
          <ul>
            <li v-for="(item, idx) in lessonData.objectives || []" :key="idx">{{ item }}</li>
          </ul>
        </div>

        <div class="lesson-section">
          <h2>教学重点</h2>
          <ul>
            <li v-for="(item, idx) in lessonData.keyPoints || []" :key="idx">{{ item }}</li>
          </ul>
        </div>

        <div class="lesson-section">
          <h2>教学难点</h2>
          <ul>
            <li v-for="(item, idx) in lessonData.difficultPoints || []" :key="idx">{{ item }}</li>
          </ul>
        </div>

        <div class="lesson-section">
          <h2>教学过程</h2>
          <div v-for="(step, idx) in lessonData.procedure || []" :key="idx" class="procedure-step">
            <h3>{{ step.title || '步骤' }}</h3>
            <p>{{ step.content || '' }}</p>
            <p v-if="step.duration" class="step-duration">⏱️ {{ step.duration }}分钟</p>
          </div>
        </div>

        <div class="lesson-section">
          <h2>板书设计</h2>
          <div class="blackboard" v-html="lessonData.blackboard || '无'"></div>
        </div>

        <div class="lesson-section">
          <h2>课后反思</h2>
          <p>{{ lessonData.reflection || '无' }}</p>
        </div>
      </div>
    </div>

    <!-- GIF预览区域 -->
    <div v-if="activeTab === 'gif'" class="gif-preview">
      <div class="gif-header">
        <h2>{{ gifData.title || '教学GIF' }}</h2>
        <button class="download-gif-btn" @click="downloadGIF">
          <span class="iconfont icon-xiazai"></span>
          下载GIF
        </button>
      </div>

      <div class="gif-player">
        <img :src="gifData.url || ''" :alt="gifData.title || 'GIF动画'" />
        <div class="gif-controls">
          <button class="gif-control-btn" @click="togglePlay">
            <span class="iconfont" :class="isPlaying ? 'icon-zanting' : 'icon-bofang'"></span>
          </button>
          <button class="gif-control-btn" @click="resetGIF">
            <span class="iconfont icon-zhongzhi"></span>
          </button>
          <span class="gif-speed">速度 ×{{ playbackSpeed }}</span>
          <input 
            type="range" 
            min="0.5" 
            max="2" 
            step="0.1" 
            v-model="playbackSpeed"
            class="speed-slider"
          />
        </div>
      </div>

      <div class="gif-description">
        <h3>动画说明</h3>
        <p>{{ gifData.description || '暂无说明' }}</p>
      </div>

      <div class="gif-tags">
        <span v-for="tag in gifData.tags || []" :key="tag" class="gif-tag">{{ tag }}</span>
      </div>
    </div>

    <!-- 创新内容预览区域 -->
    <div v-if="activeTab === 'innovation'" class="innovation-preview">
      <h2>创新教学内容</h2>
      <div class="innovation-grid">
        <div v-for="item in innovationData" :key="item.id" class="innovation-card">
          <div class="innovation-icon">
            <span :class="['iconfont', item.icon || 'icon-chuangxin']"></span>
          </div>
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <button class="view-btn" @click="viewInnovation(item)">查看详情</button>
        </div>
      </div>
    </div>

    <!-- 帮助按钮 -->
    <div class="help-button" @click="handleHelp">?</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

interface Slide {
  id: number
  title: string
  content?: string
  bgColor?: string
  steps?: Array<{ title: string }>
  image?: {
    url: string
    x?: number
    y?: number
    width?: number
    height?: number
  } | null
}

interface LessonData {
  title?: string
  subject?: string
  grade?: string
  duration?: string
  teacher?: string
  objectives?: string[]
  keyPoints?: string[]
  difficultPoints?: string[]
  procedure?: Array<{
    title?: string
    content?: string
    duration?: number
  }>
  blackboard?: string
  reflection?: string
}

interface GifData {
  title?: string
  url?: string
  description?: string
  tags?: string[]
}

interface InnovationItem {
  id: number
  title: string
  icon?: string
  description: string
  url?: string
}

const router = useRouter()
const route = useRoute()
const activeTab = ref('ppt')
const currentSlideIndex = ref(0)
const isPlaying = ref(true)
const playbackSpeed = ref(1)
const lessonContent = ref<HTMLElement | null>(null)

const tabs = [
  { id: 'ppt', name: 'PPT课件', icon: 'icon-PPT' },
  { id: 'lesson', name: '教案', icon: 'icon-wendang' },
  { id: 'gif', name: '教学GIF', icon: 'icon-donghua' },
  { id: 'innovation', name: '创新内容', icon: 'icon-chuangxin' }
]

const pptData = ref<Slide[]>([
  {
    id: 1,
    title: '分数的初步认识',
    content: '<p>本节课我们将学习分数的基本概念和表示方法。</p>',
    bgColor: '#ffffff',
    steps: [
      { title: '什么是分数' },
      { title: '分数的读写' },
      { title: '分数的比较' }
    ],
    image: null
  },
  {
    id: 2,
    title: '分数的定义',
    content: '<p>把单位"1"平均分成若干份，表示这样一份或几份的数叫做分数。</p>',
    bgColor: '#f8f9fa',
    steps: [],
    image: {
      url: 'https://via.placeholder.com/300x200',
      x: 600,
      y: 200,
      width: 300,
      height: 200
    }
  },
  {
    id: 3,
    title: '分数的读写',
    content: '<p>分数由分子、分数线和分母三部分组成。</p><p>读作：几分之几</p>',
    bgColor: '#f1f5f9',
    steps: [],
    image: null
  }
])

const lessonData = ref<LessonData>({
  title: '分数的初步认识',
  subject: '数学',
  grade: '三年级',
  duration: '40分钟',
  teacher: '张老师',
  objectives: [
    '理解分数的概念，知道分数各部分的名称',
    '能正确读写简单的分数',
    '能用分数表示实际生活中的问题'
  ],
  keyPoints: [
    '分数的概念和读写方法',
    '理解单位"1"的含义'
  ],
  difficultPoints: [
    '理解平均分的概念',
    '分数各部分表示的意义'
  ],
  procedure: [
    {
      title: '导入新课（5分钟）',
      content: '通过分蛋糕的情境导入，引出分数的概念。',
      duration: 5
    },
    {
      title: '新知讲授（20分钟）',
      content: '讲解分数的定义、读写方法和基本性质。',
      duration: 20
    },
    {
      title: '巩固练习（10分钟）',
      content: '通过练习题巩固所学知识。',
      duration: 10
    },
    {
      title: '课堂小结（5分钟）',
      content: '总结本节课的重点内容。',
      duration: 5
    }
  ],
  blackboard: `
    <div class="blackboard-content">
      <div>分数的初步认识</div>
      <div>1/2 = 二分之一</div>
      <div>分子 / 分母</div>
    </div>
  `,
  reflection: '学生对分数的概念理解较好，但在读写时容易混淆分子和分母的位置，需要加强练习。'
})

const gifData = ref<GifData>({
  title: '分数的概念演示',
  url: 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2FybjZ6eHl6bGJ6dGZ4eHl6bGJ6dGZ4eHl6bGJ6dGZ4eHl6bGJ6dA/giphy.gif',
  description: '这个动画展示了如何将一个圆形平均分成4份，取其中的一份就是1/4。',
  tags: ['分数', '数学', '动画教学', '小学']
})

const innovationData = ref<InnovationItem[]>([
  {
    id: 1,
    title: '分数互动游戏',
    icon: 'icon-youxi',
    description: '通过游戏的方式让学生理解分数的大小比较',
    url: '#'
  },
  {
    id: 2,
    title: '分数思维导图',
    icon: 'icon-siwei',
    description: '用思维导图整理分数的知识点',
    url: '#'
  },
  {
    id: 3,
    title: '分数微课视频',
    icon: 'icon-shipin',
    description: '5分钟微课视频讲解分数的应用',
    url: '#'
  }
])

const currentSlide = computed<Slide | undefined>(() => {
  return pptData.value[currentSlideIndex.value]
})

// 返回对话 - 修改为跳转到 /chat
const goBack = () => {
  router.push('/chat')
}

const prevSlide = () => {
  if (currentSlideIndex.value > 0) {
    currentSlideIndex.value--
  }
}

const nextSlide = () => {
  if (currentSlideIndex.value < pptData.value.length - 1) {
    currentSlideIndex.value++
  }
}

const downloadPPT = () => {
  alert('正在下载PPT课件...')
}

const downloadLesson = () => {
  alert('正在下载教案...')
}

const printLesson = () => {
  if (lessonContent.value) {
    const printWindow = window.open('', '_blank')
    if (printWindow) {
      printWindow.document.write(`
        <html>
          <head>
            <title>${lessonData.value.title || '教案'}</title>
            <style>
              body { font-family: Arial; padding: 40px; }
              h1 { color: #1e3c5c; }
              .lesson-meta { margin: 20px 0; color: #666; }
              h2 { color: #0ba7af; border-bottom: 2px solid #0ba7af; padding-bottom: 8px; }
              ul { list-style-type: disc; }
              .procedure-step { margin-bottom: 20px; }
            </style>
          </head>
          <body>
            ${lessonContent.value.innerHTML}
          </body>
        </html>
      `)
      printWindow.document.close()
      printWindow.print()
    }
  }
}

const downloadGIF = () => {
  alert('正在下载GIF动画...')
}

const togglePlay = () => {
  isPlaying.value = !isPlaying.value
  const gifImg = document.querySelector('.gif-player img') as HTMLImageElement | null
  if (gifImg) {
    if (isPlaying.value) {
      gifImg.src = gifImg.src
    }
  }
}

const resetGIF = () => {
  const gifImg = document.querySelector('.gif-player img') as HTMLImageElement | null
  if (gifImg && gifData.value.url) {
    gifImg.src = gifData.value.url
    isPlaying.value = true
  }
}

const viewInnovation = (item: InnovationItem) => {
  alert(`查看详情：${item.title}`)
}

const downloadAll = () => {
  alert('正在打包下载所有内容...')
}

const handleHelp = () => {
  alert('预览页面使用说明：\n1. 点击选项卡切换不同类型的内容\n2. PPT模式下可通过缩略图或箭头切换页面\n3. 教案可下载或打印\n4. GIF可控制播放速度')
}

onMounted(() => {
  const tab = route.query.tab as string
  if (tab && ['ppt', 'lesson', 'gif', 'innovation'].includes(tab)) {
    activeTab.value = tab
  }
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.preview-container {
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
  flex-direction: column;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
}

/* 头部导航 */
.preview-header {
  height: 70px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: none;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 20px;
  color: #34495e;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.back-button:hover {
  background: white;
  color: rgb(11, 167, 175);
  transform: scale(1.02);
}

.header-center h1 {
  font-size: 20px;
  color: #1e3c5c;
  font-weight: 600;
}

.download-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  border: none;
  background: rgb(11, 167, 175);
  border-radius: 20px;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.download-btn:hover {
  background: rgb(8, 130, 136);
  transform: scale(1.02);
}

/* 选项卡 */
.content-tabs {
  display: flex;
  gap: 8px;
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(5px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  border: none;
  background: white;
  border-radius: 30px;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.tab-btn:hover {
  background: #f0f8ff;
  transform: translateY(-2px);
}

.tab-btn.active {
  background: rgb(11, 167, 175);
  color: white;
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.2);
}

.tab-btn .iconfont {
  font-size: 18px;
}

/* PPT预览区域 */
.ppt-preview {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 24px;
  overflow: hidden;
}

.ppt-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  background: white;
  padding: 12px 20px;
  border-radius: 40px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  width: fit-content;
  margin: 0 auto 20px;
}

.ppt-tool-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #f0f0f0;
  color: #34495e;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.ppt-tool-btn:hover:not(:disabled) {
  background: rgb(11, 167, 175);
  color: white;
  transform: scale(1.05);
}

.ppt-tool-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.ppt-tool-btn.download {
  width: auto;
  padding: 0 16px;
  border-radius: 20px;
  gap: 8px;
  background: rgb(11, 167, 175);
  color: white;
}

.slide-info {
  font-size: 14px;
  color: #34495e;
  font-weight: 500;
}

.ppt-slide {
  flex: 1;
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;
  background: white;
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
  overflow: hidden;
  position: relative;
  aspect-ratio: 16 / 9;
}

.slide-content {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.slide-title {
  font-size: 42px;
  color: #1e3c5c;
  font-weight: 700;
  margin: 0;
}

.slide-text {
  font-size: 18px;
  color: #34495e;
  line-height: 1.6;
}

.slide-steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.step-num {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 16px;
}

.step-text {
  font-size: 18px;
  color: #34495e;
}

.slide-image {
  position: absolute;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.slide-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ppt-thumbnails {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  padding: 12px;
  background: rgba(255,255,255,0.5);
  border-radius: 12px;
  overflow-x: auto;
}

.thumbnail {
  cursor: pointer;
  flex-shrink: 0;
  width: 120px;
  transition: all 0.2s ease;
}

.thumbnail.active {
  transform: scale(1.05);
}

.thumb-preview {
  width: 100%;
  height: 68px;
  border-radius: 8px;
  background: white;
  border: 2px solid transparent;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
}

.thumbnail.active .thumb-preview {
  border-color: rgb(11, 167, 175);
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.2);
}

.thumb-title {
  font-size: 10px;
  color: #34495e;
  text-align: center;
  word-break: break-word;
}

.thumb-index {
  display: block;
  text-align: center;
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}

/* 教案预览区域 */
.lesson-preview {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.lesson-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  justify-content: flex-end;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  border: none;
  background: white;
  border-radius: 20px;
  color: #34495e;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.action-btn:hover {
  background: rgb(11, 167, 175);
  color: white;
  transform: scale(1.02);
}

.lesson-content {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.lesson-header {
  margin-bottom: 30px;
  text-align: center;
}

.lesson-title {
  font-size: 32px;
  color: #1e3c5c;
  margin-bottom: 16px;
}

.lesson-meta {
  display: flex;
  justify-content: center;
  gap: 24px;
  color: #666;
  font-size: 14px;
  flex-wrap: wrap;
}

.lesson-section {
  margin-bottom: 30px;
}

.lesson-section h2 {
  font-size: 20px;
  color: rgb(11, 167, 175);
  border-bottom: 2px solid rgba(11, 167, 175, 0.2);
  padding-bottom: 8px;
  margin-bottom: 16px;
}

.lesson-section ul {
  list-style-type: disc;
  padding-left: 20px;
}

.lesson-section li {
  margin-bottom: 8px;
  color: #34495e;
  line-height: 1.6;
}

.procedure-step {
  margin-bottom: 20px;
}

.procedure-step h3 {
  font-size: 16px;
  color: #1e3c5c;
  margin-bottom: 8px;
}

.step-duration {
  color: #ff9800;
  font-size: 14px;
  margin-top: 4px;
}

.blackboard {
  background: #1e3c5c;
  color: white;
  padding: 20px;
  border-radius: 12px;
  font-family: monospace;
  font-size: 16px;
  line-height: 2;
}

/* GIF预览区域 */
.gif-preview {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.gif-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 800px;
  margin: 0 auto 24px;
}

.gif-header h2 {
  font-size: 24px;
  color: #1e3c5c;
}

.download-gif-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  border: none;
  background: rgb(11, 167, 175);
  border-radius: 20px;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.download-gif-btn:hover {
  background: rgb(8, 130, 136);
  transform: scale(1.02);
}

.gif-player {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.gif-player img {
  width: 100%;
  border-radius: 12px;
  margin-bottom: 20px;
}

.gif-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.gif-control-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #f0f0f0;
  color: #34495e;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.gif-control-btn:hover {
  background: rgb(11, 167, 175);
  color: white;
  transform: scale(1.05);
}

.gif-speed {
  font-size: 14px;
  color: #666;
  margin-left: 8px;
}

.speed-slider {
  width: 120px;
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  outline: none;
  -webkit-appearance: none;
}

.speed-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  background: rgb(11, 167, 175);
  border-radius: 50%;
  cursor: pointer;
}

.gif-description {
  max-width: 800px;
  margin: 24px auto 0;
  padding: 20px;
  background: white;
  border-radius: 12px;
}

.gif-description h3 {
  font-size: 16px;
  color: #1e3c5c;
  margin-bottom: 8px;
}

.gif-description p {
  color: #666;
  line-height: 1.6;
}

.gif-tags {
  max-width: 800px;
  margin: 16px auto 0;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.gif-tag {
  padding: 4px 12px;
  background: rgba(11, 167, 175, 0.1);
  border-radius: 16px;
  color: rgb(11, 167, 175);
  font-size: 12px;
}

/* 创新内容区域 */
.innovation-preview {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.innovation-preview h2 {
  font-size: 24px;
  color: #1e3c5c;
  margin-bottom: 24px;
  text-align: center;
}

.innovation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.innovation-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
  cursor: pointer;
}

.innovation-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(11, 167, 175, 0.15);
}

.innovation-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.innovation-icon .iconfont {
  font-size: 32px;
  color: white;
}

.innovation-card h3 {
  font-size: 18px;
  color: #1e3c5c;
  margin-bottom: 8px;
  font-weight: 600;
}

.innovation-card p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
}

.view-btn {
  padding: 6px 16px;
  border: none;
  background: rgba(11, 167, 175, 0.1);
  border-radius: 20px;
  color: rgb(11, 167, 175);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 13px;
}

.view-btn:hover {
  background: rgb(11, 167, 175);
  color: white;
}

/* 帮助按钮 */
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

/* 滚动条样式 */
.lesson-preview::-webkit-scrollbar,
.ppt-thumbnails::-webkit-scrollbar,
.innovation-preview::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.lesson-preview::-webkit-scrollbar-track,
.ppt-thumbnails::-webkit-scrollbar-track,
.innovation-preview::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

.lesson-preview::-webkit-scrollbar-thumb,
.ppt-thumbnails::-webkit-scrollbar-thumb,
.innovation-preview::-webkit-scrollbar-thumb {
  background: rgba(11, 167, 175, 0.3);
  border-radius: 10px;
}

.lesson-preview::-webkit-scrollbar-thumb:hover,
.ppt-thumbnails::-webkit-scrollbar-thumb:hover,
.innovation-preview::-webkit-scrollbar-thumb:hover {
  background: rgba(11, 167, 175, 0.5);
}

/* 响应式 */
@media (max-width: 768px) {
  .preview-header {
    padding: 0 16px;
  }
  
  .header-center h1 {
    font-size: 16px;
  }
  
  .tab-btn {
    padding: 8px 16px;
    font-size: 13px;
  }
  
  .lesson-meta {
    flex-direction: column;
    gap: 8px;
  }
  
  .ppt-slide {
    margin: 0 -24px;
    border-radius: 0;
  }
}
</style>