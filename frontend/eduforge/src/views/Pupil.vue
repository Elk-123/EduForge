<template>
  <div
    ref="pupilRef"
    class="pupil"
    :style="{
      width: `${size}px`,
      height: `${size}px`,
      backgroundColor: pupilColor,
      transform: `translate(${position.x}px, ${position.y}px)`,
      transition: 'transform 0.1s ease-out'
    }"
  />
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, inject } from 'vue'

// 接收父组件传递的props
const props = defineProps({
  size: { type: Number, default: 12 },
  maxDistance: { type: Number, default: 5 },
  pupilColor: { type: String, default: '#2D2D2D' },
  forceLookX: { type: Number },
  forceLookY: { type: Number }
})

// 从父组件注入鼠标坐标（父组件需要provide）
const mouseX = inject('mouseX')
const mouseY = inject('mouseY')

const pupilRef = ref(null)
const position = reactive({ x: 0, y: 0 })

// 更新瞳孔位置
const updatePosition = () => {
  if (!pupilRef.value) return

  // 优先使用强制位置
  if (props.forceLookX !== undefined && props.forceLookY !== undefined) {
    position.x = props.forceLookX
    position.y = props.forceLookY
    return
  }

  // 否则跟随鼠标
  const rect = pupilRef.value.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2

  const deltaX = mouseX.value - centerX
  const deltaY = mouseY.value - centerY
  const distance = Math.min(Math.sqrt(deltaX ** 2 + deltaY ** 2), props.maxDistance)

  const angle = Math.atan2(deltaY, deltaX)
  position.x = Math.cos(angle) * distance
  position.y = Math.sin(angle) * distance
}

onMounted(() => {
  window.addEventListener('mousemove', updatePosition)
  updatePosition()
})

onUnmounted(() => {
  window.removeEventListener('mousemove', updatePosition)
})
</script>

<style scoped>
.pupil {
  border-radius: 50%;
}
</style>