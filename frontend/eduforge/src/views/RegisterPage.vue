<template>
  <div class="register-page">
    <div class="register-card-main">
      <!-- 左侧：四个小人物区域 -->
      <div class="characters-side">
        <!-- 去掉 logo-wrapper，或改为透明 -->
        <div class="characters-wrapper">
          <div class="characters-container">
            <!-- 紫色角色 -->
            <div 
              ref="purpleCharacter"
              class="character purple-character"
              :style="{
                height: (isTyping || (password.length > 0 && !showPassword)) ? '480px' : '440px',
                transform: `skewX(${getPurpleSkew()}deg) ${(isTyping || (password.length > 0 && !showPassword)) ? 'translateX(40px)' : ''}`,
                transformOrigin: 'bottom center'
              }"
            >
              <div 
                class="eyes-wrapper"
                :style="{
                  left: (password.length > 0 && showPassword) ? '20px' : isLookingAtEachOther ? '55px' : `${45 + purplePos.faceX}px`,
                  top: (password.length > 0 && showPassword) ? '35px' : isLookingAtEachOther ? '65px' : `${40 + purplePos.faceY}px`
                }"
              >
                <EyeBall :size="20" :pupil-size="8" :max-distance="5" :is-blinking="isPurpleBlinking"
                  :force-look-x="getPurpleEyeX()" :force-look-y="getPurpleEyeY()" />
                <EyeBall :size="20" :pupil-size="8" :max-distance="5" :is-blinking="isPurpleBlinking"
                  :force-look-x="getPurpleEyeX()" :force-look-y="getPurpleEyeY()" />
              </div>
            </div>

            <!-- 粉色角色 -->
            <div 
              ref="blackCharacter"
              class="character black-character"
              :style="{
                transform: `skewX(${getBlackSkew()}deg) ${isLookingAtEachOther ? 'translateX(20px)' : ''}`,
                transformOrigin: 'bottom center'
              }"
            >
              <div 
                class="eyes-wrapper"
                :style="{
                  left: (password.length > 0 && showPassword) ? '10px' : isLookingAtEachOther ? '32px' : `${26 + blackPos.faceX}px`,
                  top: (password.length > 0 && showPassword) ? '28px' : isLookingAtEachOther ? '12px' : `${32 + blackPos.faceY}px`
                }"
              >
                <EyeBall :size="18" :pupil-size="7" :max-distance="4" :is-blinking="isBlackBlinking"
                  :force-look-x="password.length > 0 && showPassword ? -4 : (isLookingAtEachOther ? 0 : undefined)"
                  :force-look-y="password.length > 0 && showPassword ? -4 : (isLookingAtEachOther ? -4 : undefined)" />
                <EyeBall :size="18" :pupil-size="7" :max-distance="4" :is-blinking="isBlackBlinking"
                  :force-look-x="password.length > 0 && showPassword ? -4 : (isLookingAtEachOther ? 0 : undefined)"
                  :force-look-y="password.length > 0 && showPassword ? -4 : (isLookingAtEachOther ? -4 : undefined)" />
              </div>
            </div>

            <!-- 深蓝色角色 -->
            <div 
              ref="orangeCharacter"
              class="character orange-character"
              :style="{
                transform: `skewX(${password.length > 0 && showPassword ? 0 : orangePos.bodySkew}deg)`,
                transformOrigin: 'bottom center'
              }"
            >
              <div 
                class="pupils-wrapper"
                :style="{
                  left: (password.length > 0 && showPassword) ? '50px' : `${82 + orangePos.faceX}px`,
                  top: (password.length > 0 && showPassword) ? '85px' : `${90 + orangePos.faceY}px`
                }"
              >
                <Pupil :size="14" :max-distance="5" :force-look-x="password.length > 0 && showPassword ? -5 : undefined"
                  :force-look-y="password.length > 0 && showPassword ? -4 : undefined" />
                <Pupil :size="14" :max-distance="5" :force-look-x="password.length > 0 && showPassword ? -5 : undefined"
                  :force-look-y="password.length > 0 && showPassword ? -4 : undefined" />
              </div>
            </div>

            <!-- 黄色角色 -->
            <div 
              ref="yellowCharacter"
              class="character yellow-character"
              :style="{
                transform: `skewX(${password.length > 0 && showPassword ? 0 : yellowPos.bodySkew}deg)`,
                transformOrigin: 'bottom center'
              }"
            >
              <div 
                class="pupils-wrapper"
                :style="{
                  left: (password.length > 0 && showPassword) ? '20px' : `${52 + yellowPos.faceX}px`,
                  top: (password.length > 0 && showPassword) ? '35px' : `${40 + yellowPos.faceY}px`
                }"
              >
                <Pupil :size="14" :max-distance="5" :force-look-x="password.length > 0 && showPassword ? -5 : undefined"
                  :force-look-y="password.length > 0 && showPassword ? -4 : undefined" />
                <Pupil :size="14" :max-distance="5" :force-look-x="password.length > 0 && showPassword ? -5 : undefined"
                  :force-look-y="password.length > 0 && showPassword ? -4 : undefined" />
              </div>
              <div 
                class="mouth"
                :style="{
                  left: (password.length > 0 && showPassword) ? '10px' : `${40 + yellowPos.faceX}px`,
                  top: (password.length > 0 && showPassword) ? '88px' : `${88 + yellowPos.faceY}px`
                }"
              ></div>
            </div>
          </div>
        </div>
        
        <div class="decorative-bg"></div>
        <div class="blur-circle top-blur"></div>
        <div class="blur-circle bottom-blur"></div>
      </div>

      <!-- 右侧：注册表单区域 -->
      <div class="form-side">
        <div class="form-content">
          <h1 class="form-title">注册账号</h1>
          <p class="form-subtitle">请填写注册信息</p>

          <form @submit.prevent="handleRegister" class="register-form">
            <div class="input-wrapper">
              <input type="text" placeholder="用户名（3-20位）" v-model="username"
                @focus="isTyping = true" @blur="isTyping = false" required class="form-input" />
            </div>

            <div class="input-wrapper">
              <input type="email" placeholder="邮箱" v-model="email" required class="form-input" :disabled="isSendingCode" />
            </div>

            <div class="input-wrapper code-wrapper">
              <input type="text" placeholder="验证码" v-model="verificationCode" required class="form-input code-input" />
              <button type="button" @click="sendVerificationCode" class="send-code-btn"
                :disabled="isSendingCode || countdown > 0">
                {{ countdown > 0 ? `${countdown}s` : (isSendingCode ? '发送中' : '获取验证码') }}
              </button>
            </div>

            <div class="input-wrapper">
              <input :type="showPassword ? 'text' : 'password'" placeholder="密码（至少6位）" v-model="password" required class="form-input" />
              <span v-if="password.length > 0" class="input-icon password-toggle" @click="showPassword = !showPassword">👁️</span>
            </div>

            <div class="input-wrapper">
              <input :type="showConfirmPassword ? 'text' : 'password'" placeholder="确认密码" v-model="confirmPassword" required class="form-input" />
              <span v-if="confirmPassword.length > 0" class="input-icon password-toggle" @click="showConfirmPassword = !showConfirmPassword">👁️</span>
            </div>

            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
            <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

            <div class="form-links">
              <router-link to="/" class="login-link">已有账号？立即登录</router-link>
            </div>

            <button type="submit" class="submit-btn" :disabled="isRegistering">
              {{ isRegistering ? '注册中...' : '注册' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Pupil from './Pupil.vue'
import EyeBall from './EyeBall.vue'
import { ref, reactive, onMounted, onUnmounted, watch, provide } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 基础注册状态
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const username = ref('')
const email = ref('')
const verificationCode = ref('')
const password = ref('')
const confirmPassword = ref('')
const isRegistering = ref(false)
const isSendingCode = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const countdown = ref(0)
let countdownTimer = null

// 动画状态
const mouseX = ref(0)
const mouseY = ref(0)
const isPurpleBlinking = ref(false)
const isBlackBlinking = ref(false)
const isTyping = ref(false)
const isLookingAtEachOther = ref(false)
const isPurplePeeking = ref(false)

provide('mouseX', mouseX)
provide('mouseY', mouseY)

const purpleCharacter = ref(null)
const blackCharacter = ref(null)
const orangeCharacter = ref(null)
const yellowCharacter = ref(null)

const purplePos = reactive({ faceX: 0, faceY: 0, bodySkew: 0 })
const blackPos = reactive({ faceX: 0, faceY: 0, bodySkew: 0 })
const orangePos = reactive({ faceX: 0, faceY: 0, bodySkew: 0 })
const yellowPos = reactive({ faceX: 0, faceY: 0, bodySkew: 0 })

const blinkTimers = reactive({
  purple: null,
  black: null,
  lookTimer: null,
  peekTimer: null
})

const sendVerificationCode = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  
  if (!email.value) {
    errorMessage.value = '请输入邮箱地址'
    return
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errorMessage.value = '请输入有效的邮箱地址'
    return
  }

  /* try {
    const registeredUsers = JSON.parse(localStorage.getItem('registeredUsers') || '[]')
    if (registeredUsers.some(u => u.email === email.value)) {
      errorMessage.value = '邮箱已被注册'
      return
    }
  } catch (err) {}
*/ 
  isSendingCode.value = true
  
  try {
    const response = await fetch('/api/send-verification-code', {    
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value })
    })
    
    const data = await response.json()
    
    if (response.ok && data.success) {
      successMessage.value = '验证码已发送'
      countdown.value = 60
      countdownTimer = setInterval(() => {
        countdown.value--
        if (countdown.value <= 0) clearInterval(countdownTimer)
      }, 1000)
    } else {
      errorMessage.value = data.message || '发送验证码失败'
    }
  } catch (err) {
    errorMessage.value = '网络错误'
  } finally {
    isSendingCode.value = false
  }
}

const handleRegister = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  
  if (!username.value) {
    errorMessage.value = '请输入用户名'
    return
  }
  if (username.value.length < 3 || username.value.length > 20) {
    errorMessage.value = '用户名长度需在3-20位'
    return
  }
  if (!email.value) {
    errorMessage.value = '请输入邮箱'
    return
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errorMessage.value = '请输入有效的邮箱地址'
    return
  }
  if (!verificationCode.value) {
    errorMessage.value = '请输入验证码'
    return
  }
  if (password.value.length < 6) {
    errorMessage.value = '密码长度不能少于6位'
    return
  }
  if (password.value !== confirmPassword.value) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }

  isRegistering.value = true
  try {
    const verifyResponse = await fetch('/api/verify-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, code: verificationCode.value })
    })
    
    const verifyData = await verifyResponse.json()
    
    if (!verifyResponse.ok || !verifyData.success) {
      errorMessage.value = verifyData.message || '验证码错误'
      return
    }
    
    const registeredUsers = JSON.parse(localStorage.getItem('registeredUsers') || '[]')
    
    if (registeredUsers.some(u => u.username === username.value)) {
      errorMessage.value = '用户名已存在'
      return
    }
    
    registeredUsers.push({
      username: username.value,
      email: email.value,
      password: password.value,
      registerTime: new Date().toISOString()
    })
    localStorage.setItem('registeredUsers', JSON.stringify(registeredUsers))
    
    await fetch('/api/clear-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value })
    }).catch(console.error)
    
    successMessage.value = '注册成功！正在跳转...'
    setTimeout(() => router.push('/'), 1500)
  } catch (err) {
    errorMessage.value = '注册失败，请重试'
  } finally {
    isRegistering.value = false
  }
}

// 角色动画函数
const calculatePosition = (el) => {
  if (!el) return { faceX: 0, faceY: 0, bodySkew: 0 }
  const rect = el.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 3
  const deltaX = mouseX.value - centerX
  const deltaY = mouseY.value - centerY
  const faceX = Math.max(-15, Math.min(15, deltaX / 20))
  const faceY = Math.max(-10, Math.min(10, deltaY / 30))
  const bodySkew = Math.max(-6, Math.min(6, -deltaX / 120))
  return { faceX, faceY, bodySkew }
}

const updateCharacterPositions = () => {
  const purpleData = calculatePosition(purpleCharacter.value)
  purplePos.faceX = purpleData.faceX
  purplePos.faceY = purpleData.faceY
  purplePos.bodySkew = purpleData.bodySkew
  const blackData = calculatePosition(blackCharacter.value)
  blackPos.faceX = blackData.faceX
  blackPos.faceY = blackData.faceY
  blackPos.bodySkew = blackData.bodySkew
  const orangeData = calculatePosition(orangeCharacter.value)
  orangePos.faceX = orangeData.faceX
  orangePos.faceY = orangeData.faceY
  orangePos.bodySkew = orangeData.bodySkew
  const yellowData = calculatePosition(yellowCharacter.value)
  yellowPos.faceX = yellowData.faceX
  yellowPos.faceY = yellowData.faceY
  yellowPos.bodySkew = yellowData.bodySkew
}

const getPurpleSkew = () => {
  if (password.value.length > 0 && showPassword.value) return 0
  return (purplePos.bodySkew || 0) - (isTyping.value || (password.value.length > 0 && !showPassword.value) ? 12 : 0)
}

const getBlackSkew = () => {
  if (password.value.length > 0 && showPassword.value) return 0
  return isLookingAtEachOther.value 
    ? (blackPos.bodySkew || 0) * 1.5 + 10 
    : (isTyping.value || (password.value.length > 0 && !showPassword.value) 
        ? (blackPos.bodySkew || 0) * 1.5 
        : blackPos.bodySkew || 0)
}

const getPurpleEyeX = () => {
  if (password.value.length > 0 && showPassword.value) return isPurplePeeking.value ? 4 : -4
  return isLookingAtEachOther.value ? 3 : undefined
}

const getPurpleEyeY = () => {
  if (password.value.length > 0 && showPassword.value) return isPurplePeeking.value ? 5 : -4
  return isLookingAtEachOther.value ? 4 : undefined
}

const handleMouseMove = (e) => {
  mouseX.value = e.clientX
  mouseY.value = e.clientY
  updateCharacterPositions()
}

const scheduleBlink = (blinkingState) => {
  const interval = Math.random() * 4000 + 3000
  return setTimeout(() => {
    blinkingState.value = true
    setTimeout(() => {
      blinkingState.value = false
      scheduleBlink(blinkingState)
    }, 150)
  }, interval)
}

const schedulePeek = () => {
  const interval = Math.random() * 3000 + 2000
  blinkTimers.peekTimer = setTimeout(() => {
    isPurplePeeking.value = true
    setTimeout(() => {
      isPurplePeeking.value = false
      if (password.value.length > 0 && showPassword.value) schedulePeek()
    }, 800)
  }, interval)
}

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
  blinkTimers.purple = scheduleBlink(isPurpleBlinking)
  blinkTimers.black = scheduleBlink(isBlackBlinking)
  updateCharacterPositions()

  watch(isTyping, (val) => {
    if (val) {
      isLookingAtEachOther.value = true
      blinkTimers.lookTimer = setTimeout(() => isLookingAtEachOther.value = false, 800)
    } else {
      isLookingAtEachOther.value = false
      clearTimeout(blinkTimers.lookTimer)
    }
  })

  watch([password, showPassword], ([pwd, show]) => {
    if (pwd.length > 0 && show) schedulePeek()
    else {
      clearTimeout(blinkTimers.peekTimer)
      isPurplePeeking.value = false
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
  clearTimeout(blinkTimers.purple)
  clearTimeout(blinkTimers.black)
  clearTimeout(blinkTimers.lookTimer)
  clearTimeout(blinkTimers.peekTimer)
  if (countdownTimer) clearInterval(countdownTimer)
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.register-page {
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(
    135deg,
    rgba(212, 245, 245, 0.3) 0%,
    rgba(130, 212, 215, 0.6) 25%,
    rgba(174, 230, 231, 0.6) 50%,
    rgba(189, 236, 236, 0.4) 75%,
    rgba(212, 245, 245, 0.3) 100%
  );
  overflow: hidden;
}

.register-card-main {
  width: 1100px;
  height: 700px;
  display: flex;
  border-radius: 32px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(20px);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.characters-side {
  flex: 1;
  position: relative;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.characters-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.characters-container {
  position: relative;
  width: 550px;
  height: 500px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.character {
  position: absolute;
  bottom: 0;
  transition: all 0.7s ease-in-out;
  border-radius: 10px 10px 0 0;
}

.purple-character {
  left: 70px;
  width: 200px;
  height: 440px;
  background-color: #91a7ff;
  z-index: 1;
}

.black-character {
  left: 270px;
  width: 140px;
  height: 350px;
  background-color: #f7d2ea;
  border-radius: 8px 8px 0 0;
  z-index: 2;
}

.orange-character {
  left: -20px;
  width: 280px;
  height: 240px;
  background-color: #9bcbed;
  border-radius: 140px 140px 0 0;
  z-index: 3;
}

.yellow-character {
  left: 370px;
  width: 160px;
  height: 270px;
  background-color: #f5e3bd;
  border-radius: 80px 80px 0 0;
  z-index: 4;
}

.eyes-wrapper {
  position: absolute;
  display: flex;
  gap: 2rem;
  transition: all 0.7s ease-in-out;
}

.pupils-wrapper {
  position: absolute;
  display: flex;
  gap: 2rem;
  transition: all 0.2s ease-out;
}

.mouth {
  position: absolute;
  width: 5rem;
  height: 4px;
  background-color: #2D2D2D;
  border-radius: 9999px;
  transition: all 0.2s ease-out;
}

.decorative-bg {
  position: absolute;
  inset: 0;
  background-image: linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
  background-size: 20px 20px;
  z-index: 1;
  pointer-events: none;
}

.blur-circle {
  position: absolute;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  filter: blur(60px);
  z-index: 1;
  pointer-events: none;
}

.top-blur {
  top: 10%;
  right: 10%;
  width: 200px;
  height: 200px;
}

.bottom-blur {
  bottom: 10%;
  left: 10%;
  width: 280px;
  height: 280px;
  background-color: rgba(255, 255, 255, 0.15);
}

.form-side {
  width: 420px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255, 255, 255, 0.5);
}

.form-content {
  width: 100%;
  padding: 0 40px;
}

.form-title {
  font-size: 32px;
  font-weight: 700;
  color: #1e3c5c;
  text-align: center;
  margin-bottom: 8px;
}

.form-subtitle {
  font-size: 14px;
  color: #6b7280;
  text-align: center;
  margin-bottom: 32px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-wrapper {
  position: relative;
  width: 100%;
}

.form-input {
  width: 100%;
  height: 48px;
  padding: 0 45px 0 18px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  font-size: 14px;
  outline: none;
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.2s ease;
  color: #34495e;
}

.form-input:focus {
  border-color: rgb(11, 167, 175);
  box-shadow: 0 0 0 3px rgba(11, 167, 175, 0.1);
  background: white;
}

.form-input::placeholder {
  color: #aaa;
}

.input-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 18px;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.input-icon:hover {
  opacity: 1;
}

.code-wrapper {
  display: flex;
  gap: 12px;
}

.code-input {
  flex: 1;
  padding-right: 12px;
}

.send-code-btn {
  height: 48px;
  padding: 0 16px;
  border: none;
  border-radius: 12px;
  background: rgb(11, 167, 175);
  color: white;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.send-code-btn:hover:not(:disabled) {
  background: rgb(8, 130, 136);
  transform: scale(1.02);
}

.send-code-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: #9ca3af;
}

.error-message {
  padding: 10px;
  font-size: 12px;
  color: #f87171;
  background-color: rgba(185, 28, 28, 0.1);
  border-radius: 10px;
  text-align: center;
}

.success-message {
  padding: 10px;
  font-size: 12px;
  color: #10b981;
  background-color: rgba(16, 185, 129, 0.1);
  border-radius: 10px;
  text-align: center;
}

.form-links {
  text-align: center;
  margin-top: 8px;
}

.login-link {
  color: rgb(11, 167, 175);
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  transition: color 0.2s;
}

.login-link:hover {
  color: rgb(8, 130, 136);
  text-decoration: underline;
}

.submit-btn {
  height: 48px;
  width: 100%;
  border: none;
  border-radius: 12px;
  background: rgb(11, 167, 175);
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 8px;
}

.submit-btn:hover:not(:disabled) {
  background: rgb(8, 130, 136);
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.3);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 1024px) {
  .register-card-main {
    width: 90%;
    height: auto;
    flex-direction: column;
  }
  .characters-side {
    height: 400px;
  }
  .form-side {
    width: 100%;
    border-left: none;
    border-top: 1px solid rgba(255, 255, 255, 0.5);
    padding: 30px 0;
  }
}

@media (max-width: 768px) {
  .form-content {
    padding: 0 25px;
  }
  .characters-side {
    display: none;
  }
}
</style>