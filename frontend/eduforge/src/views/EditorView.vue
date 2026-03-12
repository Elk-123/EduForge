<!-- src/views/EditorView.vue -->
<template>
  <div class="editor-view">
    <!-- 返回按钮 -->
    <div class="button-group">
      <button class="back-button outline-button icon-button" @click="goBack">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
    </div>

    <!-- PPT编辑器组件 -->
    <PPTEditor />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import PPTEditor from '@/components/PPTEditor.vue'

const router = useRouter()

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.editor-view {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  background: linear-gradient(
    to bottom,
    rgba(212, 245, 245, 0.2),
    rgba(130, 212, 215, 0.5) 25%,
    rgba(174, 230, 231, 0.5) 50%,
    rgba(189, 236, 236, 0.3) 75%,
    rgba(189, 236, 236, 0.3)
  );
}

.button-group {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 1000;
}

.outline-button {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 6px;
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #34495e;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.outline-button:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.15);
  border-color: rgb(11, 167, 175);
  color: rgb(11, 167, 175);
}
</style>