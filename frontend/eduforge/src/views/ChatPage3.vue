<!-- ChatPage3.vue - 彻底移除水平滚动条版本 -->
<template>
  <div class="chat3-container">
    <!-- 返回按钮 - 与GeneratePage完全一致 -->
    <div class="button-group">
      <button class="back-button outline-button icon-button" @click="goBack">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
    </div>

    <!-- 标题区域 - 左对齐 -->
    <div class="content-wrapper">
      <div class="title-section">
        <h1 class="page-title">选择模板</h1>
        <p class="page-subtitle">从精选模板开始创作</p>
      </div>
      
      <!-- 标签栏 - 左对齐 -->
      <div class="tabs-section">
        <div class="tab-buttons">
          <button class="tab-btn" 
                  :class="{ active: selectedTab === 'workspace' }"
                  @click="selectedTab = 'workspace'">
            <span class="iconfont icon-mobansheji tab-icon"></span>
            工作区模板
          </button>
          <button class="tab-btn" 
                  :class="{ active: selectedTab === 'all' }"
                  @click="selectedTab = 'all'">
            <span class="iconfont icon-tucengfengge tab-icon"></span>
            全部模板
          </button>
        </div>
      </div>

      <!-- 搜索与筛选 - 左对齐 -->
      <div class="search-filter-section">
        <!-- 搜索框 -->
        <div class="search-box">
          <span class="iconfont icon-xiala" style="transform: rotate(90deg); font-size: 16px; color: #999;"></span>
          <input 
            type="text" 
            v-model="searchKeyword" 
            placeholder="搜索模板"
            class="search-input"
          />
        </div>

        <!-- 分类下拉 -->
        <div class="select-item" @click.stop="toggleDropdown('category')">
          <span class="iconfont icon-tucengfengge select-icon"></span>
          <span>{{ selectedCategory }}</span>
          <span class="iconfont icon-xiala select-arrow" :class="{ rotated: dropdownOpen.category }"></span>
          <div v-if="dropdownOpen.category" class="dropdown-menu">
            <div class="dropdown-item" v-for="cat in categories" :key="cat" @click.stop="selectCategory(cat)">
              {{ cat }}
            </div>
          </div>
        </div>

        <!-- 排序下拉 -->
        <div class="select-item" @click.stop="toggleDropdown('sort')">
          <span class="iconfont icon-bili-ziyoubili select-icon"></span>
          <span>{{ selectedSort }}</span>
          <span class="iconfont icon-xiala select-arrow" :class="{ rotated: dropdownOpen.sort }"></span>
          <div v-if="dropdownOpen.sort" class="dropdown-menu">
            <div class="dropdown-item" @click.stop="selectSort('最近添加')">最近添加</div>
            <div class="dropdown-item" @click.stop="selectSort('最多使用')">最多使用</div>
            <div class="dropdown-item" @click.stop="selectSort('名称 A-Z')">名称 A-Z</div>
          </div>
        </div>
      </div>

      <!-- 模板卡片网格 - 左对齐，可上下滚动 -->
      <div class="template-grid-section">
        <div class="template-grid">
          <!-- 卡片 1 -->
          <div class="template-card" @click="selectTemplate('战略优先级框架')">
            <div class="card-preview">
              <div class="card-text-left">
                <div class="card-title-en">Strategic Priorities Framework</div>
              </div>
              <div class="card-image" style="background: url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400') no-repeat center/cover"></div>
            </div>
            <div class="card-label">战略优先级框架</div>
          </div>

          <!-- 卡片 2 -->
          <div class="template-card" @click="selectTemplate('融资进展更新')">
            <div class="card-preview">
              <div class="card-text-left">
                <div class="card-title-en">Fundraising Update</div>
                <div class="card-subtitle-en">Progress, Momentum & Next Steps</div>
              </div>
              <div class="card-image" style="background: url('https://images.unsplash.com/photo-1563986768609-322da13575f3?w=400') no-repeat center/cover"></div>
            </div>
            <div class="card-label">融资进展更新</div>
          </div>

          <!-- 卡片 3 -->
          <div class="template-card" @click="selectTemplate('投资者路演')">
            <div class="card-preview">
              <div class="card-text-full" style="background: #f5f7fa">
                <div class="card-title-en blue">TechVenture Investor Pitch</div>
                <div class="card-desc">Transforming my business with this amazing template</div>
              </div>
            </div>
            <div class="card-label">投资者路演</div>
          </div>

          <!-- 卡片 4 -->
          <div class="template-card" @click="selectTemplate('执行摘要')">
            <div class="card-preview">
              <div class="card-text-full dark">
                <div class="card-title-en light">Executive Summary</div>
                <div class="card-small-btns">
                  <span class="card-small-btn">Your Company</span>
                  <span class="card-small-btn">Date</span>
                </div>
              </div>
            </div>
            <div class="card-label">执行摘要</div>
          </div>

          <!-- 卡片 5 -->
          <div class="template-card" @click="selectTemplate('销售激励启动会')">
            <div class="card-preview">
              <div class="card-text-left">
                <div class="card-title-en">Sales Incentive Kickoff</div>
                <div class="card-subtitle-en">Ignite Your Winning Year</div>
              </div>
              <div class="card-image" style="background: url('https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=400') no-repeat center/cover"></div>
            </div>
            <div class="card-label">销售激励启动会</div>
          </div>

          <!-- 卡片 6 -->
          <div class="template-card" @click="selectTemplate('培训项目概述')">
            <div class="card-preview" style="background: #f0f2f5">
              <div class="card-text-center">
                <div class="card-title-en">Training Program Overview</div>
                <span class="card-small-btn light">LEARN MORE</span>
                <div class="card-small-text">name@company.com</div>
              </div>
            </div>
            <div class="card-label">培训项目概述</div>
          </div>

          <!-- 卡片 7 -->
          <div class="template-card" @click="selectTemplate('公司价值观')">
            <div class="card-preview">
              <div class="card-text-left">
                <div class="card-title-en large">Company Values</div>
              </div>
              <div class="card-image" style="background: url('https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=400') no-repeat center/cover"></div>
            </div>
            <div class="card-label">公司价值观</div>
          </div>

          <!-- 卡片 8 -->
          <div class="template-card" @click="selectTemplate('内容日历')">
            <div class="card-preview">
              <div class="card-text-left">
                <div class="card-title-en">Your Content Calendar</div>
                <div class="card-subtitle-en">Plan, Publish, and Prosper</div>
              </div>
              <div class="card-image" style="background: url('https://images.unsplash.com/photo-1617791160536-598cf32026fb?w=400') no-repeat center/cover"></div>
            </div>
            <div class="card-label">内容日历</div>
          </div>
        </div>
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
const searchKeyword = ref('')
const selectedTab = ref('all')
const selectedCategory = ref('全部模板')
const selectedSort = ref('最近添加')

const categories = ['全部模板', '有创造力的', '教育', '报告', '项目管理', '筹款', '销售量', '营销', '咨询', '战略']

// 下拉菜单状态
const dropdownOpen = ref({
  category: false,
  sort: false
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

const selectCategory = (category: string) => {
  selectedCategory.value = category
  dropdownOpen.value.category = false
}

const selectSort = (sort: string) => {
  selectedSort.value = sort
  dropdownOpen.value.sort = false
}

const selectTemplate = (templateName: string) => {
  router.push({
    path: '/generate',
    query: { template: templateName }
  })
}

const handleHelp = () => {
  alert('选择模板开始创作')
}
</script>

<style scoped>
/* 全局样式重置 - 关键：设置盒模型为border-box */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box; /* 核心：padding/border不增加元素总宽度 */
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* 主容器 - 彻底禁止水平滚动 */
.chat3-container {
  min-height: 100vh;
  width: 100%; /* 改用100%而非100vw，避免滚动条宽度问题 */
  background: linear-gradient(
    135deg,
    rgba(240, 248, 255, 0.8) 0%,
    rgba(230, 245, 250, 0.9) 50%,
    rgba(220, 240, 245, 0.8) 100%
  );
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 80px 0 40px;
  overflow-x: hidden; /* 强制隐藏水平滚动 */
  overflow-y: auto;   /* 只允许垂直滚动 */
}

/* 核心修复：内容包装器 - 统一控制内边距和最大宽度 */
.content-wrapper {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto; /* 居中 */
  padding: 0 20px; /* 只在包装器加左右内边距，避免子元素溢出 */
}

/* 按钮组 - 与GeneratePage完全一致 */
.button-group {
  position: fixed;
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

/* 标题区域 - 左对齐 */
.title-section {
  text-align: left;
  margin-bottom: 20px;
}

.page-title {
  font-size: 42px;
  color: #1e3c5c;
  font-weight: 700;
  margin-bottom: 8px;
}

.page-subtitle {
  font-size: 18px;
  color: #4a6a8a;
}

/* 标签栏 - 左对齐 */
.tabs-section {
  margin-bottom: 30px;
}

.tab-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap; /* 允许换行，避免小屏幕溢出 */
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  border-radius: 30px;
  border: 1px solid rgba(30, 60, 92, 0.1);
  background: rgba(255, 255, 255, 0.6);
  font-size: 16px;
  color: #4a6a8a;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(4px);
  white-space: nowrap;
}

.tab-btn:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.tab-btn.active {
  background: white;
  border-color: rgb(11, 167, 175);
  color: rgb(11, 167, 175);
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.15);
}

.tab-icon {
  font-size: 18px;
}

/* 搜索筛选区域 - 左对齐 */
.search-filter-section {
  margin-bottom: 30px;
  display: flex;
  gap: 16px;
  flex-wrap: wrap; /* 小屏幕自动换行 */
  position: relative;
  z-index: 100;
}

/* 搜索框样式 */
.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  padding: 8px 16px;
  border-radius: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  min-width: 240px;
  flex: 1;
}

.search-input {
  border: none;
  outline: none;
  font-size: 14px;
  color: #34495e;
  background: transparent;
  width: 100%;
}

.search-input::placeholder {
  color: #999;
}

/* 下拉选择项 */
.select-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  padding: 8px 16px;
  border-radius: 30px;
  font-size: 14px;
  color: #34495e;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
  min-width: 140px;
}

.select-item:hover {
  background: #f8f9fa;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.select-arrow {
  transition: transform 0.3s ease;
  font-size: 12px;
  margin-left: auto;
}

.select-arrow.rotated {
  transform: rotate(180deg);
}

.select-icon {
  color: #71cdd1;
  font-size: 16px;
}

/* 下拉菜单 */
.dropdown-menu {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  min-width: 160px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
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
  padding: 12px 20px;
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

/* 模板卡片网格区域 */
.template-grid-section {
  padding-bottom: 60px;
}

/* 模板卡片网格 - 关键：使用auto-fill适配，避免固定列数溢出 */
.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); /* 自适应列数，最小宽度280px */
  gap: 24px;
  width: 100%;
}

/* 模板卡片 */
.template-card {
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
}

.template-card:hover {
  transform: translateY(-4px);
}

.card-preview {
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  margin-bottom: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.template-card:hover .card-preview {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
}

.card-text-left {
  width: 40%;
  background: white;
  padding: 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card-text-full {
  width: 100%;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card-text-center {
  width: 100%;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.card-image {
  width: 60%;
  background-size: cover !important;
  background-position: center !important;
}

.card-title-en {
  font-size: 14px;
  font-weight: 600;
  color: #1f2328;
  margin-bottom: 4px;
  line-height: 1.4;
}

.card-title-en.large {
  font-size: 18px;
}

.card-title-en.blue {
  color: #0969da;
}

.card-title-en.light {
  color: white;
}

.card-subtitle-en {
  font-size: 11px;
  color: #6e7781;
}

.card-desc {
  font-size: 10px;
  color: white;
  margin-top: 6px;
  padding: 4px 8px;
  background: #6e7781;
  border-radius: 4px;
  display: inline-block;
  line-height: 1.4;
}

.card-small-btns {
  display: flex;
  gap: 4px;
  margin-top: 8px;
  flex-wrap: wrap;
}

.card-small-btn {
  padding: 4px 8px;
  border-radius: 4px;
  background: #facc15;
  color: #451a03;
  font-size: 10px;
  border: none;
  display: inline-block;
}

.card-small-btn.light {
  background: rgba(255,255,255,0.8);
  color: #1f2328;
}

.card-small-text {
  font-size: 10px;
  color: #6e7781;
  margin-top: 4px;
}

.card-text-full.dark {
  background: #1f2328;
}

.card-label {
  font-size: 14px;
  color: #4e5969;
  text-align: center;
  font-weight: 500;
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

/* 响应式适配 - 简化：依赖auto-fill，无需手动改列数 */
@media (max-width: 600px) {
  .chat3-container {
    padding: 80px 0 40px;
  }
  
  .page-title {
    font-size: 36px;
  }
  
  .page-subtitle {
    font-size: 16px;
  }
  
  .tab-buttons {
    flex-direction: column;
  }
  
  .tab-btn {
    width: 100%;
    justify-content: center;
  }
  
  .search-filter-section {
    flex-direction: column;
  }
  
  .search-box, .select-item {
    width: 100%;
  }
}
</style>