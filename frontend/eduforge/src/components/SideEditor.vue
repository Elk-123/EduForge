<!-- src/components/SideEditor.vue -->
<template>
  <aside class="side-editor">
    <div class="side-editor-header">
      <h3>配图管理</h3>
    </div>
    
    <div class="side-editor-content">
      <!-- 当前配图 -->
      <div class="image-section">
        <h4>当前配图</h4>
        <div v-if="currentSlide?.image" class="image-preview" @click="openImageSelector">
          <img :src="currentSlide.image.url" alt="当前配图" />
          <div class="image-info">
            <p>位置: ({{ currentSlide.image.x }}, {{ currentSlide.image.y }})</p>
            <p>尺寸: {{ currentSlide.image.width }} x {{ currentSlide.image.height }}</p>
          </div>
          <div class="image-actions">
            <button class="image-action-btn" @click.stop="removeImage">删除</button>
            <button class="image-action-btn primary" @click.stop="openImageSelector">更换</button>
          </div>
        </div>
        <div v-else class="no-image" @click="openImageSelector">
          <span class="iconfont icon-tupian"></span>
          <p>点击添加配图</p>
        </div>
      </div>
      
      <!-- 图片搜索 -->
      <div class="search-section">
        <div class="search-box">
          <span class="iconfont icon-sousuobeifen2 search-icon"></span>
          <input 
            type="text" 
            v-model="searchKeyword" 
            placeholder="搜索图片..."
            class="search-input"
            @keyup.enter="searchImages"
          />
          <button class="search-btn" @click="searchImages">搜索</button>
        </div>
      </div>
      
      <!-- 推荐配图 / 搜索结果 -->
      <div class="image-suggestions">
        <div class="suggestions-header">
          <h4>{{ searchKeyword ? '搜索结果' : '推荐配图' }}</h4>
          <span v-if="loading" class="loading-text">加载中...</span>
        </div>
        
        <div v-if="images.length > 0" class="suggestion-grid">
          <div 
            v-for="(img, index) in images" 
            :key="index" 
            class="suggestion-item"
            @click="selectImage(img)"
          >
            <img :src="img.url" :alt="img.title" class="suggestion-img" />
            <div class="suggestion-overlay">
              <span class="iconfont icon-xuanze"></span>
            </div>
          </div>
        </div>
        
        <div v-else-if="!loading && searchKeyword" class="no-results">
          没有找到相关图片
        </div>
        
        <div v-else class="suggestion-placeholder">
          <div v-for="i in 4" :key="i" class="placeholder-item"></div>
        </div>
      </div>
      
      <!-- 加载更多 -->
      <div v-if="hasMore" class="load-more">
        <button class="load-more-btn" @click="loadMore" :disabled="loading">
          {{ loading ? '加载中...' : '加载更多' }}
        </button>
      </div>
    </div>

    <!-- 图片选择器弹窗 -->
    <Teleport to="body">
      <div v-if="showSelector" class="image-selector-overlay" @click.self="closeSelector">
        <div class="image-selector">
          <div class="selector-header">
            <h3>选择图片</h3>
            <button class="close-btn" @click="closeSelector">×</button>
          </div>
          
          <div class="selector-search">
            <input 
              type="text" 
              v-model="selectorKeyword" 
              placeholder="搜索图片..."
              class="selector-input"
              @keyup.enter="searchSelectorImages"
            />
            <button class="selector-search-btn" @click="searchSelectorImages">搜索</button>
          </div>
          
          <div class="selector-grid">
            <div 
              v-for="(img, index) in selectorImages" 
              :key="index" 
              class="selector-item"
              @click="confirmSelectImage(img)"
            >
              <img :src="img.url" :alt="img.title" class="selector-img" />
              <div class="selector-info">
                <p class="selector-title">{{ img.title }}</p>
                <p class="selector-size">{{ img.width }}x{{ img.height }}</p>
              </div>
            </div>
          </div>
          
          <div v-if="selectorLoading" class="selector-loading">
            加载中...
          </div>
        </div>
      </div>
    </Teleport>
  </aside>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  currentSlide: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:image', 'add-image'])

// 图片数据
const images = ref([])
const selectorImages = ref([])
const loading = ref(false)
const selectorLoading = ref(false)
const hasMore = ref(false)
const searchKeyword = ref('')
const selectorKeyword = ref('')
const showSelector = ref(false)
const page = ref(1)

// 模拟图片数据（实际应该从后端获取）
const mockImages = [
  { url: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400', title: '山峰', width: 400, height: 300 },
  { url: 'https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=400', title: '城市', width: 400, height: 300 },
  { url: 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=400', title: '办公', width: 400, height: 300 },
  { url: 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=400', title: '会议', width: 400, height: 300 },
  { url: 'https://images.unsplash.com/photo-1617791160536-598cf32026fb?w=400', title: '日历', width: 400, height: 300 },
  { url: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=400', title: '团队', width: 400, height: 300 },
  { url: 'https://images.unsplash.com/photo-1557804506-669a67965ba0?w=400', title: '战略', width: 400, height: 300 },
  { url: 'https://images.unsplash.com/photo-1553877522-43269d4ea984?w=400', title: '分析', width: 400, height: 300 }
]

// 搜索图片（调用后端接口）
const searchImages = async () => {
  loading.value = true
  page.value = 1
  
  try {
    // TODO: 替换为真实后端接口
    // const response = await fetch(`/api/images/search?keyword=${searchKeyword.value}&page=${page.value}`)
    // const data = await response.json()
    // images.value = data.images
    // hasMore.value = data.hasMore
    
    // 模拟数据
    await new Promise(resolve => setTimeout(resolve, 500))
    images.value = mockImages.filter(img => 
      !searchKeyword.value || img.title.includes(searchKeyword.value)
    )
    hasMore.value = false
  } catch (error) {
    console.error('搜索图片失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载更多
const loadMore = async () => {
  if (loading.value || !hasMore.value) return
  
  loading.value = true
  page.value++
  
  try {
    // TODO: 替换为真实后端接口
    // const response = await fetch(`/api/images/search?keyword=${searchKeyword.value}&page=${page.value}`)
    // const data = await response.json()
    // images.value = [...images.value, ...data.images]
    // hasMore.value = data.hasMore
  } catch (error) {
    console.error('加载更多失败:', error)
  } finally {
    loading.value = false
  }
}

// 打开选择器
const openImageSelector = () => {
  showSelector.value = true
  selectorKeyword.value = ''
  searchSelectorImages()
}

// 关闭选择器
const closeSelector = () => {
  showSelector.value = false
}

// 搜索选择器图片
const searchSelectorImages = async () => {
  selectorLoading.value = true
  
  try {
    // TODO: 替换为真实后端接口
    await new Promise(resolve => setTimeout(resolve, 500))
    selectorImages.value = mockImages.filter(img => 
      !selectorKeyword.value || img.title.includes(selectorKeyword.value)
    )
  } catch (error) {
    console.error('搜索图片失败:', error)
  } finally {
    selectorLoading.value = false
  }
}

// 选择图片
const selectImage = (img) => {
  if (!props.currentSlide) return
  
  const newImage = {
    url: img.url,
    title: img.title,
    x: 100,
    y: 100,
    width: 300,
    height: 200
  }
  
  emit('update:image', newImage)
}

// 确认选择图片
const confirmSelectImage = (img) => {
  selectImage(img)
  closeSelector()
}

// 移除图片
const removeImage = () => {
  emit('update:image', null)
}

// 初始加载推荐图片
searchImages()

// 监听当前幻灯片变化
watch(() => props.currentSlide, () => {
  // 可以在这里根据幻灯片内容推荐相关图片
  if (props.currentSlide?.title) {
    searchKeyword.value = props.currentSlide.title
    searchImages()
  }
}, { deep: true })
</script>

<style scoped>
.side-editor {
  flex: 1;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  padding: 20px;
  overflow-y: auto;
  height: 100%;
}

.side-editor-header {
  margin-bottom: 20px;
}

.side-editor-header h3 {
  color: #1e3c5c;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.side-editor-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.image-section h4,
.image-suggestions h4 {
  color: #1e3c5c;
  font-size: 14px;
  margin-bottom: 12px;
  font-weight: 500;
}

.image-preview {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 16px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.2s ease;
}

.image-preview:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(11, 167, 175, 0.15);
}

.image-preview img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.image-info {
  font-size: 12px;
  color: #4a5568;
  margin-bottom: 12px;
  line-height: 1.5;
}

.image-actions {
  display: flex;
  gap: 8px;
}

.image-action-btn {
  flex: 1;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: white;
  font-size: 12px;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.2s ease;
}

.image-action-btn.primary {
  background: rgb(11, 167, 175);
  color: white;
  border-color: rgb(11, 167, 175);
}

.image-action-btn:hover {
  transform: scale(1.02);
}

.image-action-btn.primary:hover {
  background: rgb(8, 130, 136);
}

.no-image {
  background: rgba(255, 255, 255, 0.6);
  border-radius: 16px;
  padding: 40px 0;
  text-align: center;
  border: 2px dashed rgba(11, 167, 175, 0.3);
  cursor: pointer;
  transition: all 0.2s ease;
}

.no-image:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: rgb(11, 167, 175);
}

.no-image .iconfont {
  font-size: 48px;
  color: #71cdd1;
  margin-bottom: 8px;
  display: block;
}

.no-image p {
  color: #4a5568;
  font-size: 14px;
}

/* 搜索区域 */
.search-section {
  margin-bottom: 8px;
}

.search-box {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 30px;
  padding: 4px 4px 4px 12px;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.search-icon {
  color: #94a3b8;
  font-size: 16px;
  margin-right: 8px;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 8px 0;
  font-size: 14px;
  color: #34495e;
  outline: none;
}

.search-input::placeholder {
  color: #94a3b8;
}

.search-btn {
  padding: 6px 16px;
  border-radius: 30px;
  border: none;
  background: rgb(11, 167, 175);
  color: white;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.search-btn:hover {
  background: rgb(8, 130, 136);
  transform: scale(1.02);
}

/* 推荐配图网格 */
.suggestions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.loading-text {
  font-size: 12px;
  color: #94a3b8;
}

.suggestion-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.suggestion-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
}

.suggestion-item:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 16px rgba(11, 167, 175, 0.2);
}

.suggestion-item:hover .suggestion-overlay {
  opacity: 1;
}

.suggestion-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.suggestion-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(11, 167, 175, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.suggestion-overlay .iconfont {
  color: white;
  font-size: 24px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  padding: 8px;
}

/* 占位符 */
.suggestion-placeholder {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.placeholder-item {
  aspect-ratio: 1;
  background: linear-gradient(135deg, #e2e8f0, #f1f5f9);
  border-radius: 12px;
  animation: pulse 1.5s ease infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.no-results {
  text-align: center;
  padding: 40px 0;
  color: #94a3b8;
  font-size: 14px;
}

/* 加载更多 */
.load-more {
  text-align: center;
  margin-top: 16px;
}

.load-more-btn {
  padding: 8px 24px;
  border-radius: 30px;
  border: 1px solid rgba(11, 167, 175, 0.3);
  background: white;
  color: rgb(11, 167, 175);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.load-more-btn:hover:not(:disabled) {
  background: rgb(11, 167, 175);
  color: white;
}

.load-more-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 图片选择器弹窗 */
.image-selector-overlay {
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
}

.image-selector {
  width: 800px;
  max-width: 90vw;
  max-height: 80vh;
  background: white;
  border-radius: 24px;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.selector-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.selector-header h3 {
  font-size: 20px;
  color: #1e3c5c;
  margin: 0;
}

.close-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #f1f5f9;
  color: #64748b;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.selector-search {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.selector-input {
  flex: 1;
  padding: 12px 16px;
  border-radius: 30px;
  border: 1px solid #e2e8f0;
  font-size: 14px;
  outline: none;
  transition: all 0.2s ease;
}

.selector-input:focus {
  border-color: rgb(11, 167, 175);
  box-shadow: 0 0 0 3px rgba(11, 167, 175, 0.1);
}

.selector-search-btn {
  padding: 0 24px;
  border-radius: 30px;
  border: none;
  background: rgb(11, 167, 175);
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.selector-search-btn:hover {
  background: rgb(8, 130, 136);
}

.selector-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  overflow-y: auto;
  padding: 4px;
}

.selector-item {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
}

.selector-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(11, 167, 175, 0.15);
  border-color: rgb(11, 167, 175);
}

.selector-img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.selector-info {
  padding: 8px;
  background: white;
}

.selector-title {
  font-size: 12px;
  color: #1e293b;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.selector-size {
  font-size: 10px;
  color: #94a3b8;
}

.selector-loading {
  text-align: center;
  padding: 40px;
  color: #94a3b8;
}

/* 滚动条 */
.side-editor::-webkit-scrollbar,
.selector-grid::-webkit-scrollbar {
  width: 4px;
}

.side-editor::-webkit-scrollbar-track,
.selector-grid::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

.side-editor::-webkit-scrollbar-thumb,
.selector-grid::-webkit-scrollbar-thumb {
  background: rgba(11, 167, 175, 0.3);
  border-radius: 10px;
}
</style>