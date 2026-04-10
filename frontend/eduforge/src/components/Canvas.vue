<!-- src/components/Canvas.vue -->
<template>
  <main class="canvas">
    <div v-if="currentSlide" class="slide" :style="{ background: currentSlide.bgColor || '#ffffff' }">
      <!-- 修复光标问题：使用 v-model 风格的绑定，但通过 contenteditable 实现 -->
      <h1
        contenteditable
        class="edit-title"
        @input="handleTitleInput"
        @keydown.enter.prevent
        @keydown.delete="handleTitleDelete"
        @blur="handleTitleBlur"
        data-placeholder="点击编辑标题"
        ref="titleRef"
      ></h1>
      
      <div
        contenteditable
        class="edit-content"
        @input="handleContentInput"
        @keydown.enter.prevent
        @blur="handleContentBlur"
        data-placeholder="点击编辑内容"
        ref="contentRef"
      ></div>

      <div 
        v-if="currentSlide.image" 
        class="slide-image"
        :style="{
          left: currentSlide.image.x + 'px',
          top: currentSlide.image.y + 'px',
          width: currentSlide.image.width + 'px',
          height: currentSlide.image.height + 'px'
        }"
      >
        <img :src="currentSlide.image.url" alt="配图" />
      </div>

      <div class="steps" v-if="currentSlide.steps?.length">
        <div class="step" v-for="(s, index) in currentSlide.steps" :key="s.id">
          <div class="step-num">{{ s.id }}</div>
          <div class="step-body">
            <div
              contenteditable
              class="step-title"
              @input="(e) => handleStepInput(s, 'title', e)"
              @keydown.enter.prevent
              @blur="(e) => handleStepBlur(s, 'title', e)"
              :data-step-index="index"
              data-placeholder="步骤标题"
              :ref="el => setStepTitleRef(el, index)"
            ></div>
            <div
              contenteditable
              class="step-desc"
              @input="(e) => handleStepInput(s, 'desc', e)"
              @blur="(e) => handleStepBlur(s, 'desc', e)"
              :data-step-index="index"
              data-placeholder="步骤描述"
              :ref="el => setStepDescRef(el, index)"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'

const props = defineProps({
  currentSlide: {
    type: Object,
    default: () => ({ title: '', content: '', bgColor: '#ffffff', steps: [] })
  }
})
const emit = defineEmits(['update-field', 'update-step'])

// 定义ref，用于初始化内容和维护光标
const titleRef = ref(null)
const contentRef = ref(null)
const stepTitleRefs = ref([])
const stepDescRefs = ref([])

// 记录当前是否正在编辑，避免重复更新
const isEditing = ref(false)

// 设置步骤标题引用
const setStepTitleRef = (el, index) => {
  if (el) {
    stepTitleRefs.value[index] = el
  }
}

// 设置步骤描述引用
const setStepDescRef = (el, index) => {
  if (el) {
    stepDescRefs.value[index] = el
  }
}

// 更新所有可编辑元素的内容
const updateEditableContent = async (newSlide) => {
  if (!newSlide || isEditing.value) return
  
  await nextTick()
  
  // 更新标题
  if (titleRef.value && titleRef.value.innerText !== newSlide.title) {
    titleRef.value.innerText = newSlide.title || ''
  }
  
  // 更新内容
  if (contentRef.value && contentRef.value.innerText !== newSlide.content) {
    contentRef.value.innerText = newSlide.content || ''
  }
  
  // 更新步骤
  if (newSlide.steps?.length) {
    newSlide.steps.forEach((step, index) => {
      if (stepTitleRefs.value[index] && stepTitleRefs.value[index].innerText !== (step.title || '')) {
        stepTitleRefs.value[index].innerText = step.title || ''
      }
      if (stepDescRefs.value[index] && stepDescRefs.value[index].innerText !== (step.desc || '')) {
        stepDescRefs.value[index].innerText = step.desc || ''
      }
    })
  }
}

// 监听currentSlide变化，更新可编辑元素内容
watch(
  () => props.currentSlide,
  (newSlide) => {
    updateEditableContent(newSlide)
  },
  { immediate: true, deep: true }
)

// 处理标题输入
const handleTitleInput = (e) => {
  isEditing.value = true
  emit('update-field', 'title', e.target.innerText)
  // 输入完成后立即重置编辑状态，但保留一点延迟避免闪烁
  setTimeout(() => {
    isEditing.value = false
  }, 100)
}

// 处理标题删除键（特殊处理空内容）
const handleTitleDelete = (e) => {
  // 如果内容为空，触发更新
  if (e.target.innerText === '') {
    emit('update-field', 'title', '')
  }
}

// 处理标题失焦
const handleTitleBlur = (e) => {
  isEditing.value = false
  // 确保空值被正确更新
  if (e.target.innerText !== props.currentSlide.title) {
    emit('update-field', 'title', e.target.innerText)
  }
}

// 处理内容输入
const handleContentInput = (e) => {
  isEditing.value = true
  emit('update-field', 'content', e.target.innerText)
  setTimeout(() => {
    isEditing.value = false
  }, 100)
}

// 处理内容失焦
const handleContentBlur = (e) => {
  isEditing.value = false
  if (e.target.innerText !== props.currentSlide.content) {
    emit('update-field', 'content', e.target.innerText)
  }
}

// 处理步骤输入
const handleStepInput = (step, field, e) => {
  isEditing.value = true
  emit('update-step', step, field, e.target.innerText)
  setTimeout(() => {
    isEditing.value = false
  }, 100)
}

// 处理步骤失焦
const handleStepBlur = (step, field, e) => {
  isEditing.value = false
  const currentValue = field === 'title' ? step.title : step.desc
  if (e.target.innerText !== currentValue) {
    emit('update-step', step, field, e.target.innerText)
  }
}

// 初始化ref数组
onMounted(() => {
  nextTick(() => {
    updateEditableContent(props.currentSlide)
  })
})
</script>

<style scoped>
.canvas {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(4px);
  overflow: auto;
}

.slide {
  position: relative;
  width: 1000px;
  height: 562.5px;
  background: #ffffff;
  border-radius: 24px;
  color: #2c3e50;
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  margin: 0 auto;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.slide:hover {
  transform: translateY(-4px);
  box-shadow: 0 30px 50px rgba(0, 0, 0, 0.2);
  border-color: rgba(11, 167, 175, 0.5);
}

.edit-title {
  font-size: 42px;
  font-weight: 700;
  outline: none;
  line-height: 1.3;
  color: #1e3c5c;
  margin: 0;
  padding: 0;
  cursor: text;
  min-height: 1.3em;
}

/* 修复placeholder样式：改用data-attribute */
.edit-title:empty:before {
  content: attr(data-placeholder);
  color: #94a3b8;
  font-weight: normal;
  pointer-events: none;
  cursor: text;
}

.edit-content {
  font-size: 18px;
  color: #34495e;
  outline: none;
  line-height: 1.6;
  cursor: text;
  min-height: 1.6em;
}

.edit-content:empty:before {
  content: attr(data-placeholder);
  color: #94a3b8;
  pointer-events: none;
  cursor: text;
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
}

.step {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  background: #f8fafc;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.step:hover {
  background: #ffffff;
  border-color: rgb(11, 167, 175);
  transform: translateX(4px);
}

.step-num {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 16px;
  flex-shrink: 0;
}

.step-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.step-title {
  font-size: 18px;
  font-weight: 600;
  outline: none;
  color: #1e3c5c;
  cursor: text;
  min-height: 1.5em;
}

.step-title:empty:before {
  content: attr(data-placeholder);
  color: #94a3b8;
  font-weight: normal;
  pointer-events: none;
  cursor: text;
}

.step-desc {
  font-size: 14px;
  color: #4a5568;
  outline: none;
  line-height: 1.6;
  cursor: text;
  min-height: 1.6em;
}

.step-desc:empty:before {
  content: attr(data-placeholder);
  color: #94a3b8;
  pointer-events: none;
  cursor: text;
}

.slide-image {
  position: absolute;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  cursor: move;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}

.slide-image:hover {
  border-color: rgb(11, 167, 175);
}

.slide-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 响应式 */
@media (max-width: 1400px) {
  .slide {
    width: 900px;
    height: 506.25px;
    padding: 36px;
  }
  
  .edit-title {
    font-size: 38px;
  }
}

@media (max-width: 1200px) {
  .slide {
    width: 800px;
    height: 450px;
    padding: 32px;
  }
  
  .edit-title {
    font-size: 34px;
  }
}
</style>