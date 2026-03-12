<template>
  <div class="outline-page-container">
    <!-- 顶部导航栏 -->
    <div class="outline-header">
      <div class="header-left">
        <button class="back-button outline-button icon-button" @click="handleBack">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <span class="header-title">返回</span>
      </div>
      
      <div class="header-center">
        <span class="generate-tag">生成</span>
        <span class="prompt-text">{{ promptText }}</span>
      </div>
      
      <div class="header-right">
        <span class="card-count">{{ currentCardCount }}张卡片</span>
        <span class="separator">|</span>
        <span class="language">{{ selectedLanguage }}</span>
      </div>
    </div>

    <!-- 主要内容区域 - 滚动 -->
    <div class="outline-main" ref="outlineMain">
      <!-- 大纲标题 -->
      <div class="outline-title-section">
        <h1 class="outline-title">{{ outlineTitle }}</h1>
        <span class="outline-subtitle">{{ outlineSubtitle }}</span>
      </div>

      <!-- 大纲内容卡片 -->
      <div class="outline-cards">
        <div v-for="(section, index) in outlineSections" :key="index" class="outline-card">
          <!-- 如果是标题卡片 -->
          <div v-if="section.type === 'title'" class="card-title-section">
            <div class="title-number">{{ section.number }}</div>
            <h2 class="title-content">{{ section.content }}</h2>
          </div>
          
          <!-- 如果是内容卡片 -->
          <div v-else class="card-content-section">
            <div class="content-number">{{ section.number }}</div>
            <div class="content-wrapper">
              <h3 class="content-title">{{ section.title }}</h3>
              <ul class="content-list">
                <li v-for="(item, idx) in section.items" :key="idx">
                  <span class="bullet">·</span>
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部添加卡片区域 -->
      <div class="add-card-section">
        <button class="add-card-button">
          <span class="iconfont icon-tianjia"></span>
          添加卡片
        </button>
      </div>
    </div>

    <!-- 底部操作栏 -->
    <div class="outline-footer">
      <div class="footer-left">
        <div class="custom-input">
          <span class="iconfont icon-bi"></span>
          <input 
            type="text" 
            v-model="customText" 
            placeholder="键入生成卡片分隔符"
          />
          <span class="char-count">{{ customText.length }}/50000</span>
        </div>
      </div>
      
      <div class="footer-center">
        <div class="action-tabs">
          <button class="tab-button active">自定义您的gamma</button>
          <button class="tab-button">三文本内容</button>
          <button class="tab-button">每张卡片的字数</button>
        </div>
        
        <div class="style-options">
          <button class="style-button" :class="{ active: cardStyle === '简约' }" @click="cardStyle = '简约'">简约</button>
          <button class="style-button" :class="{ active: cardStyle === '简洁' }" @click="cardStyle = '简洁'">简洁</button>
          <button class="style-button" :class="{ active: cardStyle === '详细' }" @click="cardStyle = '详细'">详细</button>
          <button class="style-button" :class="{ active: cardStyle === '宽泛' }" @click="cardStyle = '宽泛'">宽泛</button>
        </div>
        
        <div class="visual-theme">
          <span class="theme-label">视觉效果</span>
          <span class="theme-value">主题</span>
          <span class="iconfont icon-xiala"></span>
        </div>
      </div>
      
      <div class="footer-right">
        <div class="theme-suggestions">
          <span class="suggestions-label">使用以下热门主题之一或</span>
          <button class="more-link">查看更多</button>
        </div>
        
        <div class="theme-icons">
          <div class="theme-icon-item">
            <div class="icon-demo title-demo">Title</div>
            <div class="icon-demo body-demo">Body&link</div>
          </div>
          <div class="theme-icon-item">
            <div class="icon-demo title-demo">Title</div>
            <div class="icon-demo body-demo">Body&link</div>
          </div>
          <div class="theme-icon-item">
            <div class="icon-demo title-demo">Title</div>
            <div class="icon-demo body-demo">Body&link</div>
          </div>
        </div>
        
        <div class="footer-actions">
          <span class="points">400积分</span>
          <span class="total-cards">总共{{ totalCardCount }}张卡片</span>
          <button class="generate-button" @click="handleGenerate">生成</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 接收从生成页面传递的参数
const promptText = ref(route.query.prompt || '大数据教材')
const currentCardCount = ref(route.query.cardCount || '10')
const selectedLanguage = ref(route.query.language || '简体中文')
const totalCardCount = ref(10)

// 大纲数据
const outlineTitle = ref('大数据教材精华：开启数据时代的大门')
const outlineSubtitle = ref('什么是大数据？')

const outlineSections = ref([
  {
    type: 'content',
    number: '·',
    title: '数据量巨大，预计2020年全球数据量达35ZB，约是2010年的30倍',
    items: [
      '数据类型多样，90%为非结构化数据，如文本、图片、视频等',
      '处理速度快，实时决策成为可能'
    ]
  },
  {
    type: 'title',
    number: '·',
    content: '大数据的三大特征（3V）'
  },
  {
    type: 'content',
    number: '·',
    title: 'Volume（海量）：数据规模爆炸式增长',
    items: []
  },
  {
    type: 'content',
    number: '·',
    title: 'Velocity（高速）：数据生成与处理速度极快',
    items: []
  },
  {
    type: 'content',
    number: '·',
    title: 'Variety（多样）：结构化、半结构化与非结构化数据共存',
    items: []
  },
  {
    type: 'title',
    number: '·',
    content: '大数据技术架构核心'
  },
  {
    type: 'content',
    number: '·',
    title: 'Hadoop生态系统：分布式存储（HDFS）与计算（MapReduce）',
    items: []
  },
  {
    type: 'content',
    number: '·',
    title: 'NoSQL数据库：灵活存储非结构化数据，如HBase',
    items: []
  }
])

const customText = ref('')
const cardStyle = ref('简约')

const handleBack = () => {
  router.back()
}

const handleGenerate = () => {
  // 生成最终PPT，跳转到编辑器页面
  router.push('/editor')
}

// 滚动处理
const outlineMain = ref<HTMLElement | null>(null)

onMounted(() => {
  console.log('接收到的参数:', route.query)
})
</script>

<style scoped>
.outline-page-container {
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
}

/* 顶部导航栏 */
.outline-header {
  height: 60px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.back-button {
  background: white;
  border: none;
  border-radius: 6px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #34495e;
}

.header-title {
  font-size: 14px;
  color: #34495e;
}

.header-center {
  display: flex;
  align-items: center;
  gap: 8px;
}

.generate-tag {
  background: rgb(11, 167, 175);
  color: white;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 14px;
}

.prompt-text {
  font-size: 16px;
  color: #2c3e50;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #34495e;
}

.separator {
  color: #ddd;
}

/* 主要内容区域 */
.outline-main {
  flex: 1;
  overflow-y: auto;
  padding: 24px 32px;
}

.outline-title-section {
  margin-bottom: 32px;
}

.outline-title {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 8px;
  font-weight: 600;
}

.outline-subtitle {
  font-size: 18px;
  color: #34495e;
  font-weight: 500;
}

/* 大纲卡片 */
.outline-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.outline-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.outline-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-title-section {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.title-number, .content-number {
  font-size: 20px;
  color: rgb(11, 167, 175);
  font-weight: bold;
  min-width: 20px;
}

.title-content {
  font-size: 20px;
  color: #2c3e50;
  font-weight: 600;
}

.card-content-section {
  display: flex;
  gap: 12px;
}

.content-wrapper {
  flex: 1;
}

.content-title {
  font-size: 16px;
  color: #34495e;
  margin-bottom: 8px;
  font-weight: 500;
}

.content-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.content-list li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
  line-height: 1.6;
}

.bullet {
  color: #999;
  font-size: 14px;
}

/* 添加卡片区域 */
.add-card-section {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}

.add-card-button {
  background: white;
  border: 1px dashed #ccc;
  border-radius: 24px;
  padding: 10px 24px;
  font-size: 14px;
  color: #34495e;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.add-card-button:hover {
  border-color: rgb(11, 167, 175);
  color: rgb(11, 167, 175);
}

/* 底部操作栏 */
.outline-footer {
  height: 180px;
  background: white;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  padding: 16px 24px;
  display: flex;
  flex-direction: column;
  z-index: 10;
}

.footer-left {
  margin-bottom: 12px;
}

.custom-input {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f5f5f5;
  border-radius: 20px;
  padding: 8px 16px;
  width: fit-content;
}

.custom-input input {
  border: none;
  background: transparent;
  outline: none;
  font-size: 14px;
  color: #34495e;
  width: 200px;
}

.custom-input input::placeholder {
  color: #999;
}

.char-count {
  font-size: 12px;
  color: #999;
}

.footer-center {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 12px;
}

.action-tabs {
  display: flex;
  gap: 8px;
}

.tab-button {
  background: none;
  border: none;
  padding: 6px 12px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  border-radius: 16px;
}

.tab-button.active {
  background: #e8f4f5;
  color: rgb(11, 167, 175);
}

.style-options {
  display: flex;
  gap: 8px;
}

.style-button {
  background: #f5f5f5;
  border: none;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
}

.style-button.active {
  background: rgb(11, 167, 175);
  color: white;
}

.visual-theme {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #34495e;
}

.theme-value {
  color: rgb(11, 167, 175);
  font-weight: 500;
}

.footer-right {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.theme-suggestions {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #666;
}

.more-link {
  background: none;
  border: none;
  color: rgb(11, 167, 175);
  cursor: pointer;
  font-size: 13px;
}

.theme-icons {
  display: flex;
  gap: 16px;
}

.theme-icon-item {
  display: flex;
  gap: 4px;
  font-size: 12px;
}

.icon-demo {
  padding: 2px 4px;
  border-radius: 2px;
}

.title-demo {
  background: #f0f0f0;
  color: #333;
}

.body-demo {
  background: #e0e0e0;
  color: #666;
}

.footer-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.points {
  color: #f39c12;
  font-weight: 500;
  font-size: 14px;
}

.total-cards {
  font-size: 14px;
  color: #34495e;
}

.generate-button {
  background: rgb(11, 167, 175);
  color: white;
  border: none;
  padding: 8px 24px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.generate-button:hover {
  background: rgb(8, 130, 136);
  transform: scale(1.02);
}
</style>