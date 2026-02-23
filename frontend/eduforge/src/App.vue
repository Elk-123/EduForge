<!-- frontend/eduforge/src/App.vue -->
<template>
  <div style="max-width: 600px; margin: 50px auto; font-family: sans-serif; padding: 20px; border: 1px solid #ccc; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <h2 style="text-align: center; color: #333;">EduForge 核心引擎点火自检</h2>
    
    <!-- 第一步：上传 -->
    <div style="margin-bottom: 30px; padding: 20px; background: #f9f9f9; border-radius: 8px;">
      <h3 style="margin-top: 0;">1. 上传 PDF 教案</h3>
      <input type="file" @change="handleFileUpload" accept="application/pdf" style="margin-bottom: 10px;"/>
      <p v-if="uploadStatus" :style="{ color: uploadStatus.includes('❌') ? 'red' : 'green', fontWeight: 'bold' }">
        {{ uploadStatus }}
      </p>
    </div>

    <!-- 第二步：生成 -->
    <div style="margin-bottom: 30px; padding: 20px; background: #f9f9f9; border-radius: 8px;">
      <h3 style="margin-top: 0;">2. AI 一键生成</h3>
      <button 
        @click="generatePPT" 
        :disabled="!filePath || isGenerating" 
        style="padding: 12px 24px; font-size: 16px; font-weight: bold; cursor: pointer; background: #1890ff; color: white; border: none; border-radius: 6px; width: 100%;"
        :style="{ opacity: (!filePath || isGenerating) ? 0.5 : 1 }"
      >
        {{ isGenerating ? '🧠 AI 大脑燃烧中 (LangGraph 工作流运行中...)' : '✨ 点击生成 PPT' }}
      </button>
      <p v-if="isGenerating" style="color: #666; margin-top: 10px; text-align: center; font-size: 14px;">
        请留意后端终端 (Terminal) 的进度日志...
      </p>
    </div>

    <!-- 第三步：下载 -->
    <div v-if="downloadUrl" style="padding: 20px; background: #e6f7ff; border-radius: 8px; text-align: center;">
      <h3 style="margin-top: 0;">3. 验收成果</h3>
      <a :href="'http://localhost:8000' + downloadUrl" target="_blank" style="font-size: 20px; color: #1890ff; font-weight: bold; text-decoration: none; display: block; padding: 10px; border: 2px dashed #1890ff; border-radius: 8px;">
        📥 下载生成的 PPTX 文件
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const filePath = ref('')
const uploadStatus = ref('')
const isGenerating = ref(false)
const downloadUrl = ref('')

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  uploadStatus.value = '⏳ 上传中...'
  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch('http://localhost:8000/api/upload', {
      method: 'POST',
      body: formData
    })
    const data = await res.json()
    filePath.value = data.file_path
    uploadStatus.value = '✅ 文件已就绪: ' + file.name
  } catch (err) {
    uploadStatus.value = '❌ 上传失败: 请检查后端 FastAPI 是否启动'
  }
}

const generatePPT = async () => {
  isGenerating.value = true
  downloadUrl.value = ''
  try {
    const res = await fetch('http://localhost:8000/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file_path: filePath.value })
    })
    const data = await res.json()
    if(data.status === 'success') {
      downloadUrl.value = data.download_url
    } else {
      alert("❌ 生成失败，返回异常")
    }
  } catch (error) {
    alert("❌ 生成请求失败，请查看后端控制台报错信息")
  } finally {
    isGenerating.value = false
  }
}
</script>