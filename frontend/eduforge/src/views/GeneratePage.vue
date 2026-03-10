<template>
  <div class="generate-page-container">
    <!-- 返回按钮 -->
    <div class="button-group">
      <button class="back-button outline-button icon-button" @click="handleBack">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
    </div>

    <div class="title-main">生成</div>
    <div class="title-sub">您今天想创作什么？</div>
    
    <!-- 两个方块：演示文稿和文档 -->
    <div class="block-container">
      <!-- 1 演示文稿 -->
      <div class="white-block block-item" 
           :class="{ active: activeBlock === 1 }"
           @click="handleBlockClick(1)">
        <div class="icon-wrapper">
          <span class="iconfont icon-xinjian_PPTyanshiwengao block-icon"></span>
        </div>
        <div class="block-text">演示文稿</div>
      </div>

      <!-- 2 文档 -->
      <div class="white-block block-item" 
           :class="{ active: activeBlock === 2 }"
           @click="handleBlockClick(2)">
        <div class="icon-wrapper">
          <span class="iconfont icon-wendang block-icon"></span>
        </div>
        <div class="block-text">文档</div>
      </div>
    </div>

    <!-- 下拉选择栏（去掉风格和方向） -->
    <div class="select-bar">
      <!-- 卡片数量下拉 -->
      <div class="select-item" @click.stop="toggleDropdown('cardCount')">
        <span>{{ cardCount }}张卡片</span>
        <span class="iconfont icon-xiala select-arrow" :class="{ rotated: dropdownOpen.cardCount }"></span>
        <div v-if="dropdownOpen.cardCount" class="dropdown-menu">
          <div class="dropdown-item" @click.stop="selectCardCount(5)">5张卡片</div>
          <div class="dropdown-item" @click.stop="selectCardCount(10)">10张卡片</div>
          <div class="dropdown-item" @click.stop="selectCardCount(15)">15张卡片</div>
          <div class="dropdown-item" @click.stop="selectCardCount(20)">20张卡片</div>
        </div>
      </div>

      <!-- 语言下拉 -->
      <div class="select-item" @click.stop="toggleDropdown('language')">
        <span class="iconfont icon-yuyan select-icon"></span>
        <span>{{ selectedLanguage }}</span>
        <span class="iconfont icon-xiala select-arrow" :class="{ rotated: dropdownOpen.language }"></span>
        <div v-if="dropdownOpen.language" class="dropdown-menu">
          <div class="dropdown-item" @click.stop="selectLanguage('简体中文')">简体中文</div>
          <div class="dropdown-item" @click.stop="selectLanguage('繁体中文')">繁体中文</div>
          <div class="dropdown-item" @click.stop="selectLanguage('English')">English</div>
          <div class="dropdown-item" @click.stop="selectLanguage('日本語')">日本語</div>
        </div>
      </div>
    </div>

    <!-- 大输入框 -->
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

    <!-- 示例提示区域 -->
    <div class="example-section">
      <div class="example-title">示例提示</div>
      <div class="example-grid">
        <div class="example-card" v-for="(example, index) in exampleList" :key="index" @click="handleExampleClick(example)">
          <div class="example-content">
            <span class="iconfont icon-a-gongxiaoshanguangliangdian example-icon"></span>
            <span class="example-text">{{ example }}</span>
          </div>
          <div class="example-add">+</div>
        </div>
      </div>
      <button class="refresh-button" @click="handleRefreshExample">
        <span class="iconfont icon-xiala refresh-icon" style="transform: rotate(90deg);"></span>
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

// 新增：补充master代码中用到的selectedStyle变量（避免报错）
const selectedStyle = ref('默认风格')

const dropdownOpen = ref({
  cardCount: false,
  language: false
})

const cardCount = ref(10)
const selectedLanguage = ref('简体中文')

const exampleList = ref<string[]>([
  "我从100多位首席执行官身上学到的时间管理秘诀",
  "为失去动力的创作者提供3个建议",
  "给'过于和蔼可亲'的教师的课堂管理建议",
  "从0到1000个订阅者：我希望拥有的路线图",
  "每个人都在做却没人在会议上承认的事",
  "职场沟通的高效表达技巧"
])

onMounted(() => {
  activeBlock.value = 1
})

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
    case 2: router.push('/generate/word'); break
    default: break
  }
}

const toggleDropdown = (menu: string) => {
  Object.keys(dropdownOpen.value).forEach(key => {
    if (key !== menu) {
      dropdownOpen.value[key as keyof typeof dropdownOpen.value] = false
    }
  })
  dropdownOpen.value[menu as keyof typeof dropdownOpen.value] = !dropdownOpen.value[menu as keyof typeof dropdownOpen.value]
}

const selectCardCount = (count: number) => {
  cardCount.value = count
  dropdownOpen.value.cardCount = false
}

const selectLanguage = (language: string) => {
  selectedLanguage.value = language
  dropdownOpen.value.language = false
}

const handleExampleClick = (example: string) => {
  // 如果输入框不是“正在生成”的状态，才允许填充
  if (!inputValue.value.includes("正在")) {
    inputValue.value = example
  }
}

// 发送按钮点击事件（整合版：保留你的基础校验 + master的后端对接逻辑）
const handleSend = async () => {
  // 保留你的核心校验：输入为空不执行
  if (!inputValue.value.trim()) {
    console.log('发送内容为空，不执行');
    return;
  }

  // 新增校验：没选方块（演示文稿/网页等），提示用户
  if (activeBlock.value === null) {
    alert("请先选择要生成的内容类型（演示文稿/文档）！");
    return;
  }

  const userPrompt = inputValue.value
  const currentBlock = activeBlock.value
  
  // 1. 状态提示
  inputValue.value = "正在构思中..."

  try {
    // 2. 构造 URL 参数 (匹配后端 python 函数的参数名)
    const params = new URLSearchParams({
      subject: `主题:${userPrompt} | 风格:${selectedStyle.value} | 数量:${cardCount.value}`,
      task_type: "outline", // 后端默认值
      refined_outline: "",  // 后端默认值
      mode: "dify"          // 强制走后端 dify 逻辑
    })

    // 3. 发起请求 (注意：路径要拼上 main.py 挂载的 /api/v1)
    const response = await fetch(`http://localhost:8000/api/v1/generate-content?${params.toString()}`, {
      method: 'POST',
      headers: {
        // 如果你的系统需要登录，请取消下面注释并确保 localStorage 有 token
        // 'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })

    if (!response.ok) throw new Error('服务器响应失败')
    if (!response.body) return

    // 4. 处理流式数据 (实现打字机效果)
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    inputValue.value = "" // 清空状态提示，准备接收文字

    while (true) {
      const { done, value } = await reader.read()
      if (done) break;
      
      // 解码并实时追加到输入框
      const chunk = decoder.decode(value, { stream: true })
      inputValue.value += chunk
    }

  } catch (error) {
    console.error("对接异常:", error)
    alert("生成失败，请检查后端服务是否启动")
    inputValue.value = userPrompt // 失败时恢复用户原输入
  }
}

const handleRefreshExample = () => {
  const exampleGroups: string[][] = [
    ["我从100多位首席执行官身上学到的时间管理秘诀", "为失去动力的创作者提供3个建议", "给'过于和蔼可亲'的教师的课堂管理建议", "从0到1000个订阅者：我希望拥有的路线图", "每个人都在做却没人在会议上承认的事", "职场沟通的高效表达技巧"],
    ["如何打造高转化的内容矩阵", "团队协作中的冲突解决策略", "远程办公的效率提升方法", "职场新人的快速成长指南", "管理者的激励员工技巧", "职业规划的5年规划法"],
    ["人工智能在办公中的应用", "机器学习入门指南", "深度学习框架对比", "自然语言处理基础", "计算机视觉应用", "强化学习实战"]
  ]
  
  const randomIndex = Math.floor(Math.random() * exampleGroups.length)
  exampleList.value = exampleGroups[randomIndex] ?? exampleGroups[0] ?? []
}

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
  color: #34495e;
  transition: all 0.2s ease;
}

.outline-button:hover {
  background: rgba(255,255,255,0.9);
  transform: scale(1.05);
}

.title-main {
  font-size: 48px;
  color: #2c3e50;
  font-weight: bold;
  margin-bottom: 16px;
  margin-top:10px;
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
  justify-content: center;
}

.white-block {
  width: 180px;
  height: 100px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.white-block.active {
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

.block-icon {
  font-size: 40px;
  color: #71cdd1;
}

.white-block.active .block-icon {
  color: #4ad0e2;
}

.block-text {
  margin-top: 5px;
  font-size: 14px;
  color: #34495e;
}

.white-block.active .block-text {
  color: #4ad0e2;
}

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
  font-size: 12px;
}

.select-arrow.rotated {
  transform: rotate(180deg);
}

.select-icon {
  color: #34495e;
  font-size: 16px;
}

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

.example-card {
  background: rgba(255,255,255,0.8);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  min-height: 80px;
  box-sizing: border-box;
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
  min-width: 0;
  word-wrap: break-word;
  word-break: break-word;
}

.example-icon {
  color: #34495e;
  flex-shrink: 0;
  font-size: 16px;
  margin-top: 2px;
}

.example-text {
  white-space: normal;
  line-height: 1.5;
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
  font-size: 14px;
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