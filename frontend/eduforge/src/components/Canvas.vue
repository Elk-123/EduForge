<!-- src/components/Canvas.vue -->
<template>
  <main class="canvas">
    <div v-if="currentSlide" class="slide" :style="{ background: currentSlide.bgColor || '#ffffff' }">
      <h1
        contenteditable
        v-text="currentSlide.title"
        @input="$emit('update-field', 'title', $event.target.innerText)"
        class="edit-title"
        @keydown.enter.prevent
        :placeholder="'点击编辑标题'"
      ></h1>
      
      <div
        contenteditable
        v-text="currentSlide.content"
        @input="$emit('update-field', 'content', $event.target.innerText)"
        class="edit-content"
        :placeholder="'点击编辑内容'"
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
        <div class="step" v-for="s in currentSlide.steps" :key="s.id">
          <div class="step-num">{{ s.id }}</div>
          <div class="step-body">
            <div
              contenteditable
              v-text="s.title"
              @input="$emit('update-step', s, 'title', $event.target.innerText)"
              class="step-title"
              @keydown.enter.prevent
              :placeholder="'步骤标题'"
            ></div>
            <div
              contenteditable
              v-text="s.desc"
              @input="$emit('update-step', s, 'desc', $event.target.innerText)"
              class="step-desc"
              :placeholder="'步骤描述'"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
defineProps({
  currentSlide: {
    type: Object,
    default: () => ({ title: '', content: '', bgColor: '#ffffff', steps: [] })
  }
})
defineEmits(['update-field', 'update-step'])
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
  width: 1000px;  /* 缩小一点，16:9比例 */
  height: 562.5px; /* 1000/16*9 = 562.5 */
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
}

.edit-title:empty:before {
  content: attr(placeholder);
  color: #94a3b8;
  font-weight: normal;
}

.edit-content {
  font-size: 18px;
  color: #34495e;
  outline: none;
  line-height: 1.6;
}

.edit-content:empty:before {
  content: attr(placeholder);
  color: #94a3b8;
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
}

.step-title:empty:before {
  content: attr(placeholder);
  color: #94a3b8;
  font-weight: normal;
}

.step-desc {
  font-size: 14px;
  color: #4a5568;
  outline: none;
  line-height: 1.6;
}

.step-desc:empty:before {
  content: attr(placeholder);
  color: #94a3b8;
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

[contenteditable=true]:empty:before {
  content: attr(placeholder);
  color: #94a3b8;
  pointer-events: none;
  display: block;
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