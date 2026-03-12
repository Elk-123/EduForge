<template>
  <div class="register-container" @mousemove="handleMouseMove">
    <!-- 眼睛区域：放在注册卡片上方 -->
    <div class="eyes-wrapper">
      <div class="eye" ref="eyeLeftRef">
        <div class="pupil" :style="{ transform: pupilTransformLeft }"></div>
      </div>
      <div class="eye" ref="eyeRightRef">
        <div class="pupil" :style="{ transform: pupilTransformRight }"></div>
      </div>
    </div>

    <!-- 注册卡片 -->
    <div class="register-card-wrapper">
      <div class="gradient-bg"></div>
      
      <div class="register-card">
        <h1 class="register-title">注册账号</h1>
        
        <div class="input-wrapper">
          <input 
            type="text" 
            v-model="username"
            placeholder="用户名"
            class="register-input"
            @keyup.enter="handleRegister"
          />
          <span class="input-icon iconfont icon-yonghu"></span>
        </div>
        
        <div class="input-wrapper">
          <input 
            type="email" 
            v-model="email"
            placeholder="邮箱"
            class="register-input"
            @keyup.enter="handleRegister"
          />
          <span class="input-icon iconfont icon-youxiang"></span>
        </div>
        
        <div class="input-wrapper">
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="password"
            placeholder="密码"
            class="register-input"
            @keyup.enter="handleRegister"
          />
          <span 
            class="input-icon password-toggle iconfont" 
            :class="showPassword ? 'icon-yanjing' : 'icon-yanjing-guanbi'"
            @click="showPassword = !showPassword"
          ></span>
        </div>
        
        <div class="input-wrapper">
          <input 
            :type="showConfirmPassword ? 'text' : 'password'" 
            v-model="confirmPassword"
            placeholder="确认密码"
            class="register-input"
            @keyup.enter="handleRegister"
          />
          <span 
            class="input-icon password-toggle iconfont" 
            :class="showConfirmPassword ? 'icon-yanjing' : 'icon-yanjing-guanbi'"
            @click="showConfirmPassword = !showConfirmPassword"
          ></span>
        </div>
        
        <div class="register-links">
          <a href="#" class="login-link" @click.prevent="goToLogin">已有账号？立即登录</a>
        </div>
        
        <button class="register-btn" @click.prevent="handleRegister" :disabled="isRegistering">
          {{ isRegistering ? '注册中...' : '注册' }}
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
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isRegistering = ref(false)

// 眼睛元素引用
const eyeLeftRef = ref<HTMLElement | null>(null)
const eyeRightRef = ref<HTMLElement | null>(null)

// 瞳孔变换
const pupilTransformLeft = ref('translate(-50%, -50%)')
const pupilTransformRight = ref('translate(-50%, -50%)')

// 鼠标位置跟踪
const mousePosition = ref({ x: 0, y: 0 })
const isMouseMoving = ref(false)
let mouseMoveTimer: number | null = null

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

// 注册逻辑
const handleRegister = async (): Promise<void> => {
  if (!username.value || !email.value || !password.value || !confirmPassword.value) {
    alert('请填写所有字段')
    return
  }
  
  if (password.value !== confirmPassword.value) {
    alert('两次输入的密码不一致')
    return
  }
  
  if (password.value.length < 6) {
    alert('密码长度至少为6位')
    return
  }
  
  if (!email.value.includes('@') || !email.value.includes('.')) {
    alert('请输入有效的邮箱地址')
    return
  }
  
  isRegistering.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // 这里应该是实际的注册API调用
    // 模拟注册成功
    alert('注册成功！请登录')
    router.push('/')
    
  } catch (error) {
    alert('注册失败，请重试')
  } finally {
    isRegistering.value = false
  }
}

const goToLogin = (): void => {
  router.push('/')
}

const handleHelp = (): void => {
  alert('请填写注册信息\n密码长度至少6位\n邮箱格式需正确')
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.register-container {
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

.register-card-wrapper {
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

.register-card {
  position: relative;
  width: 380px;
  height: 550px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 15px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  z-index: 2;
  padding: 20px;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.register-title {
  text-align: center;
  margin-bottom: 30px;
  margin-top: 30px;
  font-size: 42px;
  color: #1e3c5c;
  font-weight: 700;
  letter-spacing: 1px;
}

.input-wrapper {
  position: relative;
  width: 260px;
  margin: 0 auto 20px;
}

.register-input {
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

.register-input:focus {
  border-color: rgb(11, 167, 175);
  box-shadow: 0 0 0 3px rgba(11, 167, 175, 0.2);
  background: white;
}

.register-input::placeholder {
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

.register-links {
  display: flex;
  justify-content: center;
  width: 260px;
  margin: 10px auto 20px;
}

.login-link {
  color: #004288bf;
  font-size: 14px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.login-link:hover {
  color: rgb(11, 167, 175);
  text-decoration: underline;
}

.register-btn {
  height: 44px;
  width: 140px;
  margin-top: 10px;
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

.register-btn:hover:not(:disabled) {
  background: rgb(8, 130, 136);
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(11, 167, 175, 0.4);
}

.register-btn:disabled {
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
  .register-card {
    width: 320px;
    height: 520px;
  }
}
</style>