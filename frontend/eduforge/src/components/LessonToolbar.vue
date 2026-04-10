<!-- src/components/LessonToolbar.vue - 教案专用工具栏，像WPS一样 -->
<template>
  <aside class="lesson-toolbar">
    <!-- 文件操作 -->
    <div class="tool-group">
      <div class="group-title">文件</div>
      <div class="tool-row">
        <button class="tool-btn" title="新建" @click="handleNew">
          <span class="iconfont icon-xinjian">📄</span>
        </button>
        <button class="tool-btn" title="打开" @click="handleOpen">
          <span class="iconfont icon-dakai">📂</span>
        </button>
        <button class="tool-btn" title="保存" @click="handleSave">
          <span class="iconfont icon-baocun">💾</span>
        </button>
        <button class="tool-btn" title="另存为" @click="handleSaveAs">
          <span class="iconfont icon-lingcunwei">📁</span>
        </button>
      </div>
      <div class="tool-row">
        <button class="tool-btn" title="导出PDF" @click="handleExport('pdf')">
          <span class="iconfont icon-pdf">📕</span>
        </button>
        <button class="tool-btn" title="导出Word" @click="handleExport('word')">
          <span class="iconfont icon-word">📘</span>
        </button>
        <button class="tool-btn" title="打印" @click="handlePrint">
          <span class="iconfont icon-dayin">🖨️</span>
        </button>
      </div>
    </div>

    <!-- 编辑操作 -->
    <div class="tool-group">
      <div class="group-title">编辑</div>
      <div class="tool-row">
        <button class="tool-btn" title="撤销" @click="handleUndo">
          <span class="iconfont icon-chexiao">↩</span>
        </button>
        <button class="tool-btn" title="重做" @click="handleRedo">
          <span class="iconfont icon-zhongzuo">↪</span>
        </button>
        <button class="tool-btn" title="剪切" @click="handleCut">
          <span class="iconfont icon-jianqie">✂️</span>
        </button>
        <button class="tool-btn" title="复制" @click="handleCopy">
          <span class="iconfont icon-fuzhi">📋</span>
        </button>
      </div>
      <div class="tool-row">
        <button class="tool-btn" title="粘贴" @click="handlePaste">
          <span class="iconfont icon-zhantie">📌</span>
        </button>
        <button class="tool-btn" title="全选" @click="handleSelectAll">
          <span class="iconfont icon-quanxuan">✓</span>
        </button>
        <button class="tool-btn" title="查找" @click="handleSearch">
          <span class="iconfont icon-sousuo">🔍</span>
        </button>
        <button class="tool-btn" title="替换" @click="handleReplace">
          <span class="iconfont icon-tihuan">🔄</span>
        </button>
      </div>
    </div>

    <!-- 文字格式 -->
    <div class="tool-group">
      <div class="group-title">字体</div>
      <div class="tool-row">
        <select class="font-family-select" v-model="fontFamily" @change="handleFontFamily">
          <option value="宋体">宋体</option>
          <option value="黑体">黑体</option>
          <option value="楷体">楷体</option>
          <option value="仿宋">仿宋</option>
          <option value="Arial">Arial</option>
          <option value="Times New Roman">Times New Roman</option>
        </select>
      </div>
      <div class="tool-row">
        <select class="font-size-select" v-model="fontSize" @change="handleFontSize">
          <option value="12">12px</option>
          <option value="14">14px</option>
          <option value="16">16px</option>
          <option value="18">18px</option>
          <option value="20">20px</option>
          <option value="22">22px</option>
          <option value="24">24px</option>
          <option value="28">28px</option>
          <option value="32">32px</option>
          <option value="36">36px</option>
          <option value="48">48px</option>
        </select>
      </div>
      <div class="tool-row">
        <button class="tool-btn" :class="{ active: isBold }" title="加粗" @click="handleBold">
          <span class="iconfont icon-jiacu">B</span>
        </button>
        <button class="tool-btn" :class="{ active: isItalic }" title="斜体" @click="handleItalic">
          <span class="iconfont icon-xieti">I</span>
        </button>
        <button class="tool-btn" :class="{ active: isUnderline }" title="下划线" @click="handleUnderline">
          <span class="iconfont icon-xiahuaxian">U</span>
        </button>
        <button class="tool-btn" :class="{ active: isStrikethrough }" title="删除线" @click="handleStrikethrough">
          <span class="iconfont icon-shanchuxian">S</span>
        </button>
      </div>
      <div class="tool-row">
        <button class="tool-btn" title="文字颜色" @click="handleTextColor">
          <span class="iconfont icon-yanse" :style="{ color: textColor }">A</span>
        </button>
        <button class="tool-btn" title="背景颜色" @click="handleBgColor">
          <span class="iconfont icon-beijingyanse" :style="{ background: bgColor }">ab</span>
        </button>
        <button class="tool-btn" title="清除格式" @click="handleClearFormat">
          <span class="iconfont icon-qingchu">🗑️</span>
        </button>
      </div>
    </div>

    <!-- 段落格式 -->
    <div class="tool-group">
      <div class="group-title">段落</div>
      <div class="tool-row">
        <button class="tool-btn" :class="{ active: alignLeft }" title="左对齐" @click="handleAlign('left')">
          <span class="iconfont icon-zuoduiqi">⫷</span>
        </button>
        <button class="tool-btn" :class="{ active: alignCenter }" title="居中对齐" @click="handleAlign('center')">
          <span class="iconfont icon-juzhongduiqi">☰</span>
        </button>
        <button class="tool-btn" :class="{ active: alignRight }" title="右对齐" @click="handleAlign('right')">
          <span class="iconfont icon-youduiqi">⫸</span>
        </button>
        <button class="tool-btn" :class="{ active: alignJustify }" title="两端对齐" @click="handleAlign('justify')">
          <span class="iconfont icon-liangduanduiqi">⇔</span>
        </button>
      </div>
      <div class="tool-row">
        <button class="tool-btn" title="减少缩进" @click="handleOutdent">
          <span class="iconfont icon-jiansuosuo">←</span>
        </button>
        <button class="tool-btn" title="增加缩进" @click="handleIndent">
          <span class="iconfont icon-zengjiasuosuo">→</span>
        </button>
        <button class="tool-btn" title="行距" @click="handleLineHeight">
          <span class="iconfont icon-xinggao">⤒</span>
        </button>
      </div>
    </div>

    <!-- 列表 -->
    <div class="tool-group">
      <div class="group-title">列表</div>
      <div class="tool-row">
        <button class="tool-btn" :class="{ active: isBulletList }" title="无序列表" @click="handleBulletList">
          <span class="iconfont icon-wuxuliebiao">•</span>
        </button>
        <button class="tool-btn" :class="{ active: isNumberList }" title="有序列表" @click="handleNumberList">
          <span class="iconfont icon-youxuliebiao">1.</span>
        </button>
        <button class="tool-btn" title="多级列表" @click="handleMultiLevelList">
          <span class="iconfont icon-duojiliebiao">1.1</span>
        </button>
      </div>
    </div>

    <!-- 插入 -->
    <div class="tool-group">
      <div class="group-title">插入</div>
      <div class="tool-row">
        <button class="tool-btn" title="插入表格" @click="handleInsertTable">
          <span class="iconfont icon-biaoge">▦</span>
        </button>
        <button class="tool-btn" title="插入图片" @click="handleInsertImage">
          <span class="iconfont icon-tupian">🖼️</span>
        </button>
        <button class="tool-btn" title="插入附件" @click="handleInsertAttachment">
          <span class="iconfont icon-fujian">📎</span>
        </button>
        <button class="tool-btn" title="插入链接" @click="handleInsertLink">
          <span class="iconfont icon-lianjie">🔗</span>
        </button>
      </div>
      <div class="tool-row">
        <button class="tool-btn" title="插入页眉" @click="handleInsertHeader">
          <span class="iconfont icon-yemei">⏉</span>
        </button>
        <button class="tool-btn" title="插入页脚" @click="handleInsertFooter">
          <span class="iconfont icon-yejiao">⏊</span>
        </button>
        <button class="tool-btn" title="插入页码" @click="handleInsertPageNumber">
          <span class="iconfont icon-yema">#</span>
        </button>
      </div>
    </div>

    <!-- 页面设置 -->
    <div class="tool-group">
      <div class="group-title">页面</div>
      <div class="tool-row">
        <button class="tool-btn" title="纸张大小" @click="handlePaperSize">
          <span class="iconfont icon-zhizhang">📄</span>
        </button>
        <button class="tool-btn" title="纸张方向" @click="handleOrientation">
          <span class="iconfont icon-fangxiang">↕️</span>
        </button>
        <button class="tool-btn" title="页边距" @click="handleMargins">
          <span class="iconfont icon-yebianju">⊞</span>
        </button>
      </div>
      <div class="tool-row">
        <button class="tool-btn" title="分栏" @click="handleColumns">
          <span class="iconfont icon-fenlan">‖</span>
        </button>
        <button class="tool-btn" title="分隔符" @click="handleBreak">
          <span class="iconfont icon-fengefu">⸻</span>
        </button>
      </div>
    </div>

    <!-- 预览查看 -->
    <div class="tool-group">
      <div class="group-title">视图</div>
      <div class="tool-row">
        <button class="tool-btn" title="预览" @click="handlePreview">
          <span class="iconfont icon-yulan">👁️</span>
        </button>
        <button class="tool-btn" title="放大" @click="handleZoomIn">
          <span class="iconfont icon-fangda">➕</span>
        </button>
        <button class="tool-btn" title="缩小" @click="handleZoomOut">
          <span class="iconfont icon-suoxiao">➖</span>
        </button>
        <button class="tool-btn" title="100%" @click="handleZoomReset">
          <span class="iconfont icon-baifenbi">100%</span>
        </button>
      </div>
    </div>

    <!-- 隐藏的颜色选择器 -->
    <input type="color" ref="textColorPicker" class="hidden-input" @change="onTextColorChange" />
    <input type="color" ref="bgColorPicker" class="hidden-input" @change="onBgColorChange" />
  </aside>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits([
  'new', 'open', 'save', 'save-as', 'export', 'print',
  'undo', 'redo', 'cut', 'copy', 'paste', 'select-all', 'search', 'replace',
  'font-family', 'font-size', 'bold', 'italic', 'underline', 'strikethrough',
  'text-color', 'bg-color', 'clear-format',
  'align', 'outdent', 'indent', 'line-height',
  'bullet-list', 'number-list', 'multi-level-list',
  'insert-table', 'insert-image', 'insert-attachment', 'insert-link',
  'insert-header', 'insert-footer', 'insert-page-number',
  'paper-size', 'orientation', 'margins', 'columns', 'break',
  'preview', 'zoom-in', 'zoom-out', 'zoom-reset'
])

// 状态
const fontFamily = ref('宋体')
const fontSize = ref('16')
const isBold = ref(false)
const isItalic = ref(false)
const isUnderline = ref(false)
const isStrikethrough = ref(false)
const textColor = ref('#000000')
const bgColor = ref('#ffffff')
const alignLeft = ref(true)
const alignCenter = ref(false)
const alignRight = ref(false)
const alignJustify = ref(false)
const isBulletList = ref(false)
const isNumberList = ref(false)

// 颜色选择器refs
const textColorPicker = ref(null)
const bgColorPicker = ref(null)

// 文件操作
const handleNew = () => emit('new')
const handleOpen = () => emit('open')
const handleSave = () => emit('save')
const handleSaveAs = () => emit('save-as')
const handleExport = (format) => emit('export', format)
const handlePrint = () => emit('print')

// 编辑操作
const handleUndo = () => emit('undo')
const handleRedo = () => emit('redo')
const handleCut = () => emit('cut')
const handleCopy = () => emit('copy')
const handlePaste = () => emit('paste')
const handleSelectAll = () => emit('select-all')
const handleSearch = () => emit('search')
const handleReplace = () => emit('replace')

// 字体操作
const handleFontFamily = () => emit('font-family', fontFamily.value)
const handleFontSize = () => emit('font-size', parseInt(fontSize.value))
const handleBold = () => {
  isBold.value = !isBold.value
  emit('bold', isBold.value)
}
const handleItalic = () => {
  isItalic.value = !isItalic.value
  emit('italic', isItalic.value)
}
const handleUnderline = () => {
  isUnderline.value = !isUnderline.value
  emit('underline', isUnderline.value)
}
const handleStrikethrough = () => {
  isStrikethrough.value = !isStrikethrough.value
  emit('strikethrough', isStrikethrough.value)
}
const handleTextColor = () => textColorPicker.value.click()
const onTextColorChange = (e) => {
  textColor.value = e.target.value
  emit('text-color', textColor.value)
}
const handleBgColor = () => bgColorPicker.value.click()
const onBgColorChange = (e) => {
  bgColor.value = e.target.value
  emit('bg-color', bgColor.value)
}
const handleClearFormat = () => emit('clear-format')

// 段落操作
const handleAlign = (type) => {
  alignLeft.value = type === 'left'
  alignCenter.value = type === 'center'
  alignRight.value = type === 'right'
  alignJustify.value = type === 'justify'
  emit('align', type)
}
const handleOutdent = () => emit('outdent')
const handleIndent = () => emit('indent')
const handleLineHeight = () => {
  const height = prompt('请输入行距（1.0-3.0）：', '1.5')
  if (height) emit('line-height', parseFloat(height))
}

// 列表操作
const handleBulletList = () => {
  isBulletList.value = !isBulletList.value
  if (isBulletList.value) isNumberList.value = false
  emit('bullet-list', isBulletList.value)
}
const handleNumberList = () => {
  isNumberList.value = !isNumberList.value
  if (isNumberList.value) isBulletList.value = false
  emit('number-list', isNumberList.value)
}
const handleMultiLevelList = () => emit('multi-level-list')

// 插入操作
const handleInsertTable = () => {
  const rows = prompt('请输入行数：', '3')
  const cols = prompt('请输入列数：', '3')
  if (rows && cols) emit('insert-table', { rows: parseInt(rows), cols: parseInt(cols) })
}
const handleInsertImage = () => emit('insert-image')
const handleInsertAttachment = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.pdf,.doc,.docx,.txt,.ppt,.pptx,.xls,.xlsx'
  input.onchange = (e) => {
    const file = e.target.files[0]
    if (file) emit('insert-attachment', file)
  }
  input.click()
}
const handleInsertLink = () => {
  const url = prompt('请输入链接地址：', 'https://')
  const text = prompt('请输入链接文字：', '点击查看')
  if (url && text) emit('insert-link', { url, text })
}
const handleInsertHeader = () => emit('insert-header')
const handleInsertFooter = () => emit('insert-footer')
const handleInsertPageNumber = () => emit('insert-page-number')

// 页面设置
const handlePaperSize = () => {
  const sizes = ['A4', 'A3', 'A5', 'B4', 'B5', '信纸', '法律用纸']
  const size = prompt('请选择纸张大小：\n1. A4\n2. A3\n3. A5\n4. B4\n5. B5\n6. 信纸\n7. 法律用纸', '1')
  if (size) emit('paper-size', sizes[parseInt(size) - 1])
}
const handleOrientation = () => {
  const ori = prompt('请选择纸张方向：\n1. 纵向\n2. 横向', '1')
  emit('orientation', ori === '1' ? 'portrait' : 'landscape')
}
const handleMargins = () => {
  const top = prompt('上边距（mm）：', '25.4')
  const bottom = prompt('下边距（mm）：', '25.4')
  const left = prompt('左边距（mm）：', '31.7')
  const right = prompt('右边距（mm）：', '31.7')
  if (top && bottom && left && right) emit('margins', { top, bottom, left, right })
}
const handleColumns = () => {
  const cols = prompt('请输入分栏数（1-4）：', '1')
  if (cols) emit('columns', parseInt(cols))
}
const handleBreak = () => {
  const types = ['分页符', '分栏符', '分节符']
  const type = prompt('请选择分隔符类型：\n1. 分页符\n2. 分栏符\n3. 分节符', '1')
  if (type) emit('break', types[parseInt(type) - 1])
}

// 视图操作
const handlePreview = () => emit('preview')
const handleZoomIn = () => emit('zoom-in')
const handleZoomOut = () => emit('zoom-out')
const handleZoomReset = () => emit('zoom-reset')
</script>

<style scoped>
.lesson-toolbar {
  width: 260px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255, 255, 255, 0.5);
  padding: 20px 12px;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: -2px 0 12px rgba(0, 0, 0, 0.05);
}

.tool-group {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  padding: 12px;
  border: 1px solid rgba(11, 167, 175, 0.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.group-title {
  font-size: 12px;
  font-weight: 600;
  color: #1e3c5c;
  margin-bottom: 8px;
  padding-bottom: 4px;
  border-bottom: 1px solid rgba(11, 167, 175, 0.2);
  letter-spacing: 0.5px;
}

.tool-row {
  display: flex;
  gap: 6px;
  margin-bottom: 6px;
  flex-wrap: wrap;
}

.tool-row:last-child {
  margin-bottom: 0;
}

.tool-btn {
  min-width: 36px;
  height: 32px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  color: #34495e;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: all 0.2s ease;
  padding: 0 6px;
  flex: 0 0 auto;
}

.tool-btn:hover {
  background: rgba(11, 167, 175, 0.1);
  color: rgb(11, 167, 175);
  border-color: rgb(11, 167, 175);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(11, 167, 175, 0.15);
}

.tool-btn.active {
  background: rgb(11, 167, 175);
  color: white;
  border-color: rgb(11, 167, 175);
}

.font-family-select,
.font-size-select {
  width: 100%;
  height: 32px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 0 8px;
  color: #34495e;
  font-size: 13px;
  outline: none;
  cursor: pointer;
  background: white;
  transition: all 0.2s ease;
}

.font-family-select:hover,
.font-size-select:hover {
  border-color: rgb(11, 167, 175);
}

.font-family-select:focus,
.font-size-select:focus {
  border-color: rgb(11, 167, 175);
  box-shadow: 0 0 0 2px rgba(11, 167, 175, 0.1);
}

.hidden-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  pointer-events: none;
}

/* 图标占位样式 */
.iconfont {
  font-style: normal;
  font-weight: normal;
}

/* 滚动条 */
.lesson-toolbar::-webkit-scrollbar {
  width: 4px;
}

.lesson-toolbar::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.02);
}

.lesson-toolbar::-webkit-scrollbar-thumb {
  background: rgba(11, 167, 175, 0.2);
  border-radius: 4px;
}

.lesson-toolbar::-webkit-scrollbar-thumb:hover {
  background: rgba(11, 167, 175, 0.4);
}

/* 响应式 */
@media (max-width: 1200px) {
  .lesson-toolbar {
    width: 220px;
  }
  
  .tool-btn {
    min-width: 32px;
    height: 30px;
    font-size: 13px;
  }
}
</style>