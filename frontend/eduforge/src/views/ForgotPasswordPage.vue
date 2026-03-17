<template>
  <div class="forgot-container" @mousemove="handleMouseMove">
    <!-- 眼睛区域 -->
    <div class="eyes-wrapper">
      <div class="eye" ref="eyeLeftRef">
        <div class="pupil" :style="{ transform: pupilTransformLeft }"></div>
      </div>
      <div class="eye" ref="eyeRightRef">
        <div class="pupil" :style="{ transform: pupilTransformRight }"></div>
      </div>
    </div>

    <!-- 重置密码卡片 -->
    <div class="forgot-card-wrapper">
      <div class="gradient-bg"></div>
      
      <div class="forgot-card">
        <h1 class="forgot-title">重置密码</h1>
        
        <!-- 步骤1：邮箱验证 -->
        <div v-if="currentStep === 1" class="step-content">
          <div class="input-wrapper">
            <input 
              type="email" 
              v-model="email"
              placeholder="电子邮箱"
              class="forgot-input"
              @keyup.enter="sendVerificationCode"
            />
            <span class="input-icon">✉</span>
          </div>
          
          <!-- 图形验证码区域（无图标） -->
          <div class="captcha-group">
            <div class="captcha-row">
              <div class="input-wrapper captcha-input">
                <input 
                  type="text" 
                  v-model="imageCaptcha"
                  placeholder="图形验证码"
                  class="forgot-input"
                  @keyup.enter="sendVerificationCode"
                />
              </div>
              
              <!-- 图形验证码图片和刷新按钮 -->
              <div class="captcha-image-wrapper">
                <img 
                  :src="captchaImageUrl" 
                  alt="验证码"
                  class="captcha-image"
                  @click="refreshCaptcha"
                />
                <span class="captcha-refresh" @click="refreshCaptcha">↻</span>
              </div>
            </div>
            <p class="captcha-hint">点击图片可刷新验证码</p>
          </div>
          
          <!-- 获取邮箱验证码按钮 -->
          <button 
            class="captcha-btn" 
            @click="sendVerificationCode"
            :disabled="codeSent && codeCountdown > 0 || !canSendCode"
          >
            {{ codeSent ? `${codeCountdown}秒后重发` : '获取邮箱验证码' }}
          </button>

          <!-- 邮箱验证码输入 -->
          <div class="input-wrapper" v-if="codeSent">
            <input 
              type="text" 
              v-model="emailCode"
              placeholder="邮箱验证码"
              class="forgot-input"
              @keyup.enter="verifyCode"
            />
            <span class="input-icon">📧</span>
          </div>
        </div>

        <!-- 步骤2：设置新密码 -->
        <div v-if="currentStep === 2" class="step-content">
          <div class="input-wrapper">
            <input 
              :type="showNewPassword ? 'text' : 'password'"
              v-model="newPassword"
              placeholder="新密码"
              class="forgot-input"
              @keyup.enter="resetPassword"
            />
            <span 
              class="input-icon password-toggle iconfont" 
              :class="showNewPassword ? 'icon-xianshi' : 'icon-yanjing_yincang'"
              @click="showNewPassword = !showNewPassword"
            ></span>
          </div>
          
          <div class="input-wrapper">
            <input 
              :type="showConfirmPassword ? 'text' : 'password'"
              v-model="confirmPassword"
              placeholder="确认新密码"
              class="forgot-input"
              @keyup.enter="resetPassword"
            />
            <span 
              class="input-icon password-toggle iconfont" 
              :class="showConfirmPassword ? 'icon-xianshi' : 'icon-yanjing_yincang'"
              @click="showConfirmPassword = !showConfirmPassword"
            ></span>
          </div>

          <p class="password-hint">6-20位字符，建议包含字母和数字</p>
        </div>

        <!-- 底部链接：返回登录 -->
        <div class="forgot-links">
          <a href="#" class="login-link" @click.prevent="goToLogin">已有账号？返回登录</a>
        </div>
        
        <!-- 操作按钮 -->
        <button 
          v-if="currentStep === 1 && codeSent" 
          class="forgot-btn" 
          @click="verifyCode"
          :disabled="!canVerifyCode || isVerifying"
        >
          {{ isVerifying ? '验证中...' : '下一步' }}
        </button>
        
        <button 
          v-if="currentStep === 2" 
          class="forgot-btn" 
          @click="resetPassword"
          :disabled="!canResetPassword || isResetting"
        >
          {{ isResetting ? '提交中...' : '确认重置' }}
        </button>

        <!-- 提示信息 -->
        <div v-if="message" class="message-box" :class="messageType">
          {{ message }}
        </div>
      </div>
    </div>

    <!-- 帮助按钮 -->
    <div class="help-button" @click="showHelp">?</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ==================== 步骤控制 ====================
const currentStep = ref(1)

// ==================== 表单数据 ====================
const email = ref('')
const imageCaptcha = ref('') // 图形验证码
const emailCode = ref('') // 邮箱验证码
const newPassword = ref('')
const confirmPassword = ref('')

// ==================== UI状态 ====================
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)
const isVerifying = ref(false)
const isResetting = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error' | ''>('')

// ==================== 验证码发送状态 ====================
const codeSent = ref(false)
const codeCountdown = ref(0)
let countdownTimer: ReturnType<typeof setInterval> | null = null

// ==================== 图形验证码（模拟数据，对接后端后替换） ====================
const captchaImageUrl = ref('')
const captchaKey = ref('') // 后端返回的验证码唯一标识，提交时需要携带
const correctImageCaptcha = ref('1234') // 模拟正确的图形验证码

// ==================== 眼睛交互 ====================
const eyeLeftRef = ref<HTMLElement | null>(null)
const eyeRightRef = ref<HTMLElement | null>(null)
const pupilTransformLeft = ref('translate(-50%, -50%)')
const pupilTransformRight = ref('translate(-50%, -50%)')
const mousePosition = ref({ x: 0, y: 0 })
const isMouseMoving = ref(false)
let mouseMoveTimer: ReturnType<typeof setTimeout> | null = null

// ==================== 计算属性 ====================
const canSendCode = computed(() => {
  return email.value && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value) && 
         imageCaptcha.value && imageCaptcha.value.length >= 3
})

const canVerifyCode = computed(() => {
  return emailCode.value && emailCode.value.length >= 4
})

const canResetPassword = computed(() => {
  return newPassword.value.length >= 6 && 
         newPassword.value.length <= 20 && 
         newPassword.value === confirmPassword.value
})

// ==================== 后端接口：图形验证码 ====================
/**
 * 获取图形验证码
 * 后端接口：GET /api/captcha
 * 响应格式：
 * {
 *   image: string,  // base64格式的图片数据 或 SVG字符串
 *   key: string     // 验证码唯一标识，提交验证时需要
 * }
 */
const fetchCaptcha = async () => {
  try {
    // TODO: 替换为真实后端接口
    // const response = await fetch('/api/captcha')
    // const data = await response.json()
    // captchaImageUrl.value = data.image
    // captchaKey.value = data.key
    
    // 模拟数据（开发测试用）
    generateMockCaptcha()
    
  } catch (error) {
    console.error('获取验证码失败', error)
    messageType.value = 'error'
    message.value = '获取验证码失败，请重试'
  }
}

/**
 * 刷新图形验证码
 */
const refreshCaptcha = () => {
  fetchCaptcha()
  imageCaptcha.value = '' // 清空已输入的验证码
}

// ==================== 模拟数据生成（仅开发测试用，对接后端后删除） ====================
const generateMockCaptcha = () => {
  const chars = '0123456789'
  let result = ''
  for (let i = 0; i < 4; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  correctImageCaptcha.value = result
  captchaImageUrl.value = generateCaptchaSVG(result)
  captchaKey.value = `mock_${Date.now()}` // 模拟唯一标识
}

const generateCaptchaSVG = (text: string) => {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="100" height="42" viewBox="0 0 100 42">
      <rect width="100" height="42" fill="#f0f0f0"/>
      <line x1="10" y1="15" x2="90" y2="30" stroke="#ccc" stroke-width="1"/>
      <line x1="20" y1="35" x2="80" y2="10" stroke="#ccc" stroke-width="1"/>
      <text x="20" y="30" font-size="24" font-family="Arial" fill="#333" font-weight="bold">${text}</text>
    </svg>
  `
  return 'data:image/svg+xml,' + encodeURIComponent(svg)
}

// ==================== 后端接口：发送邮箱验证码 ====================
/**
 * 发送邮箱验证码
 * 后端接口：POST /api/send-email-code
 * 请求体：
 * {
 *   email: string,        // 邮箱地址
 *   captcha: string,      // 图形验证码
 *   captchaKey: string    // 图形验证码唯一标识
 * }
 * 响应格式：
 * {
 *   success: boolean,
 *   message: string,
 *   data?: {
 *     expireIn: number    // 验证码过期时间（秒）
 *   }
 * }
 */
 const sendVerificationCode = async () => {
  // 只检查邮箱格式是否正确
  if (!email.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    messageType.value = 'error';
    message.value = '请输入有效的邮箱地址';
    return;
  }
  
  message.value = '正在发送...';
  messageType.value = '';
  
  try {
    const response = await fetch('/api/send-email-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email.value
        // 删除了 captcha 和 captchaKey
      })
    })
    
    const result = await response.json()
    if (!response.ok) throw new Error(result.detail || '发送失败')

    // 发送成功，进入倒计时
    codeSent.value = true
    codeCountdown.value = 60
    
    if (countdownTimer) clearInterval(countdownTimer)
    countdownTimer = setInterval(() => {
      codeCountdown.value -= 1
      if (codeCountdown.value <= 0) {
        codeSent.value = false
        clearInterval(countdownTimer!)
      }
    }, 1000)

    messageType.value = 'success'
    message.value = '验证码已发送'
  } catch (error: any) {
    messageType.value = 'error'
    message.value = error.message || '发送失败，请稍后重试'
  }
}

// ==================== 后端接口：验证邮箱验证码 ====================
const verifyCode = async () => {
  if (!canVerifyCode.value) return
  
  isVerifying.value = true
  message.value = ''
  messageType.value = ''
  
  try {
    // 1. 发起真实请求
    const response = await fetch('/api/verify-email-code', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json' 
      },
      body: JSON.stringify({
        email: email.value, // 对应后端的 data.email
        code: emailCode.value // 对应后端的 data.code
      })
    })
    
    const resData = await response.json()
    
    // 2. 处理后端抛出的 HTTPException (status_code=400)
    if (!response.ok) {
      // 后端 detail 会被封装在 message 或 detail 中，取决于你的 FastAPI 配置
      throw new Error(resData.detail || '验证失败')
    }
    
    // 3. 验证成功：保存后端颁发的 reset_token
    // 关键点：后端返回的是 { data: { token: "xxx" } }
    const resetToken = resData.data.token
    localStorage.setItem('resetToken', resetToken)
    
    messageType.value = 'success'
    message.value = '验证成功，请重置密码'
    
    // 4. 跳转到下一步（重置密码表单）
    currentStep.value = 2
    
  } catch (error: any) {
    // 捕获网络错误或后端返回的 400 错误
    messageType.value = 'error'
    message.value = error.message || '服务器连接失败'
  } finally {
    isVerifying.value = false
  }
}

// ==================== 后端接口：重置密码 ====================
/**
 * 重置密码
 * 后端接口：POST /api/reset-password
 * 请求体：
 * {
 *   email: string,        // 邮箱地址
 *   password: string,     // 新密码
 *   confirmPassword: string, // 确认密码
 *   token: string         // 上一步获取的临时token
 * }
 * 响应格式：
 * {
 *   success: boolean,
 *   message: string
 * }
 */
 const resetPassword = async () => {
  if (!canResetPassword.value) return
  
  isResetting.value = true
  message.value = ''
  messageType.value = ''
  
  try {
    // 1. 获取 Step 2 存入的临时 Token
    const resetToken = localStorage.getItem('resetToken')
    
    if (!resetToken) {
      throw new Error('验证信息已失效，请重新获取验证码')
    }
    
    // 2. 发起重置密码请求
    const response = await fetch('/api/reset-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email.value,           // 必须与 Token 中的 sub 一致
        password: newPassword.value,
        confirmPassword: confirmPassword.value,
        token: resetToken             // 将 Token 放在 Body 中传给后端
      })
    })
    
    const resData = await response.json()
    
    // 3. 处理后端抛出的错误 (400, 401, 404)
    if (!response.ok) {
      // 如果后端返回 401，说明 Token 过期或非法
      if (response.status === 401) {
        localStorage.removeItem('resetToken') // 清理无效 Token
      }
      throw new Error(resData.detail || '重置失败')
    }
    
    // 4. 重置成功：清理现场
    localStorage.removeItem('resetToken')
    
    messageType.value = 'success'
    message.value = '密码重置成功，即将跳转到登录页'
    
    // 5. 延迟跳转
    setTimeout(() => {
      router.push('/login') 
    }, 2000)
    
  } catch (error: any) {
    messageType.value = 'error'
    message.value = error.message || '重置失败，请重试'
  } finally {
    isResetting.value = false
  }
}

// ==================== 页面跳转 ====================
const goToLogin = () => {
  router.push('/')
}

// ==================== 帮助 ====================
const showHelp = () => {
  alert('重置密码流程：\n1. 输入邮箱和图形验证码\n2. 点击获取邮箱验证码\n3. 输入邮箱验证码\n4. 设置新密码')
}

// ==================== 眼睛跟随逻辑 ====================
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

const handleMouseMove = (e: MouseEvent) => {
  mousePosition.value = { x: e.clientX, y: e.clientY }
  isMouseMoving.value = true
  
  if (mouseMoveTimer) clearTimeout(mouseMoveTimer)
  mouseMoveTimer = setTimeout(() => {
    isMouseMoving.value = false
    pupilTransformLeft.value = 'translate(-50%, -50%)'
    pupilTransformRight.value = 'translate(-50%, -50%)'
  }, 2000)
  
  updatePupils()
}

// ==================== 生命周期 ====================
onMounted(() => {
  // 初始化眼睛
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
      }, 1500)
    }
  }, 100)
  
  // 获取图形验证码
  fetchCaptcha()
})

onUnmounted(() => {
  if (mouseMoveTimer) clearTimeout(mouseMoveTimer)
  if (countdownTimer) clearInterval(countdownTimer)
  
  // 清理可能保存的token
  localStorage.removeItem('resetToken')
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.forgot-container {
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

/* 眼睛样式 */
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

/* 卡片包装 */
.forgot-card-wrapper {
  position: relative;
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
  pointer-events: none;
}

/* 卡片样式 */
.forgot-card {
  position: relative;
  width: 420px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 15px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  z-index: 2;
  padding: 30px 30px 40px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

/* 标题 */
.forgot-title {
  text-align: center;
  margin-bottom: 30px;
  margin-top: 10px;
  font-size: 42px;
  color: #1e3c5c;
  font-weight: 700;
  letter-spacing: 1px;
}

/* 步骤内容 */
.step-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

/* 输入框包装 */
.input-wrapper {
  position: relative;
  width: 100%;
}

.forgot-input {
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

.forgot-input:focus {
  border-color: rgb(11, 167, 175);
  box-shadow: 0 0 0 3px rgba(11, 167, 175, 0.2);
  background: white;
}

.forgot-input::placeholder {
  color: #999;
}

.input-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 16px;
  transition: all 0.2s ease;
  z-index: 3;
}

.password-toggle {
  cursor: pointer;
  font-size: 18px;
}

.password-toggle:hover {
  color: rgb(11, 167, 175);
  transform: translateY(-50%) scale(1.1);
}

/* 图形验证码区域 */
.captcha-group {
  margin-bottom: 5px;
}

.captcha-row {
  display: flex;
  gap: 10px;
  align-items: center;
}

.captcha-input {
  flex: 1;
}

.captcha-image-wrapper {
  position: relative;
  width: 100px;
  height: 42px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid rgba(255, 255, 255, 0.8);
  background: white;
  flex-shrink: 0;
}

.captcha-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.captcha-refresh {
  position: absolute;
  top: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  cursor: pointer;
  border-radius: 0 0 0 8px;
  transition: all 0.2s;
  z-index: 6;
}

.captcha-refresh:hover {
  background: rgba(0, 0, 0, 0.7);
  transform: rotate(180deg);
}

.captcha-hint {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  padding-left: 5px;
}

/* 获取验证码按钮 */
.captcha-btn {
  width: 100%;
  height: 42px;
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid rgb(11, 167, 175);
  border-radius: 25px;
  color: rgb(11, 167, 175);
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 5px;
}

.captcha-btn:hover:not(:disabled) {
  background: rgb(11, 167, 175);
  color: white;
  transform: scale(1.02);
}

.captcha-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  border-color: #999;
  color: #666;
}

/* 密码提示 */
.password-hint {
  font-size: 12px;
  color: #666;
  margin-top: -5px;
  padding-left: 15px;
}

/* 底部链接 */
.forgot-links {
  display: flex;
  justify-content: center;
  width: 100%;
  margin: 20px auto 20px;
}

.login-link {
  color: #004288bf;
  font-size: 14px;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
}

.login-link:hover {
  color: rgb(11, 167, 175);
  text-decoration: underline;
}

/* 按钮 */
.forgot-btn {
  height: 44px;
  width: 140px;
  margin: 0 auto;
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

.forgot-btn:hover:not(:disabled) {
  background: rgb(8, 130, 136);
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(11, 167, 175, 0.4);
}

.forgot-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 消息框 */
.message-box {
  margin-top: 20px;
  padding: 10px;
  border-radius: 25px;
  text-align: center;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
}

.message-box.success {
  color: #2e7d32;
  background: rgba(200, 255, 200, 0.3);
  border: 1px solid rgba(46, 125, 50, 0.3);
}

.message-box.error {
  color: #d32f2f;
  background: rgba(255, 200, 200, 0.3);
  border: 1px solid rgba(211, 47, 47, 0.3);
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

/* 响应式 */
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
  .forgot-card {
    width: 340px;
    padding: 20px;
  }
  .forgot-title {
    font-size: 36px;
    margin-bottom: 20px;
  }
  .captcha-row {
    flex-direction: column;
    gap: 10px;
  }
  .captcha-image-wrapper {
    width: 100%;
  }
}

/* iconfont 样式 */
.iconfont {
  font-family: "iconfont" !important;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>