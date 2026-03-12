<!-- ProfilePage.vue - 无标题，内容自然居中，仅内容区可滚动 -->
<template>
  <div class="profile-container">
    <!-- 返回按钮 - 和其他页面一样固定在顶部 -->
    <div class="button-group">
      <button class="back-button outline-button icon-button" @click="goBack">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
    </div>

    <!-- 左右布局容器 - 垂直居中 -->
    <div class="profile-layout">
      <!-- 左侧导航 -->
      <div class="profile-sidebar">
        <!-- 用户信息卡片 -->
        <div class="user-card">
          <div class="user-avatar">
            <span class="iconfont icon-yonghu avatar-icon"></span>
          </div>
          <div class="user-info">
            <div class="user-name">{{ username || '未登录用户' }}</div>
            <div class="user-email">{{ userEmail || '暂无邮箱' }}</div>
          </div>
        </div>

        <!-- 导航菜单 -->
        <div class="nav-menu">
          <div 
            v-for="item in navItems" 
            :key="item.id"
            class="nav-item"
            :class="{ active: activeNav === item.id }"
            @click="activeNav = item.id"
          >
            <span :class="['iconfont', item.icon, 'nav-icon']"></span>
            <span class="nav-text">{{ item.name }}</span>
            <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
          </div>
        </div>

        <!-- 底部退出按钮 -->
        <div class="logout-btn" @click="handleLogout">
          <span class="iconfont icon-tuichu"></span>
          <span>退出登录</span>
        </div>
      </div>

      <!-- 右侧内容 - 唯一可滚动区域 -->
      <div class="profile-content">
        <div class="content-scroll">
          <!-- 个人资料 -->
          <div v-if="activeNav === 'profile'" class="content-section">
            <h2 class="section-title">个人资料</h2>
            
            <div class="profile-form">
              <div class="form-item">
                <label class="form-label">用户名</label>
                <input type="text" v-model="profileForm.username" class="form-input" placeholder="请输入用户名">
              </div>
              
              <div class="form-item">
                <label class="form-label">邮箱</label>
                <input type="email" v-model="profileForm.email" class="form-input" placeholder="请输入邮箱">
              </div>
              
              <div class="form-item">
                <label class="form-label">手机号</label>
                <input type="tel" v-model="profileForm.phone" class="form-input" placeholder="请输入手机号">
              </div>
              
              <div class="form-item">
                <label class="form-label">个人简介</label>
                <textarea v-model="profileForm.bio" class="form-textarea" placeholder="介绍一下自己..." rows="3"></textarea>
              </div>
              
              <button class="save-btn" @click="saveProfile">保存修改</button>
            </div>
          </div>

          <!-- 创作历史 -->
          <div v-if="activeNav === 'history'" class="content-section">
            <h2 class="section-title">创作历史</h2>
            
            <div class="stats-cards">
              <div class="stat-card">
                <div class="stat-value">{{ historyStats.total }}</div>
                <div class="stat-label">总创作数</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{{ historyStats.presentations }}</div>
                <div class="stat-label">演示文稿</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{{ historyStats.documents }}</div>
                <div class="stat-label">文档</div>
              </div>
            </div>

            <div class="history-filters">
              <button 
                class="filter-btn" 
                :class="{ active: historyFilter === 'all' }"
                @click="historyFilter = 'all'"
              >全部</button>
              <button 
                class="filter-btn" 
                :class="{ active: historyFilter === 'presentation' }"
                @click="historyFilter = 'presentation'"
              >演示文稿</button>
              <button 
                class="filter-btn" 
                :class="{ active: historyFilter === 'document' }"
                @click="historyFilter = 'document'"
              >文档</button>
            </div>

            <div class="history-list">
              <div v-for="item in filteredHistory" :key="item.id" class="history-item">
                <div class="history-item-left">
                  <span :class="['iconfont', item.type === 'presentation' ? 'icon-xinjian_PPTyanshiwengao' : 'icon-wendang', 'history-icon']"></span>
                  <div class="history-info">
                    <div class="history-title">{{ item.title }}</div>
                    <div class="history-meta">
                      <span>{{ item.date }}</span>
                      <span>· {{ item.type === 'presentation' ? '演示文稿' : '文档' }}</span>
                      <span>· {{ item.cardCount }}张卡片</span>
                    </div>
                  </div>
                </div>
                <div class="history-item-right">
                  <button class="history-btn" @click="editItem(item)">编辑</button>
                  <button class="history-btn" @click="downloadItem(item)">下载</button>
                  <button class="history-btn delete" @click="deleteItem(item)">删除</button>
                </div>
              </div>
            </div>
          </div>

          <!-- 帮助中心 -->
          <div v-if="activeNav === 'help'" class="content-section">
            <h2 class="section-title">帮助中心</h2>
            
            <div class="help-search">
              <span class="iconfont icon-sousuo search-icon"></span>
              <input type="text" v-model="helpSearch" placeholder="搜索帮助文档..." class="help-search-input">
            </div>

            <div class="help-categories">
              <div 
                v-for="cat in helpCategories" 
                :key="cat.id"
                class="help-category"
                :class="{ active: activeHelpCat === cat.id }"
                @click="activeHelpCat = cat.id"
              >
                <span :class="['iconfont', cat.icon, 'category-icon']"></span>
                <span>{{ cat.name }}</span>
              </div>
            </div>

            <div class="faq-list">
              <div v-for="(faq, index) in filteredFaqs" :key="index" class="faq-item">
                <div class="faq-question" @click="toggleFaq(index)">
                  <span class="faq-q">Q</span>
                  <span>{{ faq.question }}</span>
                  <span class="faq-arrow" :class="{ expanded: faq.expanded }">▼</span>
                </div>
                <div v-if="faq.expanded" class="faq-answer">
                  <span class="faq-a">A</span>
                  <span>{{ faq.answer }}</span>
                </div>
              </div>
            </div>

            <div class="contact-support">
              <div class="support-title">没找到想要的答案？</div>
              <div class="support-btns">
                <button class="support-btn" @click="contactEmail">
                  <span class="iconfont icon-email"></span>
                  邮件联系
                </button>
                <button class="support-btn" @click="contactChat">
                  <span class="iconfont icon-kefu"></span>
                  在线客服
                </button>
              </div>
            </div>
          </div>

          <!-- 关于我们 -->
          <div v-if="activeNav === 'about'" class="content-section">
            <h2 class="section-title">关于我们</h2>
            
            <div class="about-content">
              <div class="about-logo">
                <span class="iconfont icon-a-gongxiaoshanguangliangdian logo-icon"></span>
                <span class="about-version">AI创作助手 v1.0.0</span>
              </div>
              
              <div class="about-desc">
                AI创作助手是一款智能内容生成工具，帮助您快速创建专业的演示文稿和文档。
              </div>
              
              <div class="about-features">
                <div class="feature-item">
                  <span class="iconfont icon-xinjian_PPTyanshiwengao feature-icon"></span>
                  <div class="feature-text">
                    <div class="feature-title">AI智能生成</div>
                    <div class="feature-desc">基于先进AI模型，快速生成高质量内容</div>
                  </div>
                </div>
                <div class="feature-item">
                  <span class="iconfont icon-mobansheji feature-icon"></span>
                  <div class="feature-text">
                    <div class="feature-title">海量模板</div>
                    <div class="feature-desc">提供多种专业模板，满足不同场景需求</div>
                  </div>
                </div>
                <div class="feature-item">
                  <span class="iconfont icon-daoru feature-icon"></span>
                  <div class="feature-text">
                    <div class="feature-title">多格式支持</div>
                    <div class="feature-desc">支持PPT、Word、PDF等多种格式导入导出</div>
                  </div>
                </div>
              </div>
              
              <div class="about-links">
                <a href="#" @click.prevent>用户协议</a>
                <span class="link-divider">|</span>
                <a href="#" @click.prevent>隐私政策</a>
                <span class="link-divider">|</span>
                <a href="#" @click.prevent>版本更新</a>
              </div>
              
              <div class="about-copyright">
                © 2024 AI创作助手. All rights reserved.
              </div>
            </div>
          </div>

          <!-- 账号设置 -->
          <div v-if="activeNav === 'settings'" class="content-section">
            <h2 class="section-title">账号设置</h2>
            
            <div class="settings-group">
              <h3 class="settings-group-title">安全设置</h3>
              
              <div class="settings-item">
                <div class="settings-item-left">
                  <div class="settings-item-title">修改密码</div>
                  <div class="settings-item-desc">定期更换密码可以提高账号安全性</div>
                </div>
                <button class="settings-btn" @click="showChangePassword = true">修改</button>
              </div>
              
              <div class="settings-item">
                <div class="settings-item-left">
                  <div class="settings-item-title">绑定手机</div>
                  <div class="settings-item-desc">已绑定 {{ profileForm.phone || '未绑定' }}</div>
                </div>
                <button class="settings-btn" @click="bindPhone">{{ profileForm.phone ? '更换' : '绑定' }}</button>
              </div>
              
              <div class="settings-item">
                <div class="settings-item-left">
                  <div class="settings-item-title">绑定邮箱</div>
                  <div class="settings-item-desc">已绑定 {{ profileForm.email || '未绑定' }}</div>
                </div>
                <button class="settings-btn" @click="bindEmail">{{ profileForm.email ? '更换' : '绑定' }}</button>
              </div>
            </div>
            
            <div class="settings-group">
              <h3 class="settings-group-title">通知设置</h3>
              
              <div class="settings-item">
                <div class="settings-item-left">
                  <div class="settings-item-title">邮件通知</div>
                  <div class="settings-item-desc">接收产品更新、活动通知</div>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="settings.emailNotification">
                  <span class="slider"></span>
                </label>
              </div>
              
              <div class="settings-item">
                <div class="settings-item-left">
                  <div class="settings-item-title">消息提醒</div>
                  <div class="settings-item-desc">接收系统消息和提醒</div>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="settings.messageNotification">
                  <span class="slider"></span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 帮助按钮 -->
    <div class="help-button" @click="handleHelp">?</div>

    <!-- 修改密码弹窗 -->
    <div v-if="showChangePassword" class="modal-overlay" @click.self="showChangePassword = false">
      <div class="modal-content">
        <h3 class="modal-title">修改密码</h3>
        <input type="password" v-model="passwordForm.oldPassword" placeholder="原密码" class="modal-input">
        <input type="password" v-model="passwordForm.newPassword" placeholder="新密码" class="modal-input">
        <input type="password" v-model="passwordForm.confirmPassword" placeholder="确认新密码" class="modal-input">
        <div class="modal-btns">
          <button class="modal-btn cancel" @click="showChangePassword = false">取消</button>
          <button class="modal-btn confirm" @click="changePassword">确认</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

interface HistoryItem {
  id: number
  title: string
  type: 'presentation' | 'document'
  date: string
  cardCount: number
}

interface FAQ {
  question: string
  answer: string
  expanded: boolean
  category: string
}

const router = useRouter()
const route = useRoute()
const username = ref('')
const userEmail = ref('')
const activeNav = ref<string>('profile')
const helpSearch = ref('')
const activeHelpCat = ref<string>('all')
const showChangePassword = ref(false)
const historyFilter = ref<'all' | 'presentation' | 'document'>('all')
const hasMoreHistory = ref(true)

onMounted(() => {
  username.value = localStorage.getItem('username') || '未登录用户'
  
  const tab = route.query.tab as string
  if (tab && ['history', 'settings', 'help', 'about'].includes(tab)) {
    activeNav.value = tab
  }
})

interface NavItem {
  id: string
  name: string
  icon: string
  badge?: string
}

const navItems: NavItem[] = [
  { id: 'profile', name: '个人资料', icon: 'icon-yonghu' },
  { id: 'history', name: '创作历史', icon: 'icon-lishi', badge: '12' },
  { id: 'help', name: '帮助中心', icon: 'icon-bangzhu' },
  { id: 'about', name: '关于我们', icon: 'icon-guanyu' },
  { id: 'settings', name: '账号设置', icon: 'icon-shezhi' }
]

const profileForm = reactive({
  username: '',
  email: '',
  phone: '',
  bio: ''
})

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const settings = reactive({
  emailNotification: true,
  messageNotification: true
})

const historyStats = reactive({
  total: 28,
  presentations: 16,
  documents: 12
})

const historyList = ref<HistoryItem[]>([
  { id: 1, title: '2024年度销售总结汇报', type: 'presentation', date: '2024-03-15', cardCount: 12 },
  { id: 2, title: '产品发布会演讲文稿', type: 'presentation', date: '2024-03-14', cardCount: 8 },
  { id: 3, title: '市场调研分析报告', type: 'document', date: '2024-03-13', cardCount: 15 },
  { id: 4, title: '团队周报模板', type: 'document', date: '2024-03-12', cardCount: 6 },
  { id: 5, title: '投资者路演PPT', type: 'presentation', date: '2024-03-11', cardCount: 20 },
  { id: 6, title: '项目计划书', type: 'document', date: '2024-03-10', cardCount: 10 }
])

const filteredHistory = computed<HistoryItem[]>(() => {
  if (historyFilter.value === 'all') return historyList.value
  return historyList.value.filter(item => item.type === historyFilter.value)
})

interface HelpCategory {
  id: string
  name: string
  icon: string
}

const helpCategories: HelpCategory[] = [
  { id: 'all', name: '全部', icon: 'icon-quanbu' },
  { id: 'basic', name: '基础使用', icon: 'icon-jichu' },
  { id: 'advanced', name: '高级功能', icon: 'icon-gaoji' },
  { id: 'faq', name: '常见问题', icon: 'icon-wenti' },
  { id: 'tutorial', name: '教程指南', icon: 'icon-jiaocheng' }
]

const faqs = ref<FAQ[]>([
  { 
    question: '如何开始使用AI生成内容？', 
    answer: '在首页选择您想创作的类型（演示文稿或文档），然后输入提示词或粘贴内容，点击发送即可开始生成。',
    expanded: false,
    category: 'basic'
  },
  { 
    question: '支持哪些文件格式导入？', 
    answer: '目前支持导入PPTX、DOCX、PDF格式文件，以及Google Drive文档和网页URL。',
    expanded: false,
    category: 'basic'
  },
  { 
    question: '生成的內容可以导出为什么格式？', 
    answer: '生成的演示文稿可以导出为PPTX格式，文档可以导出为DOCX格式，同时也支持PDF导出。',
    expanded: false,
    category: 'basic'
  },
  { 
    question: '如何查看我的创作历史？', 
    answer: '在个人中心的"创作历史"选项卡中，您可以查看所有历史生成的文档和演示文稿。',
    expanded: false,
    category: 'faq'
  },
  { 
    question: 'AI生成的内容版权归谁所有？', 
    answer: '您生成的内容版权归您所有，您可以自由使用、修改和分发。',
    expanded: false,
    category: 'faq'
  },
  { 
    question: '如何提高生成内容的质量？', 
    answer: '提供更详细、更具体的提示词，选择合适的内容类型和语气风格，可以显著提高生成内容的质量。',
    expanded: false,
    category: 'advanced'
  }
])

const filteredFaqs = computed<FAQ[]>(() => {
  let filtered = faqs.value
  
  if (activeHelpCat.value !== 'all') {
    filtered = filtered.filter(faq => faq.category === activeHelpCat.value)
  }
  
  if (helpSearch.value && helpSearch.value.trim() !== '') {
    const search = helpSearch.value.toLowerCase().trim()
    filtered = filtered.filter(faq => {
      const question = faq.question?.toLowerCase() || ''
      const answer = faq.answer?.toLowerCase() || ''
      return question.includes(search) || answer.includes(search)
    })
  }
  
  return filtered
})

const toggleFaq = (index: number) => {
  if (faqs.value[index]) {
    faqs.value[index].expanded = !faqs.value[index].expanded
  }
}

const goBack = () => {
  router.back()
}

const saveProfile = () => {
  alert('资料保存成功！')
}

const editItem = (item: HistoryItem) => {
  router.push(`/editor/${item.id}`)
}

const downloadItem = (item: HistoryItem) => {
  alert(`开始下载：${item.title}`)
}

const deleteItem = (item: HistoryItem) => {
  if (confirm(`确定要删除"${item.title}"吗？`)) {
    historyList.value = historyList.value.filter(i => i.id !== item.id)
  }
}

const loadMoreHistory = () => {
  setTimeout(() => {
    hasMoreHistory.value = false
  }, 1000)
}

const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    localStorage.removeItem('isLoggedIn')
    localStorage.removeItem('username')
    router.push('/')
  }
}

const bindPhone = () => {
  alert('绑定手机功能开发中')
}

const bindEmail = () => {
  alert('绑定邮箱功能开发中')
}

const changePassword = () => {
  if (!passwordForm.oldPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) {
    alert('请填写所有字段')
    return
  }
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    alert('新密码与确认密码不一致')
    return
  }
  alert('密码修改成功！')
  showChangePassword.value = false
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
}

const contactEmail = () => {
  window.location.href = 'mailto:support@aicreator.com'
}

const contactChat = () => {
  alert('在线客服功能开发中')
}

const handleHelp = () => {
  alert('个人中心：管理您的账号、查看创作历史和获取帮助')
}
</script>

<style scoped>
/* 强制全局无滚动 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  overflow: hidden !important;
  height: 100vh !important;
  width: 100vw !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
}

.profile-container {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(
    135deg,
    rgba(240, 248, 255, 0.8) 0%,
    rgba(230, 245, 250, 0.9) 50%,
    rgba(220, 240, 245, 0.8) 100%
  );
  position: fixed;
  top: 0;
  left: 0;
  overflow: hidden;
  /* 使用flex让内容垂直居中 */
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.button-group {
  position: absolute;
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

/* 布局容器 - 垂直居中，左右留白 */
.profile-layout {
  display: flex;
  gap: 24px;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  height: 80vh; /* 固定高度为视口的80%，自然居中 */
  overflow: hidden;
  padding: 0 20px;
}

/* 左侧导航 - 固定 */
.profile-sidebar {
  width: 280px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  flex-shrink: 0;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-icon {
  font-size: 32px;
  color: white;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 18px;
  font-weight: 600;
  color: #1e3c5c;
  margin-bottom: 4px;
}

.user-email {
  font-size: 13px;
  color: #6e7781;
}

.nav-menu {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 20px;
}

.nav-menu::-webkit-scrollbar {
  width: 4px;
}

.nav-menu::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

.nav-menu::-webkit-scrollbar-thumb {
  background: rgba(11, 167, 175, 0.3);
  border-radius: 10px;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 4px;
}

.nav-item:hover {
  background: rgba(11, 167, 175, 0.1);
}

.nav-item.active {
  background: rgba(11, 167, 175, 0.15);
  color: rgb(11, 167, 175);
}

.nav-icon {
  font-size: 20px;
  margin-right: 12px;
  color: #71cdd1;
}

.nav-item.active .nav-icon {
  color: rgb(11, 167, 175);
}

.nav-text {
  font-size: 15px;
  font-weight: 500;
  flex: 1;
}

.nav-badge {
  background: rgb(11, 167, 175);
  color: white;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 12px;
}

.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border-radius: 10px;
  background: rgba(255, 99, 99, 0.1);
  color: #ff6b6b;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 99, 99, 0.2);
}

.logout-btn:hover {
  background: rgba(255, 99, 99, 0.2);
}

/* 右侧内容 - 固定，仅内部滚动 */
.profile-content {
  flex: 1;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  height: 100%;
  overflow: hidden;
}

/* 唯一可滚动的区域 */
.content-scroll {
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 8px;
}

.content-scroll::-webkit-scrollbar {
  width: 6px;
}

.content-scroll::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

.content-scroll::-webkit-scrollbar-thumb {
  background: rgba(11, 167, 175, 0.3);
  border-radius: 10px;
}

.content-scroll::-webkit-scrollbar-thumb:hover {
  background: rgba(11, 167, 175, 0.5);
}

.content-section {
  width: 100%;
}

.section-title {
  font-size: 24px;
  color: #1e3c5c;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid rgba(11, 167, 175, 0.2);
}

/* 以下样式保持不变... */
.profile-form {
  max-width: 600px;
}

.form-item {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 14px;
  color: #4a5568;
  margin-bottom: 6px;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  font-size: 14px;
  transition: all 0.2s ease;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: rgb(11, 167, 175);
  box-shadow: 0 0 0 3px rgba(11, 167, 175, 0.1);
}

.form-textarea {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  font-size: 14px;
  transition: all 0.2s ease;
  background: white;
  resize: none;
  font-family: inherit;
}

.save-btn {
  background: rgb(11, 167, 175);
  color: white;
  border: none;
  border-radius: 30px;
  padding: 10px 28px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.save-btn:hover {
  background: rgb(8, 130, 136);
  transform: scale(1.02);
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.stat-card {
  background: white;
  border-radius: 10px;
  padding: 15px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: rgb(11, 167, 175);
  margin-bottom: 2px;
}

.stat-label {
  font-size: 13px;
  color: #6e7781;
}

.history-filters {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}

.filter-btn {
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: white;
  font-size: 13px;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn.active {
  background: rgb(11, 167, 175);
  color: white;
  border-color: rgb(11, 167, 175);
}

.history-list {
  max-height: 300px;
  overflow-y: auto;
  padding-right: 4px;
}

.history-list::-webkit-scrollbar {
  width: 4px;
}

.history-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

.history-list::-webkit-scrollbar-thumb {
  background: rgba(11, 167, 175, 0.3);
  border-radius: 10px;
}

.history-item {
  background: white;
  border-radius: 10px;
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.history-item-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.history-icon {
  font-size: 22px;
  color: #71cdd1;
}

.history-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.history-title {
  font-size: 15px;
  font-weight: 600;
  color: #1e3c5c;
}

.history-meta {
  font-size: 12px;
  color: #6e7781;
  display: flex;
  gap: 6px;
}

.history-item-right {
  display: flex;
  gap: 6px;
}

.history-btn {
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: white;
  font-size: 12px;
  color: #4a5568;
  cursor: pointer;
}

.history-btn.delete:hover {
  background: #fff0f0;
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.help-search {
  position: relative;
  margin-bottom: 16px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 14px;
}

.help-search-input {
  width: 100%;
  padding: 10px 10px 10px 36px;
  border-radius: 30px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  font-size: 14px;
  background: white;
}

.help-categories {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.help-category {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 30px;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.1);
  font-size: 13px;
  color: #4a5568;
  cursor: pointer;
}

.help-category.active {
  background: rgb(11, 167, 175);
  color: white;
  border-color: rgb(11, 167, 175);
}

.category-icon {
  font-size: 14px;
}

.faq-list {
  max-height: 250px;
  overflow-y: auto;
  margin-bottom: 16px;
  padding-right: 4px;
}

.faq-list::-webkit-scrollbar {
  width: 4px;
}

.faq-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

.faq-list::-webkit-scrollbar-thumb {
  background: rgba(11, 167, 175, 0.3);
  border-radius: 10px;
}

.faq-item {
  background: white;
  border-radius: 10px;
  margin-bottom: 8px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.faq-question {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.faq-q {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgb(11, 167, 175);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.faq-arrow {
  margin-left: auto;
  font-size: 10px;
  color: #999;
  transition: transform 0.3s ease;
}

.faq-arrow.expanded {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 16px 12px 48px;
  display: flex;
  gap: 10px;
  color: #4a5568;
  font-size: 13px;
  line-height: 1.5;
  background: #f8f9fa;
}

.faq-a {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #ff9800;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.contact-support {
  text-align: center;
  padding: 20px;
  background: rgba(11, 167, 175, 0.05);
  border-radius: 12px;
}

.support-title {
  font-size: 16px;
  color: #1e3c5c;
  margin-bottom: 16px;
  font-weight: 600;
}

.support-btns {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.support-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 20px;
  border-radius: 30px;
  border: 1px solid rgba(11, 167, 175, 0.3);
  background: white;
  font-size: 14px;
  color: rgb(11, 167, 175);
  cursor: pointer;
}

.support-btn:hover {
  background: rgb(11, 167, 175);
  color: white;
}

.about-content {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.about-logo {
  margin-bottom: 20px;
}

.logo-icon {
  font-size: 60px;
  color: rgb(11, 167, 175);
  display: block;
  margin-bottom: 8px;
}

.about-version {
  font-size: 13px;
  color: #6e7781;
  background: rgba(11, 167, 175, 0.1);
  padding: 3px 10px;
  border-radius: 20px;
}

.about-desc {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 20px;
  padding: 0 15px;
}

.about-features {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
  text-align: left;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: white;
  border-radius: 10px;
}

.feature-icon {
  font-size: 24px;
  color: rgb(11, 167, 175);
}

.feature-text {
  flex: 1;
}

.feature-title {
  font-size: 15px;
  font-weight: 600;
  color: #1e3c5c;
  margin-bottom: 2px;
}

.feature-desc {
  font-size: 12px;
  color: #6e7781;
}

.settings-group {
  margin-bottom: 20px;
}

.settings-group-title {
  font-size: 16px;
  color: #1e3c5c;
  margin-bottom: 12px;
  font-weight: 600;
}

.settings-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: white;
  border-radius: 10px;
  margin-bottom: 6px;
}

.settings-item-left {
  flex: 1;
}

.settings-item-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e3c5c;
  margin-bottom: 2px;
}

.settings-item-desc {
  font-size: 12px;
  color: #6e7781;
}

.settings-btn {
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid rgba(11, 167, 175, 0.3);
  background: white;
  font-size: 13px;
  color: rgb(11, 167, 175);
  cursor: pointer;
}

.settings-btn:hover {
  background: rgb(11, 167, 175);
  color: white;
}

.switch {
  position: relative;
  display: inline-block;
  width: 46px;
  height: 22px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 22px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: rgb(11, 167, 175);
}

input:checked + .slider:before {
  transform: translateX(24px);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 24px;
  width: 360px;
  max-width: 90%;
}

.modal-title {
  font-size: 18px;
  color: #1e3c5c;
  margin-bottom: 16px;
  text-align: center;
}

.modal-input {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  font-size: 14px;
  margin-bottom: 12px;
}

.modal-btns {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 16px;
}

.modal-btn {
  padding: 8px 18px;
  border-radius: 8px;
  border: none;
  font-size: 13px;
  cursor: pointer;
}

.modal-btn.cancel {
  background: #f0f0f0;
  color: #666;
}

.modal-btn.confirm {
  background: rgb(11, 167, 175);
  color: white;
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
  z-index: 1000;
}

.help-button:hover {
  transform: scale(1.05);
}

@media (max-width: 1024px) {
  .profile-layout {
    flex-direction: column;
    height: 90vh; /* 小屏幕时更高一些 */
  }
  
  .profile-sidebar {
    width: 100%;
    height: 280px;
    margin-bottom: 16px;
  }
  
  .profile-content {
    height: calc(100% - 296px);
  }
}
</style>