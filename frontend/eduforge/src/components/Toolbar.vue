<!-- src/components/Toolbar.vue -->
<template>
  <aside class="toolbar">
    <button class="tool-btn" title="搜索" @click="handleSearch">
      <span class="iconfont">&#xe628;</span>
    </button>
    <button class="tool-btn" title="文字样式" @click="handleFont">
      <span class="iconfont">&#xe69f;</span>
    </button>
    <button class="tool-btn" title="图片" @click="handleImage">
      <span class="iconfont">&#xe889;</span>
    </button>
    <button class="tool-btn" title="布局" @click="handleLayout">
      <span class="iconfont">&#xeb28;</span>
    </button>
    <button class="tool-btn" title="添加步骤" @click="handleAddStep">
      <span class="iconfont">&#xe679;</span>
    </button>
    <button class="tool-btn" title="删除步骤" @click="handleDelStep">
      <span class="iconfont">&#xe739;</span>
    </button>
    <button class="tool-btn" title="背景颜色" @click="handleBgColor">
      <span class="iconfont">&#xe6f8;</span>
    </button>
    <button class="tool-btn" title="预览" @click="handlePreview">
      <span class="iconfont">&#xe655;</span>
    </button>
    <button class="tool-btn" title="保存" @click="handleSave">
      <span class="iconfont">&#xec09;</span>
    </button>
   <button class="tool-btn" title="撤销" @click="handleUndo">
  <span class="iconfont icon-chexiao1-copy"></span>
</button>
    <button class="tool-btn" title="重做" @click="handleRedo">
      <span class="iconfont">&#xe604;</span>
    </button>
    <button class="tool-btn" title="导出" @click="handleExport">
      <span class="iconfont">&#xe63e;</span>
    </button>
  </aside>
</template>

<script setup>
const emit = defineEmits([
  'add-step', 
  'del-step', 
  'change-font', 
  'change-bg', 
  'search', 
  'add-image', 
  'change-layout', 
  'preview',
  'save',
  'undo',
  'redo',
  'export'
])

// 搜索 - 弹出搜索框
const handleSearch = () => {
  const keyword = prompt('请输入搜索关键词：', '')
  if (keyword !== null && keyword.trim() !== '') {
    emit('search', keyword)
  }
}

// 文字样式 - 弹出字体大小选择
const handleFont = () => {
  const sizes = [12, 14, 16, 18, 20, 24, 28, 32, 36, 42, 48]
  const sizeStr = prompt('请输入字体大小(px)：\n可选：12,14,16,18,20,24,28,32,36,42,48', '16')
  if (sizeStr !== null) {
    const size = parseInt(sizeStr)
    if (!isNaN(size) && size > 0) {
      emit('change-font', size)
    } else {
      alert('请输入有效的数字！')
    }
  }
}

// 图片 - 打开图片选择器
const handleImage = () => {
  emit('add-image')
}

// 布局 - 切换布局
const handleLayout = () => {
  const layouts = ['标准', '宽屏', '紧凑']
  const layoutStr = prompt('请选择布局：\n1. 标准\n2. 宽屏\n3. 紧凑', '1')
  if (layoutStr !== null) {
    const index = parseInt(layoutStr) - 1
    if (index >= 0 && index < layouts.length) {
      emit('change-layout', layouts[index])
    } else {
      alert('请输入1-3之间的数字！')
    }
  }
}

// 添加步骤
const handleAddStep = () => {
  emit('add-step')
}

// 删除步骤
const handleDelStep = () => {
  if (confirm('确定删除最后一个步骤吗？')) {
    emit('del-step')
  }
}

// 背景颜色
const handleBgColor = () => {
  const colors = ['白色', '浅灰', '冷灰', '暖白', '浅蓝', '浅绿', '浅粉', '浅紫']
  const colorStr = prompt('请选择背景颜色：\n1. 白色\n2. 浅灰\n3. 冷灰\n4. 暖白\n5. 浅蓝\n6. 浅绿\n7. 浅粉\n8. 浅紫', '1')
  if (colorStr !== null) {
    const index = parseInt(colorStr) - 1
    if (index >= 0 && index < colors.length) {
      emit('change-bg', index)
    } else {
      alert('请输入1-8之间的数字！')
    }
  }
}

// 预览
const handlePreview = () => {
  emit('preview')
}

// 保存
const handleSave = () => {
  emit('save')
}

// 撤销
const handleUndo = () => {
  emit('undo')
}

// 重做
const handleRedo = () => {
  emit('redo')
}

// 导出
const handleExport = () => {
  const formats = ['PPTX', 'PDF', '图片']
  const formatStr = prompt('请选择导出格式：\n1. PPTX\n2. PDF\n3. 图片', '1')
  if (formatStr !== null) {
    const index = parseInt(formatStr) - 1
    if (index >= 0 && index < formats.length) {
      emit('export', formats[index])
    } else {
      alert('请输入1-3之间的数字！')
    }
  }
}
</script>

<style scoped>
.toolbar {
  width: 60px;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
  gap: 12px;
  height: 100%;
  overflow-y: auto;
  flex-shrink: 0;
}

.tool-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.3);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.tool-btn:hover {
  background: white;
  color: #91a7ff;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(145, 167, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.3);
}

.toolbar::-webkit-scrollbar {
  width: 4px;
}

.toolbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

.toolbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}
</style>