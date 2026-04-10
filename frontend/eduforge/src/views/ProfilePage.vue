<!-- ProfilePage.vue - 完整版，页面标题添加图标 -->
<template>
  <div class="profile-container">
    <!-- 左右布局容器 - 垂直居中 -->
    <div class="profile-layout">
      <!-- 左侧导航 -->
      <div class="profile-sidebar">
        <!-- 用户信息卡片 - 可点击上传头像 -->
        <div class="user-card">
          <div class="user-avatar">
            <img v-if="avatarUrl" :src="avatarUrl" class="avatar-img" />
            <span v-else class="iconfont icon-touxiang avatar-icon"></span>
          </div>
          <div class="user-info">
            <div class="user-name">{{ profileForm.username || '未登录用户' }}</div>
            <div class="user-email">{{ profileForm.email || '暂无邮箱' }}</div>
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
          <!-- 个人资料 - 这里放头像上传 -->
          <div v-if="activeNav === 'profile'" class="content-section">
            <h2 class="section-title">
              <span class="iconfont icon-touxiang section-icon"></span>
              个人资料
            </h2>
            
            <!-- 头像上传区域 -->
            <div class="avatar-upload-section" @click="triggerAvatarUpload">
              <div class="avatar-preview">
                <img v-if="avatarUrl" :src="avatarUrl" class="avatar-preview-img" />
                <span v-else class="iconfont icon-touxiang avatar-placeholder"></span>
                <div class="avatar-upload-overlay">
                  <span class="iconfont icon-shangchuan"></span>
                  <span>点击上传头像</span>
                </div>
              </div>
            </div>
            
            <!-- 隐藏的文件上传输入框 -->
            <input 
              type="file" 
              ref="avatarInput" 
              class="hidden-input" 
              accept="image/*"
              @change="handleAvatarUpload"
            />

            <div class="profile-form">
              <div class="form-item">
                <label class="form-label">用户名</label>
                <input type="text" v-model="profileForm.username" class="form-input" placeholder="请输入用户名" @blur="saveUsername">
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
            <h2 class="section-title">
              <span class="iconfont icon-wenjian section-icon"></span>
              创作历史
            </h2>
            
            <div class="stats-cards">
              <div class="stat-card">
                <div class="stat-value">{{ historyStats.total }}</div>
                <div class="stat-label">总创作数</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{{ historyStats.ppt }}</div>
                <div class="stat-label">PPT课件</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{{ historyStats.lesson }}</div>
                <div class="stat-label">教案</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{{ historyStats.gif }}</div>
                <div class="stat-label">教学GIF</div>
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
                :class="{ active: historyFilter === 'ppt' }"
                @click="historyFilter = 'ppt'"
              >PPT课件</button>
              <button 
                class="filter-btn" 
                :class="{ active: historyFilter === 'lesson' }"
                @click="historyFilter = 'lesson'"
              >教案</button>
              <button 
                class="filter-btn" 
                :class="{ active: historyFilter === 'gif' }"
                @click="historyFilter = 'gif'"
              >教学GIF</button>
            </div>

            <div class="history-list">
              <div v-for="item in filteredHistory" :key="item.id" class="history-item">
                <div class="history-item-left">
                  <span :class="['iconfont', getHistoryIcon(item.type), 'history-icon']"></span>
                  <div class="history-info">
                    <div class="history-title">{{ item.title }}</div>
                    <div class="history-meta">
                      <span>{{ item.date }}</span>
                      <span>· {{ getHistoryTypeName(item.type) }}</span>
                      <span v-if="item.type === 'ppt'">· {{ item.slideCount }}页</span>
                      <span v-else-if="item.type === 'lesson'">· {{ item.stepCount }}环节</span>
                      <span v-else-if="item.type === 'gif'">· {{ item.frameCount }}帧</span>
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

          <!-- 帮助中心 - 标题带客服图标 -->
          <div v-if="activeNav === 'help'" class="content-section">
            <h2 class="section-title">
              <span class="iconfont icon-kefu section-icon"></span>
              帮助中心
            </h2>
            
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
                  <span class="iconfont icon-icon-youxiang"></span>
                  邮件联系
                </button>
                <button class="support-btn" @click="contactChat">
                  <span class="iconfont icon-kefu"></span>
                  在线客服
                </button>
              </div>
            </div>
          </div>

          <!-- 关于我们 - 标题带关于图标 -->
          <div v-if="activeNav === 'about'" class="content-section">
            <h2 class="section-title">
              <span class="iconfont icon-guanyu_o section-icon"></span>
              关于我们
            </h2>
            
            <div class="about-content">
              <div class="about-logo">
                <span class="iconfont icon-a-gongxiaoshanguangliangdian logo-icon"></span>
                <span class="about-version">教学智能体 v1.0.0</span>
              </div>
              
              <div class="about-desc">
                教学智能体是一款专业的教学辅助工具，帮助教师快速创建PPT课件、编写教案、制作教学GIF动画。
              </div>
              
              <div class="about-features">
                <div class="feature-item">
                  <span class="iconfont icon-xinjian_PPTyanshiwengao feature-icon"></span>
                  <div class="feature-text">
                    <div class="feature-title">PPT课件生成</div>
                    <div class="feature-desc">输入主题，自动生成精美课件，支持多种模板</div>
                  </div>
                </div>
                <div class="feature-item">
                  <span class="iconfont icon-wendang feature-icon"></span>
                  <div class="feature-text">
                    <div class="feature-title">教案编写</div>
                    <div class="feature-desc">根据教学目标，生成完整教案，包含教学目标、重难点、教学过程</div>
                  </div>
                </div>
                <div class="feature-item">
                  <span class="iconfont icon-gif feature-icon"></span>
                  <div class="feature-text">
                    <div class="feature-title">教学GIF制作</div>
                    <div class="feature-desc">将抽象概念转化为生动的动画演示，支持多帧编辑</div>
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
                © 2024 教学智能体. All rights reserved.
              </div>
            </div>
          </div>

          <!-- 账号设置 - 标题带设置图标 -->
          <div v-if="activeNav === 'settings'" class="content-section">
            <h2 class="section-title">
              <span class="iconfont icon-shezhi section-icon"></span>
              账号设置
            </h2>
            
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
  type: 'ppt' | 'lesson' | 'gif'
  date: string
  slideCount?: number
  stepCount?: number
  frameCount?: number
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
const avatarUrl = ref('')
const avatarInput = ref<HTMLInputElement | null>(null)
const activeNav = ref<string>('profile')
const helpSearch = ref('')
const activeHelpCat = ref<string>('all')
const showChangePassword = ref(false)
const historyFilter = ref<'all' | 'ppt' | 'lesson' | 'gif'>('all')
const hasMoreHistory = ref(true)

// 从localStorage加载用户数据
onMounted(() => {
  const savedUsername = localStorage.getItem('username') || '未登录用户'
  username.value = savedUsername
  
  const savedAvatar = localStorage.getItem('userAvatar')
  if (savedAvatar) {
    avatarUrl.value = savedAvatar
  }
  
  // 初始化表单
  profileForm.username = savedUsername
  
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
  { id: 'profile', name: '个人资料', icon: 'icon-touxiang' },
  { id: 'history', name: '创作历史', icon: 'icon-wenjian', badge: '12' },
  { id: 'help', name: '帮助中心', icon: 'icon-kefu' },
  { id: 'about', name: '关于我们', icon: 'icon-guanyu_o' },
  { id: 'settings', name: '账号设置', icon: 'icon-shezhi' }
]

const profileForm = reactive({
  username: 'ELK',
  email: 'meng.archi6829@gmail.com',
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
  ppt: 12,
  lesson: 8,
  gif: 8
})

const historyList = ref<HistoryItem[]>([
  { id: 1, title: '分数初步认识', type: 'ppt', date: '2024-03-15', slideCount: 12 },
  { id: 2, title: '光合作用教案', type: 'lesson', date: '2024-03-14', stepCount: 8 },
  { id: 3, title: '细胞分裂过程', type: 'gif', date: '2024-03-13', frameCount: 15 },
  { id: 4, title: '勾股定理证明', type: 'ppt', date: '2024-03-12', slideCount: 6 },
  { id: 5, title: '英语现在完成时', type: 'lesson', date: '2024-03-11', stepCount: 10 },
  { id: 6, title: '地球公转演示', type: 'gif', date: '2024-03-10', frameCount: 8 }
])

const filteredHistory = computed<HistoryItem[]>(() => {
  if (historyFilter.value === 'all') return historyList.value
  return historyList.value.filter(item => item.type === historyFilter.value)
})

const getHistoryIcon = (type: string) => {
  switch(type) {
    case 'ppt': return 'icon-xinjian_PPTyanshiwengao'
    case 'lesson': return 'icon-wendang'
    case 'gif': return 'icon-gif'
    default: return 'icon-wenjian'
  }
}

const getHistoryTypeName = (type: string) => {
  switch(type) {
    case 'ppt': return 'PPT课件'
    case 'lesson': return '教案'
    case 'gif': return '教学GIF'
    default: return '文档'
  }
}

interface HelpCategory {
  id: string
  name: string
  icon: string
}

const helpCategories: HelpCategory[] = [
  { id: 'all', name: '全部', icon: 'icon-sousuo' },
  { id: 'ppt', name: 'PPT课件', icon: 'icon-xinjian_PPTyanshiwengao' },
  { id: 'lesson', name: '教案', icon: 'icon-wendang' },
  { id: 'gif', name: '教学GIF', icon: 'icon-gif' },
  { id: 'account', name: '账号问题', icon: 'icon-touxiang' }
]

const faqs = ref<FAQ[]>([
  { 
    question: '如何生成PPT课件？', 
    answer: '在首页选择"生成PPT课件"，输入主题或上传教材，AI会自动生成精美的PPT课件，包含多页内容和步骤。',
    expanded: false,
    category: 'ppt'
  },
  { 
    question: '如何编写教案？', 
    answer: '在首页选择"编写教案"，输入教学目标和内容，AI会生成完整的教案，包括教学目标、重难点、教学过程等。',
    expanded: false,
    category: 'lesson'
  },
  { 
    question: '如何制作教学GIF？', 
    answer: '在首页选择"制作教学GIF"，输入想要演示的概念，AI会生成多帧动画，您可以编辑每一帧的内容。',
    expanded: false,
    category: 'gif'
  },
  { 
    question: '如何查看创作历史？', 
    answer: '在个人中心的"创作历史"选项卡中，您可以查看所有历史生成的PPT、教案和GIF，并可以继续编辑。',
    expanded: false,
    category: 'account'
  },
  { 
    question: '如何修改头像和用户名？', 
    answer: '在个人中心的"个人资料"页面，点击头像可以上传新头像，在表单中可以修改用户名和其他信息。',
    expanded: false,
    category: 'account'
  },
  { 
    question: '如何导出已生成的内容？', 
    answer: '在编辑器中点击"导出"按钮，可以选择导出为PPTX、PDF、GIF等格式。',
    expanded: false,
    category: 'ppt'
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

const triggerAvatarUpload = () => {
  avatarInput.value?.click()
}

const handleAvatarUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  
  if (!file) return
  
  if (!file.type.startsWith('image/')) {
    alert('请上传图片文件')
    return
  }
  
  if (file.size > 2 * 1024 * 1024) {
    alert('图片大小不能超过2MB')
    return
  }
  
  const reader = new FileReader()
  reader.onload = (e) => {
    const result = e.target?.result as string
    avatarUrl.value = result
    localStorage.setItem('userAvatar', result)
    alert('头像上传成功！')
  }
  reader.readAsDataURL(file)
}

const saveUsername = () => {
  if (profileForm.username) {
    localStorage.setItem('username', profileForm.username)
    username.value = profileForm.username
  }
}

const saveProfile = () => {
  if (profileForm.username) {
    localStorage.setItem('username', profileForm.username)
    username.value = profileForm.username
  }
  alert('资料保存成功！')
}

const editItem = (item: HistoryItem) => {
  let path = ''
  switch(item.type) {
    case 'ppt':
      path = '/editor'
      break
    case 'lesson':
      path = '/lesson-editor'
      break
    case 'gif':
      path = '/gif-editor'
      break
  }
  router.push({
    path: path,
    query: {
      title: item.title,
      id: item.id.toString(),
      t: Date.now().toString()
    }
  })
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
    localStorage.removeItem('userAvatar')
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
  window.location.href = 'mailto:support@teachai.com'
}

const contactChat = () => {
  alert('在线客服功能开发中')
}

const handleHelp = () => {
  alert('个人中心：管理您的账号、查看创作历史（PPT/教案/GIF）和获取帮助')
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
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* 布局容器 - 垂直居中，左右留白 */
.profile-layout {
  display: flex;
  gap: 24px;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  height: 80vh;
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
  overflow: hidden;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-icon {
  font-size: 30px;
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

/* 页面标题 - 带图标样式 */
.section-title {
  font-size: 24px;
  color: #1e3c5c;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid rgba(11, 167, 175, 0.2);
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-icon {
  font-size: 28px;
  color: rgb(11, 167, 175);
}

/* 头像上传区域 - 在个人资料页面 */
.avatar-upload-section {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
  cursor: pointer;
}

.avatar-preview {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid rgb(11, 167, 175);
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.3);
}

.avatar-preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  color: white;
  font-size: 60px;
}

.avatar-upload-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  color: white;
}

.avatar-preview:hover .avatar-upload-overlay {
  opacity: 1;
}

.avatar-upload-overlay .iconfont {
  font-size: 30px;
  margin-bottom: 5px;
}

.avatar-upload-overlay span {
  font-size: 12px;
}

.hidden-input {
  display: none;
}

/* 个人资料表单 */
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

/* 统计卡片 - 改为4列 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
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
  flex-wrap: wrap;
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
  flex-wrap: wrap;
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

/* 帮助中心样式 */
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
  padding: 8px 16px;
  border-radius: 30px;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.1);
  font-size: 14px;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.2s ease;
}

.help-category:hover {
  border-color: rgb(11, 167, 175);
  background: rgba(11, 167, 175, 0.05);
}

.help-category.active {
  background: rgb(11, 167, 175);
  color: white;
  border-color: rgb(11, 167, 175);
}

.help-category.active .category-icon {
  color: white;
}

.category-icon {
  font-size: 16px;
  color: #71cdd1;
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
  transition: all 0.2s ease;
}

.support-btn:hover {
  background: rgb(11, 167, 175);
  color: white;
}

/* 关于我们 */
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
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

/* 账号设置 */
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
  border: 1px solid rgba(0, 0, 0, 0.05);
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
  transition: all 0.2s ease;
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

/* 弹窗样式 */
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
    height: 90vh;
  }
  
  .profile-sidebar {
    width: 100%;
    height: 280px;
    margin-bottom: 16px;
  }
  
  .profile-content {
    height: calc(100% - 296px);
  }
  
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>