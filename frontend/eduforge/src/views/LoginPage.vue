<template>
  <div class="login-container" @mousemove="handleMouseMove">
    <!-- 眼睛区域 -->
    <div class="eyes-wrapper">
      <div class="eye" ref="eyeLeftRef">
        <div class="pupil" :style="{ transform: pupilTransformLeft }"></div>
      </div>
      <div class="eye" ref="eyeRightRef">
        <div class="pupil" :style="{ transform: pupilTransformRight }"></div>
      </div>
    </div>

    <!-- 登录卡片 -->
    <div class="login-card-wrapper">
      <div class="gradient-bg"></div>
      
      <div class="login-card">
        <h1 class="login-title">登录</h1>
        
        <div class="input-wrapper">
          <input 
            type="text" 
            v-model="username"
            placeholder="账号"
            class="login-input"
            @keyup.enter="handleLogin"
          />
          <!-- 账号图标：已移除 -->
        </div>
        
        <div class="input-wrapper">
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="password"
            placeholder="密码"
            class="login-input"
            @keyup.enter="handleLogin"
          />
          <!-- 只有输入密码时才显示切换图标 -->
          <span 
            v-if="password.length > 0"
            class="input-icon password-toggle iconfont" 
            :class="showPassword ? 'icon-icon-xianshi' : 'icon-icon-yanjing_yincang'"
            @click="showPassword = !showPassword"
          ></span>
        </div>
        
        <div class="login-links">
          <router-link to="/forgot-password" class="forgot-link">忘记密码？</router-link>
          <router-link to="/register" class="register-link">注册账号</router-link>
        </div>
        
        <button class="login-btn" @click.prevent="handleLogin" :disabled="isLoggingIn">
          {{ isLoggingIn ? '登录中...' : '登录' }}
        </button>
      </div>
    </div>

    <!-- 帮助按钮 -->
    <div class="help-button" @click="handleHelp">?</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const isLoggingIn = ref(false)

// 眼睛元素引用
const eyeLeftRef = ref<HTMLElement | null>(null)
const eyeRightRef = ref<HTMLElement | null>(null)

// 瞳孔变换
const pupilTransformLeft = ref('translate(-50%, -50%)')
const pupilTransformRight = ref('translate(-50%, -50%)')

// 鼠标位置跟踪
const mousePosition = ref({ x: 0, y: 0 })
const isMouseMoving = ref(false)
// 修复 timer 类型
let mouseMoveTimer: ReturnType<typeof setTimeout> | null = null

// 限制瞳孔移动范围的函数
const calculatePupilPosition = (eyeElement: HTMLElement, mouseX: number, mouseY: number): string => {
  const rect = eyeElement.getBoundingClientRect()
  
  const eyeCenterX = rect.left + rect.width / 2
  const eyeCenterY = rect.top + rect.height / 2
  
  const deltaX = mouseX - eyeCenterX
  const deltaY = mouseY - eyeCenterY
  
  const angle = Math.atan2(deltaY, deltaX)
  
  const eyeRadius = rect.width / 2
  const pupilRadius = 20
  const maxMove = eyeRadius - pupilRadius - 5
  
  const distance = Math.min(Math.sqrt(deltaX ** 2 + deltaY ** 2), maxMove)
  
  const moveX = Math.cos(angle) * distance
  const moveY = Math.sin(angle) * distance
  
  return `translate(calc(-50% + ${moveX}px), calc(-50% + ${moveY}px))`
}

// 更新瞳孔位置
const updatePupils = () => {
  if (!isMouseMoving.value) return
  
  requestAnimationFrame(() => {
    if (eyeLeftRef.value) {
      pupilTransformLeft.value = calculatePupilPosition(eyeLeftRef.value, mousePosition.value.x, mousePosition.value.y)
    }
    if (eyeRightRef.value) {
      pupilTransformRight.value = calculatePupilPosition(eyeRightRef.value, mousePosition.value.x, mousePosition.value.y)
    }
  })
}

// 处理鼠标移动
const handleMouseMove = (e: MouseEvent) => {
  mousePosition.value = { x: e.clientX, y: e.clientY }
  isMouseMoving.value = true
  
  if (mouseMoveTimer) {
    clearTimeout(mouseMoveTimer)
  }
  
  mouseMoveTimer = setTimeout(() => {
    isMouseMoving.value = false
    pupilTransformLeft.value = 'translate(-50%, -50%)'
    pupilTransformRight.value = 'translate(-50%, -50%)'
  }, 2000)
  
  updatePupils()
}

onMounted(() => {
  setTimeout(() => {
    if (eyeLeftRef.value && eyeRightRef.value) {
      const centerX = window.innerWidth / 2
      const centerY = window.innerHeight / 2
      mousePosition.value = { x: centerX, y: centerY }
      isMouseMoving.value = true
      updatePupils()
      
      setTimeout(() => {
        isMouseMoving.value = false
        pupilTransformLeft.value = 'translate(-50%, -50%)'
        pupilTransformRight.value = 'translate(-50%, -50%)'
      }, 2000)
    }
  }, 100)
})

onUnmounted(() => {
  if (mouseMoveTimer) {
    clearTimeout(mouseMoveTimer)
  }
})

// 登录逻辑
const validUsers = [
  { username: 'admin', password: 'admin123' },
  { username: 'user', password: 'user123' },
  { username: 'test', password: 'test123' }
]

const handleLogin = async (): Promise<void> => {
  if (!username.value || !password.value) {
    alert('请输入账号和密码')
    return
  }

  isLoggingIn.value = true

  try {
    const formData = new URLSearchParams()
    formData.append('username', username.value)
    formData.append('password', password.value)

    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'  // 🌟 必须这个类型
      },
      body: formData
    })

    if (!response.ok) {
      const error = await response.json()
      alert(error.detail || '登录失败')
      return
    }

    const data = await response.json()
    // 保存 token 到 localStorage
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('token_type', data.token_type)
    localStorage.setItem('username', username.value)

    router.push('/home')
  } catch (error) {
    alert('登录失败，请重试')
  } finally {
    isLoggingIn.value = false
  }
}

const handleHelp = (): void => {
  alert('请输入您的账号和密码进行登录\n测试账号：admin/admin123')
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* 确保iconfont样式正确 */
.iconfont {
  font-family: "iconfont" !important;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.login-container {
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(
    135deg,
    rgba(212, 245, 245, 0.3) 0%,
    rgba(130, 212, 215, 0.6) 25%,
    rgba(174, 230, 231, 0.6) 50%,
    rgba(189, 236, 236, 0.4) 75%,
    rgba(212, 245, 245, 0.3) 100%
  );
}

.eyes-wrapper {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
  z-index: 10;
}

.eye {
  width: 120px;
  height: 120px;
  background: white;
  border-radius: 50%;
  position: relative;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.5);
}

.eye::after {
  content: '';
  position: absolute;
  top: 20%;
  left: 20%;
  width: 25%;
  height: 25%;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  z-index: 2;
  pointer-events: none;
  opacity: 0.8;
  filter: blur(1px);
}

.pupil {
  width: 40px;
  height: 40px;
  background: #1e3c5c;
  border-radius: 50%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  transition: transform 0.1s ease-out;
  box-shadow: inset 0 0 0 2px #2a4a6a, 0 2px 4px rgba(0,0,0,0.2);
  z-index: 3;
}

.pupil::after {
  content: '';
  position: absolute;
  top: 15%;
  left: 15%;
  width: 25%;
  height: 25%;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  z-index: 4;
}

.login-card-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  z-index: 5;
}

.gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 30% 50%, rgba(255,255,255,0.2) 0%, transparent 50%);
  z-index: 1;
}

/* 统一卡片宽度为 420px，与忘记密码页面一致 */
.login-card {
  position: relative;
  width: 420px;
  height: 450px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 15px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  z-index: 2;
  padding: 20px 30px;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.login-title {
  text-align: center;
  margin-bottom: 50px;
  margin-top: 40px;
  font-size: 42px;
  color: #1e3c5c;
  font-weight: 700;
  letter-spacing: 1px;
}

/* 输入框宽度设为100%，自适应卡片宽度 */
.input-wrapper {
  position: relative;
  width: 100%;
  margin: 0 auto 25px;
}

.login-input {
  width: 100%;
  height: 42px;
  padding: 0 40px 0 20px;
  border-radius: 25px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.8);
  font-size: 15px;
  outline: none;
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.2s ease;
  color: #34495e;
}

.login-input:focus {
  border-color: rgb(11, 167, 175);
  box-shadow: 0 0 0 3px rgba(11, 167, 175, 0.2);
  background: white;
}

.login-input::placeholder {
  color: #999;
}

.input-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 18px;
  transition: all 0.2s ease;
  z-index: 3;
}

.password-toggle {
  cursor: pointer;
  font-size: 20px;
}

.password-toggle:hover {
  color: rgb(11, 167, 175);
  transform: translateY(-50%) scale(1.1);
}

.login-links {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin: 0 auto 20px;
}

.forgot-link, .register-link {
  color: #004288bf;
  font-size: 14px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.forgot-link:hover, .register-link:hover {
  color: rgb(11, 167, 175);
  text-decoration: underline;
}

.login-btn {
  height: 44px;
  width: 140px;
  margin-top: 20px;
  margin-left: auto;
  margin-right: auto;
  display: block;
  font-size: 18px;
  font-weight: 500;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  outline: none;
  background: rgb(11, 167, 175);
  color: white;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.3);
}

.login-btn:hover:not(:disabled) {
  background: rgb(8, 130, 136);
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(11, 167, 175, 0.4);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  transition: all 0.2s ease;
  z-index: 1000;
}

.help-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

@media (max-width: 768px) {
  .eye {
    width: 80px;
    height: 80px;
  }
  .pupil {
    width: 28px;
    height: 28px;
  }
  .eyes-wrapper {
    gap: 20px;
    margin-bottom: 20px;
  }
  .login-card {
    width: 340px;
    height: 420px;
    padding: 20px;
  }
}
</style>