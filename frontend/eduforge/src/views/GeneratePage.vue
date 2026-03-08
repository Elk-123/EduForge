<template>
  <div class="generate-page-container">
    <!-- 返回按钮 -->
    <div class="button-group">
      <button class="back-button outline-button icon-button" @click="handleBack">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
    </div>

    <div class="title-main">生成</div>
    <div class="title-sub">您今天想创作什么？</div>
    
    <!-- 四个方块 -->
    <div class="block-container">
      <!-- 1 演示文稿 -->
      <div class="white-block block-item" 
           :class="{ active: activeBlock === 1 }"
           @mouseenter="handleBlockHover(1)" 
           @mouseleave="handleBlockLeave"
           @click="handleBlockClick(1)">
        <div class="icon-wrapper icon1">
          <svg class="block-icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M682.666667 85.333333l213.333333 213.333334v597.674666a42.368 42.368 0 0 1-42.368 42.325334H170.368A42.666667 42.666667 0 0 1 128 896.341333V127.658667C128 104.277333 146.986667 85.333333 170.368 85.333333H682.666667z" fill="#71cdd1"></path>
            <path d="M341.333333 341.333333v341.333334h85.333334v-85.333334h256V341.333333H341.333333z m85.333334 85.333334h170.666666v85.333333h-170.666666v-85.333333z" fill="#FFF8F4" opacity=".8"></path>
          </svg>
        </div>
        <div class="block-text">演示文稿</div>
      </div>

      <!-- 2 网页 -->
      <div class="white-block block-item" 
           :class="{ active: activeBlock === 2 }"
           @mouseenter="handleBlockHover(2)" 
           @mouseleave="handleBlockLeave"
           @click="handleBlockClick(2)">
        <div class="icon-wrapper icon2">
          <svg class="block-icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M952.888889 281.6V910.222222c0 62.862222-50.915556 113.777778-113.777778 113.777778H156.444444c-62.862222 0-113.777778-50.915556-113.777777-113.777778V113.777778c0-62.862222 50.915556-113.777778 113.777777-113.777778h514.844445L952.888889 281.6z" fill="#71cdd1"></path>
            <path d="M511.146667 294.656l0.711111 0.142222a246.044444 246.044444 0 0 1 0 491.292445 17.92 17.92 0 0 1-5.688889 0.284444h-0.995556l-7.395555 0.113778a246.044444 246.044444 0 1 1 8.391111-491.946667 17.237333 17.237333 0 0 1 4.977778 0.113778z m-98.986667 355.271111l-92.501333 0.028445a209.180444 209.180444 0 0 0 144.896 96.938666 334.961778 334.961778 0 0 1-52.394667-96.938666z m263.736889 0.028445H592.497778a337.92 337.92 0 0 1-50.062222 94.776888 209.351111 209.351111 0 0 0 133.461333-94.776888z m-122.737778 0h-101.603555a298.069333 298.069333 0 0 0 51.2 85.248c21.902222-26.026667 38.684444-54.897778 50.403555-85.248z m-155.534222-159.288889h-102.968889A209.578667 209.578667 0 0 0 288.711111 540.444444c0 25.486222 4.551111 49.92 12.913778 72.533334h100.181333a338.773333 338.773333 0 0 1-4.181333-122.311111z m171.832889 0.028444h-134.4a301.511111 301.511111 0 0 0 4.721778 122.282667h125.013333c9.813333-40.078222 11.377778-81.720889 4.664889-122.282667z m131.413333 0h-93.980444a342.186667 342.186667 0 0 1-4.152889 122.282667h91.192889A208.64 208.64 0 0 0 706.844444 540.444444c0-17.152-2.076444-33.820444-5.973333-49.777777z m-236.288-156.728889l-0.711111 0.142222A209.351111 209.351111 0 0 0 307.484444 453.688889h97.735112a334.705778 334.705778 0 0 1 59.335111-119.694222z m38.200889 11.719111l-3.868444 4.579556a298.012444 298.012444 0 0 0-55.239112 103.452444h117.248a301.397333 301.397333 0 0 0-58.140444-108.032z m39.651556-9.528889l4.295111 5.831112a338.062222 338.062222 0 0 1 52.622222 111.701333h88.689778a209.464889 209.464889 0 0 0-145.607111-117.532445z" fill="#FFFFFF"></path>
            <path d="M676.664889 167.822222V0l281.6 281.6h-167.822222c-62.862222 0-113.777778-50.915556-113.777778-113.777778" fill="#2B9592"></path>
          </svg>
        </div>
        <div class="block-text">网页</div>
      </div>

      <!-- 3 文档 -->
      <div class="white-block block-item" 
           :class="{ active: activeBlock === 3 }"
           @mouseenter="handleBlockHover(3)" 
           @mouseleave="handleBlockLeave"
           @click="handleBlockClick(3)">
        <div class="icon-wrapper icon3">
          <svg class="block-icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M146.863158 0h538.947368l296.421053 296.421053v619.789473c0 59.284211-48.505263 107.789474-107.789474 107.789474H146.863158c-59.284211 0-107.789474-48.505263-107.789474-107.789474V107.789474c0-59.284211 48.505263-107.789474 107.789474-107.789474z" fill="#71cdd1"></path>
            <path d="M688.505263 0l296.421053 296.421053h-296.421053V0zM549.726316 661.557895H142.821053c-14.821053 0-25.6-12.126316-25.6-25.6V633.263158c0-14.821053 12.126316-25.6 25.6-25.6h406.905263c13.473684 0 25.6 12.126316 25.6 25.6v2.694737c0 13.473684-10.778947 25.6-25.6 25.6z m-134.736842-350.31579H142.821053c-14.821053 0-25.6-10.778947-25.6-25.6V282.947368c0-14.821053 12.126316-25.6 25.6-25.6h272.168421c13.473684 0 25.6 12.126316 25.6 25.6v2.694737c0 13.473684-10.778947 25.6-25.6 25.6z m-272.168421 121.263158h245.221052c13.473684 0 25.6 12.126316 25.6 25.6v2.694737c0 13.473684-12.126316 25.6-25.6 25.6H142.821053c-14.821053 0-25.6-10.778947-25.6-25.6V458.105263c0-14.821053 12.126316-25.6 25.6-25.6z" fill="#AFFCFE"></path>
          </svg>
        </div>
        <div class="block-text">文档</div>
      </div>

      <!-- 4 社媒 -->
      <div class="white-block block-item" 
           :class="{ active: activeBlock === 4 }"
           @mouseenter="handleBlockHover(4)" 
           @mouseleave="handleBlockLeave"
           @click="handleBlockClick(4)">
        <div class="icon-wrapper icon4">
          <svg class="block-icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M419.584 358.144a21.333333 21.333333 0 0 1 21.333333 21.333333v151.68a21.333333 21.333333 0 0 1-21.333333 21.333334H376.874667a21.333333 21.333333 0 0 1-21.333334-21.333334V379.477333a21.333333 21.333333 0 0 1 21.333334-21.333333h42.709333zM647.125333 358.144a21.333333 21.333333 0 0 1 21.333334 21.333333v151.68a21.333333 21.333333 0 0 1-21.333334 21.333334h-42.709333a21.333333 21.333333 0 0 1-21.333333-21.333334V379.477333a21.333333 21.333333 0 0 1 21.333333-21.333333h42.709333z" fill="#9ed1d3"></path>
            <path d="M768 146.986667a128 128 0 0 1 128 128v360.234666l-0.170667 6.613334A128 128 0 0 1 768 763.178667h-261.461333l-201.856 108.714666a42.666667 42.666667 0 0 1-62.890667-37.546666v-71.978667a128 128 0 0 1-113.621333-120.576L128 635.221333V274.986667a128 128 0 0 1 128-128h512z m-512 85.333333a42.666667 42.666667 0 0 0-42.666667 42.666667v360.234666l0.213334 4.394667a42.666667 42.666667 0 0 0 42.453333 38.272h28.458667a42.666667 42.666667 0 0 1 42.666666 42.666667v42.325333l148.48-79.914667 4.778667-2.176a42.666667 42.666667 0 0 1 15.402667-2.901333H768a42.666667 42.666667 0 0 0 42.453333-38.272l0.213334-4.394667V274.986667a42.666667 42.666667 0 0 0-42.666667-42.666667H256z" fill="#71cdd1"></path>
          </svg>
        </div>
        <div class="block-text">社媒</div>
      </div>
    </div>

    <!-- 下拉选择栏（带展开功能） -->
    <div class="select-bar">
      <!-- 卡片数量下拉 -->
      <div class="select-item" @click.stop="toggleDropdown('cardCount')">
        <span>{{ cardCount }}张卡片</span>
        <svg class="select-arrow" :class="{ rotated: dropdownOpen.cardCount }" width="12" height="12" viewBox="0 0 1024 1024" fill="currentColor">
          <path d="M840.4 300H183.6c-19.9 0-30.8 20.8-18.5 35l328.4 380.8c11.9 13.9 32.2 13.9 44.1 0l328.4-380.8c12.4-14.2 1.5-35-18.5-35z"></path>
        </svg>
        <!-- 下拉菜单 -->
        <div v-if="dropdownOpen.cardCount" class="dropdown-menu">
          <div class="dropdown-item" @click.stop="selectCardCount(5)">5张卡片</div>
          <div class="dropdown-item" @click.stop="selectCardCount(10)">10张卡片</div>
          <div class="dropdown-item" @click.stop="selectCardCount(15)">15张卡片</div>
          <div class="dropdown-item" @click.stop="selectCardCount(20)">20张卡片</div>
        </div>
      </div>

      <!-- 风格下拉 -->
      <div class="select-item" @click.stop="toggleDropdown('style')">
        <svg class="select-icon" width="16" height="16" viewBox="0 0 1024 1024" fill="currentColor">
          <path d="M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.4 0-372-166.6-372-372s166.6-372 372-372 372 166.6 372 372-166.6 372-372 372z"></path>
          <path d="M464 336a48 48 0 1 0 96 0 48 48 0 1 0-96 0zm72 64h-48v288h48V400zm208-120h-48v288h48V280z"></path>
        </svg>
        <span>{{ selectedStyle }}</span>
        <svg class="select-arrow" :class="{ rotated: dropdownOpen.style }" width="12" height="12" viewBox="0 0 1024 1024" fill="currentColor">
          <path d="M840.4 300H183.6c-19.9 0-30.8 20.8-18.5 35l328.4 380.8c11.9 13.9 32.2 13.9 44.1 0l328.4-380.8c12.4-14.2 1.5-35-18.5-35z"></path>
        </svg>
        <!-- 下拉菜单 -->
        <div v-if="dropdownOpen.style" class="dropdown-menu">
          <div class="dropdown-item" @click.stop="selectStyle('经典')">经典</div>
          <div class="dropdown-item" @click.stop="selectStyle('现代')">现代</div>
          <div class="dropdown-item" @click.stop="selectStyle('简约')">简约</div>
          <div class="dropdown-item" @click.stop="selectStyle('创意')">创意</div>
        </div>
      </div>

      <!-- 方向下拉 -->
      <div class="select-item" @click.stop="toggleDropdown('orientation')">
        <svg class="select-icon" width="16" height="16" viewBox="0 0 1024 1024" fill="currentColor">
          <path d="M768 903.2V120.8c0-44.2-43.2-80.8-96-80.8H352c-52.8 0-96 36.6-96 80.8v782.4c0 44.2 43.2 80.8 96 80.8h320c52.8 0 96-36.6 96-80.8zM512 896c-17.7 0-32-14.3-32-32s14.3-32 32-32 32 14.3 32 32-14.3 32-32 32z"></path>
        </svg>
        <span>{{ selectedOrientation }}</span>
        <svg class="select-arrow" :class="{ rotated: dropdownOpen.orientation }" width="12" height="12" viewBox="0 0 1024 1024" fill="currentColor">
          <path d="M840.4 300H183.6c-19.9 0-30.8 20.8-18.5 35l328.4 380.8c11.9 13.9 32.2 13.9 44.1 0l328.4-380.8c12.4-14.2 1.5-35-18.5-35z"></path>
        </svg>
        <!-- 下拉菜单 -->
        <div v-if="dropdownOpen.orientation" class="dropdown-menu">
          <div class="dropdown-item" @click.stop="selectOrientation('默认   动态')">默认   动态</div>
          <div class="dropdown-item" @click.stop="selectOrientation('传统   16:9')">传统   16:9</div>
          <div class="dropdown-item" @click.stop="selectOrientation('高大    4:3')">高大    4:3</div>
        </div>
      </div>

      <!-- 语言下拉 -->
      <div class="select-item" @click.stop="toggleDropdown('language')">
        <svg class="select-icon" width="16" height="16" viewBox="0 0 1024 1024" fill="currentColor">
          <path d="M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.4 0-372-166.6-372-372s166.6-372 372-372 372 166.6 372 372-166.6 372-372 372z"></path>
          <path d="M434.1 685.7l-67.6 39.7c-3.4 2-7.4 2-10.8 0l-67.6-39.7c-2.3-1.4-4.6-3.9-4.6-6.6V376.9c0-2.7 2.3-5.2 4.6-6.6l67.6-39.7c3.4-2 7.4-2 10.8 0l67.6 39.7c2.3 1.4 4.6 3.9 4.6 6.6v302.2c0 2.7-2.3 5.2-4.6 6.6zM658.9 685.7l-67.6 39.7c-3.4 2-7.4 2-10.8 0l-67.6-39.7c-2.3-1.4-4.6-3.9-4.6-6.6V376.9c0-2.7 2.3-5.2 4.6-6.6l67.6-39.7c3.4-2 7.4-2 10.8 0l67.6 39.7c2.3 1.4 4.6 3.9 4.6 6.6v302.2c0 2.7-2.3 5.2-4.6 6.6z"></path>
        </svg>
        <span>{{ selectedLanguage }}</span>
        <svg class="select-arrow" :class="{ rotated: dropdownOpen.language }" width="12" height="12" viewBox="0 0 1024 1024" fill="currentColor">
          <path d="M840.4 300H183.6c-19.9 0-30.8 20.8-18.5 35l328.4 380.8c11.9 13.9 32.2 13.9 44.1 0l328.4-380.8c12.4-14.2 1.5-35-18.5-35z"></path>
        </svg>
        <!-- 下拉菜单 -->
        <div v-if="dropdownOpen.language" class="dropdown-menu">
          <div class="dropdown-item" @click.stop="selectLanguage('简体中文')">简体中文</div>
          <div class="dropdown-item" @click.stop="selectLanguage('繁体中文')">繁体中文</div>
          <div class="dropdown-item" @click.stop="selectLanguage('English')">English</div>
          <div class="dropdown-item" @click.stop="selectLanguage('日本語')">日本語</div>
        </div>
      </div>
    </div>

    <!-- 大输入框（带发送箭头） -->
    <div class="input-container">
      <input 
        type="text" 
        class="main-input" 
        v-model="inputValue" 
        placeholder="描述您想生成的内容" 
        @keyup.enter="handleSend"
      />
      <button class="send-button" @click="handleSend">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <!-- 示例提示区域（固定卡片，支持换行） -->
    <div class="example-section">
      <div class="example-title">示例提示</div>
      <div class="example-grid">
        <div class="example-card" v-for="(example, index) in exampleList" :key="index" @click="handleExampleClick(example)">
          <div class="example-content">
            <svg class="example-icon" width="16" height="16" viewBox="0 0 1024 1024" fill="currentColor">
              <path d="M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.4 0-372-166.6-372-372s166.6-372 372-372 372 166.6 372 372-166.6 372-372 372z"></path>
              <path d="M464 336a48 48 0 1 0 96 0 48 48 0 1 0-96 0zm72 64h-48v288h48V400zm208-120h-48v288h48V280z"></path>
            </svg>
            <span class="example-text">{{ example }}</span>
          </div>
          <div class="example-add">+</div>
        </div>
      </div>
      <button class="refresh-button" @click="handleRefreshExample">
        <svg class="refresh-icon" width="16" height="16" viewBox="0 0 1024 1024" fill="currentColor">
          <path d="M715.8 488.4c-16.3-6.5-35.2 2.2-41.8 18.7C662.9 568.1 608.3 616 544.6 616c-111.1 0-201.5-89.4-201.5-200.5 0-111.1 90.4-200.5 201.5-200.5 51.2 0 98.8 20.3 134.8 53.6 8.1 6.6 20.1 7.7 28.1 2.4 8.1-5.3 11.4-15.6 6.1-23.7C655.4 183.6 583.7 144 511.3 144c-209 0-380.5 171.5-380.5 380.6 0 209.1 171.6 380.6 380.5 380.6 116.2 0 222.3-54.3 292.1-139.8 9.1-11 7-26.8-4.1-35.9z"></path>
          <path d="M808 357.3c-13.4-13.4-35.1-13.4-48.5 0l-120.1 120.1c-6.7 6.7-6.7 17.6 0 24.3l120.1 120.1c13.4 13.4 35.1 13.4 48.5 0s13.4-35.1 0-48.5L724.1 512l83.9-83.9c13.4-13.4 13.4-35.1 0-48.5z"></path>
        </svg>
        换一组
      </button>
    </div>

    <!-- 帮助按钮 -->
    <div class="help-button" @click="handleHelp">?</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeBlock = ref<number | null>(null)
const inputValue = ref('')

// 下拉菜单状态
const dropdownOpen = ref({
  cardCount: false,
  style: false,
  orientation: false,
  language: false
})

// 选中的值
const cardCount = ref(10)
const selectedStyle = ref('经典')
const selectedOrientation = ref('默认')
const selectedLanguage = ref('简体中文')

// 示例数据
const exampleList = ref<string[]>([
  "我从100多位首席执行官身上学到的时间管理秘诀",
  "为失去动力的创作者提供3个建议",
  "给'过于和蔼可亲'的教师的课堂管理建议",
  "Z世代营销失败，让你显得老气横秋",
  "从0到1000个订阅者：我希望拥有的路线图",
  "每个人都在做却没人在会议上承认的事"
])

// 页面加载时锁定当前页面对应的方块
onMounted(() => {
  activeBlock.value = 1 // 演示文稿页锁定第一个方块
})

// 点击其他地方关闭下拉菜单
onMounted(() => {
  document.addEventListener('click', () => {
    Object.keys(dropdownOpen.value).forEach(key => {
      dropdownOpen.value[key as keyof typeof dropdownOpen.value] = false
    })
  })
})

const handleBack = () => {
  router.back()
}

const handleBlockClick = (index: number) => {
  switch(index) {
    case 1: router.push('/generate'); break
    case 2: router.push('/generate/web'); break
    case 3: router.push('/generate/word'); break
    case 4: router.push('/generate/social'); break
  }
}

const handleBlockHover = (index: number) => {
  const blocks = document.querySelectorAll('.white-block')
  // 先移除所有hover类
  blocks.forEach(block => block.classList.remove('hover'))
  // 给当前hover的方块添加hover类（如果不是激活态）
  const targetBlock = blocks[index - 1]
  if (targetBlock && !targetBlock.classList.contains('active')) {
    targetBlock.classList.add('hover')
  }
}

const handleBlockLeave = () => {
  const blocks = document.querySelectorAll('.white-block')
  // 移除所有hover类
  blocks.forEach(block => block.classList.remove('hover'))
}



// 下拉菜单切换
const toggleDropdown = (menu: string) => {
  // 关闭其他所有下拉菜单
  Object.keys(dropdownOpen.value).forEach(key => {
    if (key !== menu) {
      dropdownOpen.value[key as keyof typeof dropdownOpen.value] = false
    }
  })
  // 切换当前菜单
  dropdownOpen.value[menu as keyof typeof dropdownOpen.value] = !dropdownOpen.value[menu as keyof typeof dropdownOpen.value]
}

// 选择卡片数量
const selectCardCount = (count: number) => {
  cardCount.value = count
  dropdownOpen.value.cardCount = false
  console.log('选择卡片数量:', count)
  // TODO: 调用后端API更新卡片数量
}

// 选择风格
const selectStyle = (style: string) => {
  selectedStyle.value = style
  dropdownOpen.value.style = false
  console.log('选择风格:', style)
  // TODO: 调用后端API更新风格
}

// 选择方向
const selectOrientation = (orientation: string) => {
  selectedOrientation.value = orientation
  dropdownOpen.value.orientation = false
  console.log('选择方向:', orientation)
  // TODO: 调用后端API更新方向
}

// 选择语言
const selectLanguage = (language: string) => {
  selectedLanguage.value = language
  dropdownOpen.value.language = false
  console.log('选择语言:', language)
  // TODO: 调用后端API更新语言
}

// 点击示例卡片，填充到输入框
const handleExampleClick = (example: string) => {
  inputValue.value = example
}

// 发送按钮点击事件
const handleSend = () => {
  if (inputValue.value.trim()) {
    console.log('发送内容:', inputValue.value)
    // TODO: 调用后端API发送内容
    alert(`发送: ${inputValue.value}`)
  }
}

// 换一组示例
const handleRefreshExample = async () => {
  try {
    const exampleGroups: string[][] = [
      ["我从100多位首席执行官身上学到的时间管理秘诀", "为失去动力的创作者提供3个建议", "给'过于和蔼可亲'的教师的课堂管理建议", "Z世代营销失败，让你显得老气横秋", "从0到1000个订阅者：我希望拥有的路线图", "每个人都在做却没人在会议上承认的事"],
      ["如何打造高转化的社交媒体内容矩阵", "短视频脚本创作的黄金法则", "私域流量运营的7个核心技巧", "爆款文案的底层逻辑拆解", "直播带货的节奏把控技巧", "内容创作的灵感获取方法"],
      ["职场沟通的高效表达技巧", "团队协作中的冲突解决策略", "远程办公的效率提升方法", "职场新人的快速成长指南", "管理者的激励员工技巧", "职业规划的5年规划法"]
    ]
    
    const randomIndex = Math.floor(Math.random() * exampleGroups.length)
    exampleList.value = exampleGroups[randomIndex] ?? exampleGroups[0] ?? []
    
  } catch (error) {
    console.error('换一组失败：', error)
  }
}

// 帮助按钮
const handleHelp = () => {
  alert('点击方块可切换页面，点击示例可填充输入框')
}
</script>

<style scoped>
.generate-page-container {
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
  overflow: hidden !important;
  position: fixed;
  top: 0;
  left: 0;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.button-group {
  position: absolute;
  top: 20px;
  left: 20px;
}

.outline-button {
  background: rgba(255,255,255,0.7);
  border: 1px solid rgba(255,255,255,0.7);
  border-radius: 6px;
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.title-main {
  font-size: 48px;
  color: #2c3e50;
  font-weight: bold;
  margin-bottom: 16px;
}

.title-sub {
  font-size: 18px;
  color: #34495e;
  margin-bottom: 40px;
}

.block-container {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  align-items: center;
}

.white-block {
  width: 180px;
  height: 100px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.white-block.active {
  border: 2px solid rgb(11, 167, 175);
  background-color: #f0f8ff;
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.2);
}

.white-block.hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border: 2px solid rgba(11, 167, 175, 0.5);
}

.white-block.active.hover {
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

.icon1 .block-icon,
.icon2 .block-icon,
.icon3 .block-icon,
.icon4 .block-icon {
  width: 40px;
  height: 40px;
  display: block;
}

.block-text {
  margin-top: 5px;
  font-size: 14px;
  color: #34495e;
  font-family: "Microsoft YaHei", sans-serif;
}

.white-block.active .block-text {
  color: #4ad0e2;
}

/* 下拉选择栏 */
.select-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
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
}

.select-arrow.rotated {
  transform: rotate(180deg);
}

.select-icon {
  color: #34495e;
}

/* 下拉菜单 */
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

/* 输入框容器（带发送按钮） */
.input-container {
  width: 60%;
  margin-bottom: 30px;
  position: relative;
  display: flex;
  align-items: center;
}

.main-input {
  width: 100%;
  padding: 16px 50px 16px 20px;
  border-radius: 30px;
  border: none;
  font-size: 16px;
  color: #34495e;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  outline: none;
  transition: all 0.2s ease;
}

.main-input:focus {
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.2);
}

.main-input::placeholder {
  color: #999;
}

/* 发送按钮 */
.send-button {
  position: absolute;
  right: 8px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgb(11, 167, 175);
  border: none;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.send-button:hover {
  background: rgb(8, 130, 136);
  transform: scale(1.05);
}

.send-button:active {
  transform: scale(0.95);
}

/* 示例提示区域 */
.example-section {
  width: 60%;
  max-width: 900px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.example-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
  position: relative;
  width: 100%;
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

/* 固定网格布局 */
.example-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
  width: 100%;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

/* 固定卡片样式 */
.example-card {
  background: rgba(255,255,255,0.8);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  cursor: pointer;
  transition: all 0.2s ease;
  
  /* 固定尺寸 */
  width: 100%;
  min-height: 80px;
  box-sizing: border-box;
}

.example-card:hover {
  background: rgba(255,255,255,1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* 内容区域 - 支持换行 */
.example-content {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 14px;
  color: #34495e;
  line-height: 1.5;
  
  /* 允许换行 */
  flex: 1;
  min-width: 0;
  word-wrap: break-word;
  word-break: break-word;
}

.example-text {
  white-space: normal;  /* 允许换行 */
  line-height: 1.5;
}

.example-icon {
  color: #34495e;
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  margin-top: 2px;
}

.example-add {
  font-size: 18px;
  color: #666;
  font-weight: bold;
  flex-shrink: 0;
  margin-left: 8px;
  width: 20px;
  text-align: center;
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  padding: 8px 16px;
  border-radius: 20px;
  border: none;
  font-size: 14px;
  color: #34495e;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
}

.refresh-button:hover {
  background: #f8f9fa;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.refresh-icon {
  color: #34495e;
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
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.2s ease;
  z-index: 1000;
}

.help-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
</style>