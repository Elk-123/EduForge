<!-- src/components/LessonEditor.vue - 修复版 -->
<template>
  <div class="lesson-editor">
    <!-- 中间编辑画布 - 传递初始文档数据 -->
    <LessonCanvas
      ref="canvasRef"
      :initial-document="initialDocument"
      @update-document="handleDocumentUpdate"
      @save="handleSave"
    />

    <!-- 搜索面板 -->
    <SearchPanel 
      v-if="showSearch"
      :slides="lessons"
      @close="showSearch = false"
      @navigate="goToLesson"
    />

    <!-- 预览弹窗 -->
    <div v-if="showPreview" class="preview-modal" @click.self="showPreview = false">
      <div class="preview-content">
        <div class="preview-header">
          <h3>教案预览</h3>
          <button class="close-preview" @click="showPreview = false">×</button>
        </div>
        <div class="preview-body" v-html="previewContent"></div>
      </div>
    </div>

    <!-- 保存提示 -->
    <div v-if="showSaveToast" class="save-toast">保存成功</div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import LessonCanvas from './LessonCanvas.vue'
import SearchPanel from './SearchPanel.vue'

const route = useRoute()
const canvasRef = ref(null)
const lessons = ref([])
const currentLesson = ref(null)
const showPreview = ref(false)
const showSearch = ref(false)
const showSaveToast = ref(false)
const previewContent = ref('')
const history = ref([])
const historyIndex = ref(-1)

// 生成初始教案数据，转换为 LessonCanvas 需要的格式
const generateInitialDocument = (title) => {
  const cleanTitle = title || '新教案'
  
  return {
    id: Date.now(),
    title: cleanTitle,
    showPages: true,
    pages: [
      {
        id: 1,
        title: cleanTitle,
        teacherLabel: '授课教师：',
        classLabel: '授课班级：',
        dateLabel: '授课时间：',
        periodLabel: '课时安排：',
        teacher: '',
        class: '',
        date: new Date().toLocaleDateString('zh-CN'),
        period: '1课时',
        objectives: ['', '', ''],
        keyPoints: { 重点: '', 难点: '' },
        methods: '',
        preparations: [''],
        steps: [],
        board: '',
        reflection: '',
        image: null,
        bgColor: '#ffffff',
        fontSize: 16,
        fontFamily: '宋体',
        content: ''
      }
    ]
  }
}

// 初始文档
const initialDocument = ref(null)

onMounted(() => {
  const title = route.query.title || '新教案'
  initialDocument.value = generateInitialDocument(title)
  
  // 同时初始化 lessons 用于搜索
  lessons.value = [{
    id: 1,
    title: title,
    content: ''
  }]
  currentLesson.value = lessons.value[0]
})

// 处理文档更新
const handleDocumentUpdate = (documentList) => {
  // 可以在这里保存到 lessons 用于搜索
  if (documentList && documentList.length > 0) {
    lessons.value = documentList.map((doc, index) => ({
      id: doc.id,
      title: doc.title || `文档${index + 1}`,
      content: doc.pages?.[0]?.content || ''
    }))
    currentLesson.value = lessons.value[0]
  }
  saveToHistory()
}

// 保存
const handleSave = () => {
  showSaveToast.value = true
  setTimeout(() => { showSaveToast.value = false }, 2000)
}

// 历史记录
const saveToHistory = () => {
  // 历史记录逻辑
}

// 搜索
const search = () => { showSearch.value = true }

const goToLesson = (lessonId) => {
  const lesson = lessons.value.find(l => l.id === lessonId)
  if (lesson) {
    currentLesson.value = lesson
    showSearch.value = false
  }
}

const preview = () => {
  if (canvasRef.value) {
    previewContent.value = '预览内容'
    showPreview.value = true
  }
}

const save = () => {
  localStorage.setItem('savedLesson', JSON.stringify(lessons.value))
  showSaveToast.value = true
  setTimeout(() => { showSaveToast.value = false }, 2000)
}

const undo = () => {
  // 撤销逻辑
}

const redo = () => {
  // 重做逻辑
}

const exportLesson = (format) => {
  alert(`正在导出为 ${format} 格式...`)
}
</script>

<style scoped>
.lesson-editor {
  display: flex;
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

.preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(5px);
}

.preview-content {
  width: 800px;
  max-width: 90vw;
  max-height: 90vh;
  background: white;
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.preview-header h3 {
  color: #1e293b;
  font-size: 18px;
  margin: 0;
}

.close-preview {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: #e2e8f0;
  color: #64748b;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-body {
  flex: 1;
  overflow-y: auto;
  padding: 30px;
  width: 210mm;
  margin: 0 auto;
  background: white;
  font-family: '宋体';
  line-height: 1.8;
}

.save-toast {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: rgb(11, 167, 175);
  color: white;
  padding: 10px 30px;
  border-radius: 30px;
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.3);
  z-index: 3000;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}
</style>