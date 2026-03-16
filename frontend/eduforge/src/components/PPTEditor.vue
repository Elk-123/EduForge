<!-- src/components/PPTEditor.vue -->
<template>
  <div class="ppt-editor">
    <!-- 左侧缩略图 -->
    <Sidebar
      :slides="slides"
      :current-slide="currentSlide"
      @select-slide="selectSlide"
      @add-slide="addSlide"
    />

    <!-- 中间编辑画布 -->
    <Canvas
      :current-slide="currentSlide"
      @update-field="updateField"
      @update-step="updateStep"
    />

    <!-- 右侧工具栏和配图面板 -->
    <div class="right-panel">
      <!-- 竖排工具栏 -->
      <Toolbar
        @add-step="addStep"
        @del-step="delStep"
        @change-font="changeFontSize"
        @change-bg="changeBg"
        @search="search"
        @add-image="addImage"
        @change-layout="changeLayout"
        @preview="preview"
        @save="save"
        @undo="undo"
        @redo="redo"
        @export="exportPPT"
      />
      
      <!-- 配图预览面板 -->
      <SideEditor 
        :current-slide="currentSlide" 
        @update:image="updateImage"
      />
    </div>

    <!-- 搜索面板 -->
    <SearchPanel 
      v-if="showSearch"
      :slides="slides"
      @close="showSearch = false"
      @navigate="goToSlide"
    />

    <!-- 预览弹窗 -->
    <div v-if="showPreview" class="preview-modal" @click.self="showPreview = false">
      <div class="preview-content">
        <div class="preview-header">
          <h3>PPT预览</h3>
          <button class="close-preview" @click="showPreview = false">×</button>
        </div>
        <div class="preview-slides">
          <div 
            v-for="(slide, index) in slides" 
            :key="slide.id"
            class="preview-slide"
            :style="{ background: slide.bgColor }"
          >
            <h2>{{ slide.title || '无标题' }}</h2>
            <p>{{ slide.content || '无内容' }}</p>
            <div class="preview-steps" v-if="slide.steps?.length">
              <div v-for="step in slide.steps" :key="step.id" class="preview-step">
                <span class="preview-step-num">{{ step.id }}</span>
                <span>{{ step.title }}</span>
              </div>
            </div>
            <div class="preview-index">{{ index + 1 }}/{{ slides.length }}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="action-buttons" style="position: fixed; bottom: 30px; right: 30px; display: flex; gap: 10px; z-index: 1000;">
  <button 
    @click="handleGeneratePPT" 
    style="background: #ff6b6b; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px;"
  >
    ✨ 生成PPT
  </button>
  
  <a 
    v-if="downloadUrl" 
    :href="downloadUrl" 
    target="_blank"
    style="background: rgb(11, 167, 175); color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-size: 14px;"
  >
    下载PPT
  </a>
</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './Sidebar.vue'
import Canvas from './Canvas.vue'
import Toolbar from './Toolbar.vue'
import SideEditor from './SideEditor.vue'
import SearchPanel from './SearchPanel.vue'
import axios from 'axios'
const route = useRoute()
const slides = ref([])
const currentSlide = ref(null)
const fontSize = ref(16)
const showPreview = ref(false)
const showSearch = ref(false)
const history = ref([])
const API_BASE_URL = 'http://localhost:8000/api/v1'
const downloadUrl = ref('')  // 只存下载链接
const historyIndex = ref(-1)


// 初始化数据
onMounted(() => {
  slides.value = [
    {
      id: 1,
      title: '点击编辑标题',
      content: '点击编辑内容',
      bgColor: '#ffffff',
      image: null,
      steps: [
        { id: 1, title: '第一步', desc: '这是第一步的描述' },
        { id: 2, title: '第二步', desc: '这是第二步的描述' }
      ]
    }
  ]
  currentSlide.value = slides.value[0]
  saveToHistory()
})

// 保存到历史记录
const saveToHistory = () => {
  const snapshot = JSON.parse(JSON.stringify(slides.value))
  history.value = history.value.slice(0, historyIndex.value + 1)
  history.value.push(snapshot)
  historyIndex.value = history.value.length - 1
}

// 选择幻灯片
const selectSlide = (slide) => { 
  currentSlide.value = slide 
}

// 添加幻灯片
const addSlide = () => {
  const newSlide = { 
    id: Date.now(), 
    title: '新页面', 
    content: '点击编辑内容', 
    bgColor: '#ffffff', 
    image: null, 
    steps: [] 
  }
  slides.value.push(newSlide)
  currentSlide.value = newSlide
  saveToHistory()
  alert('新页面添加成功！')
}

// 更新字段
const updateField = (field, value) => {
  if (currentSlide.value) {
    currentSlide.value[field] = value
    saveToHistory()
  }
}

// 更新步骤
const updateStep = (step, field, value) => {
  if (step) {
    step[field] = value
    saveToHistory()
  }
}

// 添加步骤
const addStep = () => {
  if (!currentSlide.value?.steps) return
  const newId = Math.max(...currentSlide.value.steps.map(s => s.id), 0) + 1
  currentSlide.value.steps.push({ 
    id: newId, 
    title: '新步骤', 
    desc: '点击编辑步骤描述' 
  })
  saveToHistory()
  alert(`步骤 ${newId} 添加成功！`)
}

// 删除步骤
const delStep = () => {
  if (currentSlide.value?.steps?.length) {
    const lastStep = currentSlide.value.steps[currentSlide.value.steps.length - 1]
    currentSlide.value.steps.pop()
    saveToHistory()
    alert(`步骤 ${lastStep.id} 已删除`)
  } else {
    alert('没有步骤可以删除')
  }
}

// 改变字体大小 - 实时渲染
const changeFontSize = (size) => {
  fontSize.value = size
  
  // 获取当前幻灯片的DOM元素并修改样式
  const slideElement = document.querySelector('.slide')
  if (slideElement) {
    const titleElement = slideElement.querySelector('.edit-title')
    const contentElement = slideElement.querySelector('.edit-content')
    const stepElements = slideElement.querySelectorAll('.step-title, .step-desc')
    
    if (titleElement) {
      titleElement.style.fontSize = (size * 2.5) + 'px'
    }
    if (contentElement) {
      contentElement.style.fontSize = size + 'px'
    }
    
    stepElements.forEach(el => {
      if (el.classList.contains('step-title')) {
        el.style.fontSize = (size * 1.2) + 'px'
      } else {
        el.style.fontSize = (size * 0.9) + 'px'
      }
    })
  }
  
  alert(`字体大小已实时调整为 ${size}px`)
}

// 改变背景色 - 实时渲染
const changeBg = (index) => {
  if (!currentSlide.value) return
  
  const colors = [
    '#ffffff', '#f8f9fa', '#f1f5f9', '#fef9e7', 
    '#e6f7ff', '#f0f9f1', '#fdf2f8', '#f3e8ff'
  ]
  
  currentSlide.value.bgColor = colors[index]
  saveToHistory()
  
  // 实时修改DOM背景色
  const slideElement = document.querySelector('.slide')
  if (slideElement) {
    slideElement.style.backgroundColor = colors[index]
  }
  
  alert(`背景色已实时更换为 ${index + 1}号色`)
}

// 布局切换 - 实时渲染
const changeLayout = (layout) => {
  const slideElement = document.querySelector('.slide')
  if (!slideElement) return
  
  let width, height, padding
  
  switch(layout) {
    case '标准':
      width = '1000px'
      height = '562.5px'
      padding = '40px'
      break
    case '宽屏':
      width = '1200px'
      height = '675px'
      padding = '48px'
      break
    case '紧凑':
      width = '800px'
      height = '450px'
      padding = '30px'
      break
    default:
      return
  }
  
  slideElement.style.width = width
  slideElement.style.height = height
  slideElement.style.padding = padding
  
  alert(`布局已实时切换为：${layout}`)
}

// 搜索 - 打开搜索面板
const search = () => {
  showSearch.value = true
}

// 跳转到指定幻灯片
const goToSlide = (slideId) => {
  const slide = slides.value.find(s => s.id === slideId)
  if (slide) {
    currentSlide.value = slide
    showSearch.value = false
  }
}

// 添加图片
const addImage = () => {
  alert('请在右侧配图面板选择或上传图片')
}

// 预览
const preview = () => {
  showPreview.value = true
}

// 保存
const save = () => {
  localStorage.setItem('savedPPT', JSON.stringify(slides.value))
  alert('保存成功！数据已保存到本地')
}

// 撤销
const undo = () => {
  if (historyIndex.value > 0) {
    historyIndex.value--
    slides.value = JSON.parse(JSON.stringify(history.value[historyIndex.value]))
    currentSlide.value = slides.value[0]
    alert('撤销成功')
  } else {
    alert('没有可以撤销的操作')
  }
}

// 重做
const redo = () => {
  if (historyIndex.value < history.value.length - 1) {
    historyIndex.value++
    slides.value = JSON.parse(JSON.stringify(history.value[historyIndex.value]))
    currentSlide.value = slides.value[0]
    alert('重做成功')
  } else {
    alert('没有可以重做的操作')
  }
}

// 导出
const exportPPT = (format) => {
  alert(`正在导出为 ${format} 格式...`)
  setTimeout(() => {
    alert(`导出成功！文件已保存`)
  }, 1000)
}

// 更新图片
const updateImage = (image) => {
  if (currentSlide.value) {
    currentSlide.value.image = image
    saveToHistory()
    alert('图片已添加')
  }
}
const handleGeneratePPT = async () => {
  try {
    alert('正在生成PPT，请稍候...')
    
    // 从路由参数获取大纲数据
    const outlineParam = route.query.outline
    if (!outlineParam) {
      alert('未找到大纲数据')
      return
    }
    
    const outlineData = JSON.parse(outlineParam)
    
    const response = await axios.post(`${API_BASE_URL}/generate-content`, {
      subject: outlineData.title || 'PPT生成',
      stage: 'generate',
      refined_outline: JSON.stringify(outlineData.items),  // 使用传入的 items
      mode: 'dify'
    })
    
    console.log('后端返回:', response.data)
    
    // 只处理下载链接
    if (response.data.download_url) {
      downloadUrl.value = response.data.download_url
      alert('PPT生成成功！可以点击下载按钮')
    } else {
      alert('生成成功，但未获取到下载链接')
    }
    
  } catch (error) {
    console.error('生成PPT失败:', error)
    alert('生成PPT失败：' + (error.response?.data?.message || error.message))
  }
}
</script>

<style scoped>
.ppt-editor {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: linear-gradient(
    to bottom,
    rgba(212, 245, 245, 0.2),
    rgba(130, 212, 215, 0.5) 25%,
    rgba(174, 230, 231, 0.5) 50%,
    rgba(189, 236, 236, 0.3) 75%,
    rgba(189, 236, 236, 0.3)
  );
  position: relative;
}

/* 左侧缩略图区域 */
:deep(.sidebar) {
  width: 220px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.5);
}

/* 右侧面板 */
.right-panel {
  display: flex;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255, 255, 255, 0.5);
  width: 350px;
  height: 100vh;
}

/* 工具栏 */
:deep(.toolbar) {
  width: 60px;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 0;
  gap: 16px;
  height: 100%;
  overflow-y: auto;
}

:deep(.tool-btn) {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.3);
  color: #34495e;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

:deep(.tool-btn:hover) {
  background: white;
  color: rgb(11, 167, 175);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.2);
  border-color: rgb(11, 167, 175);
}

/* 配图面板 */
:deep(.side-editor) {
  flex: 1;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  padding: 20px;
  overflow-y: auto;
  height: 100%;
}

:deep(.side-editor-header h3) {
  color: #1e3c5c;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(11, 167, 175, 0.2);
}

:deep(.image-section h4),
:deep(.image-suggestions h4) {
  color: #1e3c5c;
  font-size: 14px;
  margin-bottom: 12px;
}

:deep(.no-image p) {
  color: #4a5568;
}

:deep(.image-info) {
  color: #4a5568;
  font-size: 12px;
}

:deep(.image-preview) {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

:deep(.image-action-btn) {
  background: white;
  color: #4a5568;
  border: 1px solid #e2e8f0;
}

:deep(.image-action-btn.primary) {
  background: rgb(11, 167, 175);
  color: white;
  border: none;
}

:deep(.search-box) {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

:deep(.search-input) {
  color: #34495e;
}

:deep(.search-input::placeholder) {
  color: #94a3b8;
}

:deep(.search-btn) {
  background: rgb(11, 167, 175);
  color: white;
}

:deep(.suggestion-item) {
  border: 2px solid transparent;
}

:deep(.suggestion-item:hover) {
  border-color: rgb(11, 167, 175);
}

/* 预览弹窗 */
.preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(5px);
}

.preview-content {
  width: 800px;
  max-width: 90vw;
  max-height: 80vh;
  background: white;
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.preview-header h3 {
  color: #1e293b;
  font-size: 18px;
  margin: 0;
}

.close-preview {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: #e2e8f0;
  color: #64748b;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-preview:hover {
  background: #cbd5e1;
  color: #1e293b;
}

.preview-slides {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.preview-slide {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  min-height: 200px;
}

.preview-slide h2 {
  font-size: 24px;
  color: #1e293b;
  margin-bottom: 12px;
}

.preview-slide p {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 16px;
}

.preview-steps {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.preview-step {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #475569;
}

.preview-step-num {
  width: 20px;
  height: 20px;
  background: #e2e8f0;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #334155;
}

.preview-index {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 12px;
  color: #94a3b8;
  background: rgba(255, 255, 255, 0.9);
  padding: 4px 8px;
  border-radius: 12px;
}
</style>