<!-- src/components/Sidebar.vue -->
<template>
  <aside class="sidebar">
    <button class="add-btn" @click="$emit('add-slide')">
      <span class="iconfont icon-xinjian"></span>
      新建页面
    </button>
    <div class="thumb-list">
      <div
        v-for="slide in slides"
        :key="slide.id"
        :class="{ active: slide.id === currentSlide?.id }"
        @click="$emit('select-slide', slide)"
        class="thumb-item"
      >
        <div class="thumb-preview" :style="{ background: slide.bgColor || '#ffffff' }">
          <img v-if="slide?.image?.url" :src="slide.image.url" class="thumb-img" />
          <span class="thumb-title">{{ slide.title || '无标题' }}</span>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  slides: { 
    type: Array, 
    required: true,
    default: () => []
  },
  currentSlide: { 
    type: Object,
    default: null
  }
})

defineEmits(['select-slide', 'add-slide'])
</script>

<style scoped>
.sidebar {
  width: 200px;
  background: #ffffff;
  border-right: 1px solid #e4e6e9;
  padding: 20px 12px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  height: 100%;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
}

.add-btn {
  padding: 12px;
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  background: #f8fafc;
  color: #475569;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.add-btn:hover {
  border-color: #0ba7af;
  color: #0ba7af;
  background: #f0f9ff;
}

.add-btn .iconfont {
  font-size: 16px;
}

.thumb-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.thumb-item {
  cursor: pointer;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.thumb-item:hover {
  transform: translateX(4px);
}

.thumb-item.active .thumb-preview {
  outline: 3px solid #0ba7af;
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.2);
}

.thumb-preview {
  width: 100%;
  height: 100px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1e293b;
  font-size: 12px;
  font-weight: 500;
  position: relative;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 8px;
  overflow: hidden;
}

.thumb-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
}

.thumb-title {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 4px 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  max-width: 90%;
  font-size: 12px;
  color: #1e293b;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
</style>