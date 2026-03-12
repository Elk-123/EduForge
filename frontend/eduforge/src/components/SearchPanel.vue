<!-- src/components/SearchPanel.vue -->
<template>
  <div class="search-panel" v-if="show">
    <div class="search-header">
      <h3>搜索</h3>
      <button class="close-btn" @click="$emit('close')">×</button>
    </div>
    
    <div class="search-input-wrapper">
      <span class="iconfont icon-sousuobeifen2 search-icon"></span>
      <input 
        ref="searchInput"
        type="text" 
        v-model="keyword" 
        placeholder="输入关键词搜索..."
        class="search-input"
        @keyup.enter="handleSearch"
      />
      <button class="search-btn" @click="handleSearch">搜索</button>
    </div>
    
    <div v-if="searching" class="search-status">搜索中...</div>
    
    <div v-else-if="results.length > 0" class="search-results">
      <div class="result-count">找到 {{ results.length }} 个结果</div>
      <div class="result-list">
        <div 
          v-for="(result, index) in results" 
          :key="index"
          class="result-item"
          @click="goToResult(result)"
        >
          <span class="result-page">第{{ result.page }}页</span>
          <span class="result-content">{{ result.content }}</span>
        </div>
      </div>
    </div>
    
    <div v-else-if="searched && !searching" class="no-results">
      未找到相关内容
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  slides: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'navigate'])

const keyword = ref('')
const searchInput = ref(null)
const results = ref([])
const searching = ref(false)
const searched = ref(false)

// 当显示搜索框时自动聚焦
watch(() => props.show, (newVal) => {
  if (newVal) {
    nextTick(() => {
      searchInput.value?.focus()
    })
    keyword.value = ''
    results.value = []
    searched.value = false
  }
})

// 执行搜索
const handleSearch = () => {
  if (!keyword.value.trim()) return
  
  searching.value = true
  searched.value = true
  
  // 模拟搜索延迟
  setTimeout(() => {
    const searchTerm = keyword.value.toLowerCase()
    const newResults = []
    
    props.slides.forEach((slide, slideIndex) => {
      // 搜索标题
      if (slide.title?.toLowerCase().includes(searchTerm)) {
        newResults.push({
          page: slideIndex + 1,
          content: slide.title,
          slideId: slide.id,
          type: 'title'
        })
      }
      
      // 搜索内容
      if (slide.content?.toLowerCase().includes(searchTerm)) {
        newResults.push({
          page: slideIndex + 1,
          content: slide.content.substring(0, 30) + (slide.content.length > 30 ? '...' : ''),
          slideId: slide.id,
          type: 'content'
        })
      }
      
      // 搜索步骤
      slide.steps?.forEach(step => {
        if (step.title?.toLowerCase().includes(searchTerm)) {
          newResults.push({
            page: slideIndex + 1,
            content: `步骤: ${step.title}`,
            slideId: slide.id,
            type: 'step'
          })
        }
        if (step.desc?.toLowerCase().includes(searchTerm)) {
          newResults.push({
            page: slideIndex + 1,
            content: `描述: ${step.desc.substring(0, 30)}${step.desc.length > 30 ? '...' : ''}`,
            slideId: slide.id,
            type: 'step'
          })
        }
      })
    })
    
    results.value = newResults
    searching.value = false
  }, 300)
}

// 跳转到结果
const goToResult = (result) => {
  emit('navigate', result.slideId)
  emit('close')
}
</script>

<style scoped>
.search-panel {
  position: absolute;
  top: 80px;
  right: 360px; /* 在工具栏左边 */
  width: 320px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  overflow: hidden;
  animation: slideDown 0.2s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.search-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  color: white;
}

.search-header h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
}

.search-icon {
  color: #94a3b8;
  font-size: 16px;
  margin-right: 8px;
}

.search-input {
  flex: 1;
  border: none;
  padding: 8px 0;
  font-size: 14px;
  outline: none;
  color: #1e293b;
}

.search-input::placeholder {
  color: #94a3b8;
}

.search-btn {
  padding: 6px 16px;
  border-radius: 20px;
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

.search-status,
.no-results {
  padding: 40px 20px;
  text-align: center;
  color: #94a3b8;
  font-size: 14px;
}

.search-results {
  max-height: 300px;
  overflow-y: auto;
}

.result-count {
  padding: 10px 16px;
  font-size: 12px;
  color: #64748b;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.result-list {
  padding: 8px 0;
}

.result-item {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.result-item:hover {
  background: #f1f5f9;
  border-left-color: rgb(11, 167, 175);
}

.result-page {
  font-size: 12px;
  color: rgb(11, 167, 175);
  background: #e6f7ff;
  padding: 2px 8px;
  border-radius: 12px;
  margin-right: 12px;
  white-space: nowrap;
}

.result-content {
  font-size: 13px;
  color: #334155;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 滚动条 */
.search-results::-webkit-scrollbar {
  width: 4px;
}

.search-results::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.search-results::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.search-results::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>