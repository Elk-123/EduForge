<template>
  <div
    ref="eyeRef"
    class="eye-ball"
    :style="{
      width: `${size}px`,
      height: isBlinking ? '2px' : `${size}px`,
      backgroundColor: eyeColor,
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      overflow: 'hidden',
      transition: 'all 0.15s ease'
    }"
  >
    <div
      v-if="!isBlinking"
      class="pupil-inner"
      :style="{
        width: `${pupilSize}px`,
        height: `${pupilSize}px`,
        backgroundColor: pupilColor,
        borderRadius: '50%',
        transform: `translate(${pupilPosition.x}px, ${pupilPosition.y}px)`,
        transition: 'transform 0.1s ease-out'
      }"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, inject } from 'vue'

const props = defineProps({
  size: { type: Number, default: 48 },
  pupilSize: { type: Number, default: 16 },
  maxDistance: { type: Number, default: 10 },
  eyeColor: { type: String, default: 'white' },
  pupilColor: { type: String, default: '#2D2D2D' },
  isBlinking: { type: Boolean, default: false },
  forceLookX: { type: Number },
  forceLookY: { type: Number }
})

const mouseX = inject('mouseX')
const mouseY = inject('mouseY')

const eyeRef = ref(null)
const pupilPosition = reactive({ x: 0, y: 0 })

const updatePupilPosition = () => {
  if (!eyeRef.value) return

  if (props.forceLookX !== undefined && props.forceLookY !== undefined) {
    pupilPosition.x = props.forceLookX
    pupilPosition.y = props.forceLookY
    return
  }

  const rect = eyeRef.value.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2

  const deltaX = mouseX.value - centerX
  const deltaY = mouseY.value - centerY
  const distance = Math.min(Math.sqrt(deltaX ** 2 + deltaY ** 2), props.maxDistance)

  const angle = Math.atan2(deltaY, deltaX)
  pupilPosition.x = Math.cos(angle) * distance
  pupilPosition.y = Math.sin(angle) * distance
}

onMounted(() => {
  window.addEventListener('mousemove', updatePupilPosition)
  updatePupilPosition()
})

onUnmounted(() => {
  window.removeEventListener('mousemove', updatePupilPosition)
})
</script>

<style scoped>
.eye-ball {
  /* 样式已在inline style中定义，这里仅做兜底 */
}
.pupil-inner {
  /* 样式已在inline style中定义 */
}
</style>