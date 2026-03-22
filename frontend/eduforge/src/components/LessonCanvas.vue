<template>
  <div class="wps-editor">
    <!-- 左侧文档列表 - 添加包装器让滚动条贴边 -->
    <div class="sidebar-wrapper">
      <div class="sidebar">
        <button class="new-btn" @click="createDoc">
          <i class="iconfont icon-xinjian"></i> 新建文档
        </button>
        <div class="doc-list">
          <div v-for="(doc, idx) in docs" :key="doc.id" class="doc-item" :class="{ active: activeDoc === idx }" @click="switchDoc(idx)">
            <span>{{ doc.name }}</span>
            <button class="del-doc" @click.stop="deleteDoc(idx)">×</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 中间编辑区 -->
    <div class="canvas" ref="canvasRef" @scroll="onScroll">
      <div v-if="currentDoc" class="pages">
        <div v-for="(page, pageIdx) in currentDoc.pages" :key="page.id" class="page" :ref="el => setPageRef(el, pageIdx)">
          <div class="page-content" 
               contenteditable="true"
               :ref="el => setContentRef(el, pageIdx)"
               @input="(e) => onInput(pageIdx, e)"
               @keydown="onKeydown"
               @paste="onPaste"
               @click="(e) => onPageClick(pageIdx, e)">
          </div>
          <div class="page-num">{{ pageIdx + 1 }}</div>
        </div>
      </div>
      <div v-else class="empty-tip">点击左侧「新建文档」开始编辑</div>
    </div>

    <!-- 右侧工具栏 -->
    <div class="right-panel">
      <div class="toolbar">
        <button class="tool-btn" @click="addTextElement" title="添加文字">
          <i class="iconfont icon-wenziyangshi"></i>
        </button>
        <button class="tool-btn" @click="showShapeSelector = true" title="添加形状">
          <i class="iconfont icon-xingzhuang"></i>
        </button>
        <button class="tool-btn" @click="openImageUpload" title="添加图片">
          <i class="iconfont icon-tupian"></i>
        </button>
        <button class="tool-btn" @click="undo" title="撤销">
          <i class="iconfont icon-chexiao1-copy"></i>
        </button>
        <button class="tool-btn" @click="redo" title="重做">
          <i class="iconfont icon-zhongzuo"></i>
        </button>
        <button class="tool-btn" @click="openFind" title="查找">
          <i class="iconfont icon-sousuo"></i>
        </button>
        <button class="tool-btn" @click="exportToWord" title="导出Word">
          <i class="iconfont icon-daochu"></i>
        </button>
      </div>
      
      <div class="side-panel">
        <div class="panel-header">
          <h3>页面属性</h3>
        </div>
        <div class="panel-content">
          <div class="panel-section">
            <div class="property-item">
              <span class="property-label">背景:</span>
              <input type="color" v-model="currentPageBgColor" @change="updatePageBgColor" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 查找弹窗 -->
  <Teleport to="body">
    <div v-if="showFindModal" class="modal-overlay" @click.self="showFindModal = false">
      <div class="modal-content small">
        <div class="modal-header">
          <h3>查找</h3>
          <button class="close-btn" @click="showFindModal = false">×</button>
        </div>
        <div class="modal-body">
          <input type="text" v-model="findKeyword" placeholder="输入查找内容" class="find-input" />
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showFindModal = false">取消</button>
          <button class="confirm-btn" @click="doFind">查找</button>
        </div>
      </div>
    </div>
  </Teleport>

  <!-- 形状选择器悬浮窗 -->
  <Teleport to="body">
    <div v-if="showShapeSelector" class="modal-overlay" @click.self="showShapeSelector = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>选择形状</h3>
          <button class="close-btn" @click="showShapeSelector = false">×</button>
        </div>
        
        <div class="modal-body">
          <div class="shape-category">
            <h4>基础形状</h4>
            <div class="shape-grid">
              <div class="shape-item" @click="addShapeElement('rectangle')">
                <div class="shape-preview rectangle"></div>
                <span>矩形</span>
              </div>
              <div class="shape-item" @click="addShapeElement('square')">
                <div class="shape-preview square"></div>
                <span>正方形</span>
              </div>
              <div class="shape-item" @click="addShapeElement('circle')">
                <div class="shape-preview circle"></div>
                <span>圆形</span>
              </div>
              <div class="shape-item" @click="addShapeElement('ellipse')">
                <div class="shape-preview ellipse"></div>
                <span>椭圆</span>
              </div>
            </div>
          </div>

          <div class="shape-category">
            <h4>多边形</h4>
            <div class="shape-grid">
              <div class="shape-item" @click="addShapeElement('triangle')">
                <div class="shape-preview triangle"></div>
                <span>三角形</span>
              </div>
              <div class="shape-item" @click="addShapeElement('rightTriangle')">
                <div class="shape-preview right-triangle"></div>
                <span>直角△</span>
              </div>
            </div>
          </div>

          <div class="shape-category">
            <h4>箭头</h4>
            <div class="shape-grid">
              <div class="shape-item" @click="addShapeElement('arrowRight')">
                <div class="shape-preview arrow-right"></div>
                <span>右箭头</span>
              </div>
              <div class="shape-item" @click="addShapeElement('arrowLeft')">
                <div class="shape-preview arrow-left"></div>
                <span>左箭头</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>

  <!-- 图片上传隐藏输入框 -->
  <input type="file" ref="imageInput" class="hidden-input" accept="image/*" @change="handleImageUpload" />

  <div v-if="toastMsg" class="toast">{{ toastMsg }}</div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'

// ========== 数据 ==========
const docs = ref([])
const activeDoc = ref(-1)
const canvasRef = ref(null)
const pageRefs = ref([])
const contentRefs = ref([])
const toastMsg = ref('')

let splitTimer = null
let isSplitting = false

// 弹窗控制
const showFindModal = ref(false)
const showShapeSelector = ref(false)
const findKeyword = ref('')
const imageInput = ref(null)

// WPS标准页边距
const TOP_MARGIN = 96
const BOTTOM_MARGIN = 96
const LINE_HEIGHT = 24

// 当前页面背景色
const currentPageBgColor = computed(() => {
  return currentPage.value?.bgColor || '#ffffff'
})

// 当前文档
const currentDoc = computed(() => docs.value[activeDoc.value])
const currentPage = computed(() => currentDoc.value?.pages[activeDoc.value === -1 ? 0 : activeDoc.value] || null)

const showToast = (msg) => {
  toastMsg.value = msg
  setTimeout(() => { toastMsg.value = '' }, 1500)
}

// 创建空白页
const createPage = () => ({
  id: Date.now() + Math.random(),
  content: '',
  bgColor: '#ffffff'
})

// 创建新文档
const createDoc = () => {
  docs.value.push({
    id: Date.now(),
    name: `文档${docs.value.length + 1}`,
    pages: [createPage()]
  })
  activeDoc.value = docs.value.length - 1
  
  nextTick(() => {
    const firstContent = contentRefs.value[0]
    if (firstContent) firstContent.focus()
  })
  showToast('新建文档成功')
}

// 切换文档
const switchDoc = (idx) => {
  activeDoc.value = idx
  nextTick(() => {
    const content = contentRefs.value[0]
    if (content) content.focus()
    if (canvasRef.value) canvasRef.value.scrollTop = 0
  })
}

// 删除文档
const deleteDoc = (idx) => {
  if (docs.value.length <= 1) {
    showToast('至少保留一个文档')
    return
  }
  docs.value.splice(idx, 1)
  if (activeDoc.value >= idx) {
    activeDoc.value = Math.max(0, activeDoc.value - 1)
  }
}

// DOM 引用
const setPageRef = (el, idx) => { if (el) pageRefs.value[idx] = el }
const setContentRef = (el, idx) => { if (el) contentRefs.value[idx] = el }

// 获取页面内容最大高度
const getMaxContentHeight = (pageIdx) => {
  const page = pageRefs.value[pageIdx]
  if (!page) return 0
  return page.clientHeight - TOP_MARGIN - BOTTOM_MARGIN
}

// 检查页面是否已满
const isPageFull = (pageIdx) => {
  const content = contentRefs.value[pageIdx]
  if (!content) return false
  
  const contentHeight = content.scrollHeight
  const maxHeight = getMaxContentHeight(pageIdx)
  
  return contentHeight >= maxHeight - LINE_HEIGHT
}

// 将多余内容移到下一页
const splitToNextPage = async (pageIdx) => {
  if (isSplitting) return false
  isSplitting = true

  try {
    const contentEl = contentRefs.value[pageIdx]
    if (!contentEl) return false

    const html = contentEl.innerHTML
    if (!html.trim()) return false

    const maxHeight = getMaxContentHeight(pageIdx)

    const temp = document.createElement('div')
    temp.style.cssText = `
      position: absolute;
      visibility: hidden;
      width: ${contentEl.clientWidth}px;
      font-size: 12pt;
      line-height: 1.5;
      font-family: '宋体', 'SimSun', serif;
      white-space: pre-wrap;
      word-break: break-word;
      padding: 0;
    `
    document.body.appendChild(temp)

    let left = 0, right = html.length, splitPoint = 0
    while (left <= right) {
      const mid = Math.floor((left + right) / 2)
      temp.innerHTML = html.substring(0, mid)
      if (temp.scrollHeight <= maxHeight) {
        splitPoint = mid
        left = mid + 1
      } else {
        right = mid - 1
      }
    }

    let finalSplit = splitPoint
    for (let i = splitPoint; i >= Math.max(0, splitPoint - 100); i--) {
      const c = html[i]
      if (c === '\n' || c === '。' || c === '！' || c === '？' || c === '；' || c === '：') {
        finalSplit = i + 1
        break
      }
    }

    const keepHtml = html.substring(0, finalSplit)
    const moveHtml = html.substring(finalSplit)

    document.body.removeChild(temp)

    if (!moveHtml.trim()) return false

    contentEl.innerHTML = keepHtml
    currentDoc.value.pages[pageIdx].content = keepHtml

    let nextPage = currentDoc.value.pages[pageIdx + 1]
    if (!nextPage) {
      nextPage = createPage()
      currentDoc.value.pages.splice(pageIdx + 1, 0, nextPage)
    }

    await nextTick()

    const nextContent = contentRefs.value[pageIdx + 1]
    if (nextContent) {
      nextContent.innerHTML = moveHtml
      nextPage.content = moveHtml
    }

    setTimeout(() => {
      if (pageRefs.value[pageIdx + 1]) {
        pageRefs.value[pageIdx + 1].scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
      if (nextContent) {
        nextContent.focus()
        const range = document.createRange()
        const sel = window.getSelection()
        if (nextContent.firstChild) {
          range.setStart(nextContent.firstChild, 0)
          range.collapse(true)
          sel.removeAllRanges()
          sel.addRange(range)
        }
      }
    }, 100)

    return true

  } finally {
    setTimeout(() => { isSplitting = false }, 200)
  }
}

// 输入事件
const onInput = async (pageIdx, e) => {
  if (isSplitting) return

  if (currentDoc.value?.pages[pageIdx]) {
    currentDoc.value.pages[pageIdx].content = e.target.innerHTML
  }

  if (splitTimer) clearTimeout(splitTimer)
  
  splitTimer = setTimeout(async () => {
    if (isPageFull(pageIdx)) {
      await splitToNextPage(pageIdx)
    }
  }, 100)
}

// 粘贴事件
const onPaste = (e) => {
  e.preventDefault()
  const text = e.clipboardData.getData('text/plain')
  document.execCommand('insertText', false, text)
}

// 键盘事件
const onKeydown = (e) => {
  if (e.altKey) {
    e.preventDefault()
    return
  }

  if (e.ctrlKey && e.key === 'a' && e.target?.isContentEditable) {
    e.preventDefault()
    const sel = window.getSelection()
    if (sel) {
      const range = document.createRange()
      range.selectNodeContents(e.target)
      sel.removeAllRanges()
      sel.addRange(range)
    }
    return
  }

  if (e.key === 'Enter') {
    setTimeout(() => {
      const activePage = contentRefs.value.findIndex(el => el === document.activeElement)
      if (activePage >= 0 && isPageFull(activePage)) {
        splitToNextPage(activePage)
      }
    }, 10)
  }
}

// 光标定位功能
const onPageClick = (pageIdx, e) => {
  const contentEl = contentRefs.value[pageIdx]
  if (!contentEl) return
  
  contentEl.focus()
  
  const x = e.clientX
  const y = e.clientY
  
  let range = null
  if (document.caretRangeFromPoint) {
    range = document.caretRangeFromPoint(x, y)
  } else if (document.caretPositionFromPoint) {
    const caretPosition = document.caretPositionFromPoint(x, y)
    if (caretPosition) {
      range = document.createRange()
      range.setStart(caretPosition.offsetNode, caretPosition.offset)
      range.collapse(true)
    }
  }
  
  if (range) {
    const sel = window.getSelection()
    sel.removeAllRanges()
    sel.addRange(range)
  }
}

// 滚动同步
const onScroll = () => {
  if (!canvasRef.value) return
  const scrollTop = canvasRef.value.scrollTop
  
  for (let i = 0; i < pageRefs.value.length; i++) {
    const page = pageRefs.value[i]
    if (page && scrollTop >= page.offsetTop - 100 && scrollTop < page.offsetTop + page.offsetHeight - 100) {
      break
    }
  }
}

// 历史记录
const historyStack = ref([])
const historyIndex = ref(-1)

const saveHistory = () => {
  if (!currentDoc.value) return
  historyStack.value = historyStack.value.slice(0, historyIndex.value + 1)
  historyStack.value.push({
    docs: JSON.parse(JSON.stringify(docs.value)),
    activeDoc: activeDoc.value
  })
  historyIndex.value = historyStack.value.length - 1
  if (historyStack.value.length > 50) historyStack.value.shift()
}

const undo = () => {
  if (historyIndex.value <= 0) {
    showToast('没有可撤销的操作')
    return
  }
  historyIndex.value--
  const data = historyStack.value[historyIndex.value]
  docs.value = JSON.parse(JSON.stringify(data.docs))
  activeDoc.value = data.activeDoc
  
  nextTick(() => {
    for (let i = 0; i < contentRefs.value.length; i++) {
      const el = contentRefs.value[i]
      const page = currentDoc.value?.pages[i]
      if (el && page) {
        el.innerHTML = page.content || ''
      }
    }
  })
  showToast('撤销成功')
}

const redo = () => {
  if (historyIndex.value >= historyStack.value.length - 1) {
    showToast('没有可重做的操作')
    return
  }
  historyIndex.value++
  const data = historyStack.value[historyIndex.value]
  docs.value = JSON.parse(JSON.stringify(data.docs))
  activeDoc.value = data.activeDoc
  
  nextTick(() => {
    for (let i = 0; i < contentRefs.value.length; i++) {
      const el = contentRefs.value[i]
      const page = currentDoc.value?.pages[i]
      if (el && page) {
        el.innerHTML = page.content || ''
      }
    }
  })
  showToast('重做成功')
}

// 元素操作
const addTextElement = () => {
  if (!currentPage.value) {
    showToast('请先创建文档')
    return
  }
  const contentEl = contentRefs.value[activeDoc.value]
  if (contentEl) {
    contentEl.focus()
    document.execCommand('insertText', false, '请输入文字')
    saveHistory()
  }
}

const addShapeElement = (shapeType) => {
  if (!currentPage.value) {
    showToast('请先创建文档')
    return
  }
  showShapeSelector.value = false
  showToast(`添加${shapeType}形状`)
}

const updatePageBgColor = () => {
  if (!currentPage.value) return
  currentPage.value.bgColor = currentPageBgColor.value
  saveHistory()
}

const openFind = () => { showFindModal.value = true }
const doFind = () => {
  if (!findKeyword.value) return
  showToast(`查找：${findKeyword.value}`)
  showFindModal.value = false
}

const openImageUpload = () => { imageInput.value?.click() }
const handleImageUpload = (e) => {
  if (!currentPage.value || !e.target?.files?.length) return
  showToast(`上传图片：${e.target.files[0].name}`)
}

const exportToWord = () => {
  if (!currentDoc.value) {
    showToast('没有可导出的文档')
    return
  }
  showToast('正在导出Word...')
  setTimeout(() => showToast('导出成功！'), 1000)
}

// ========== 实时渲染接口 ==========
// 更新整个文档内容
const updateDocumentContent = (content) => {
  if (!currentDoc.value) return
  
  if (typeof content === 'string') {
    if (contentRefs.value[0]) {
      contentRefs.value[0].innerHTML = content
      currentDoc.value.pages[0].content = content
    }
  } 
  else if (typeof content === 'object') {
    content.pages?.forEach((pageContent, idx) => {
      if (contentRefs.value[idx]) {
        contentRefs.value[idx].innerHTML = pageContent
        if (currentDoc.value.pages[idx]) {
          currentDoc.value.pages[idx].content = pageContent
        }
      }
    })
  }
  
  saveHistory()
  showToast('内容已更新')
}

// 在光标位置插入内容
const insertAtCursor = (text, pageIndex = activePageIndex.value) => {
  const contentEl = contentRefs.value[pageIndex]
  if (!contentEl) return
  
  contentEl.focus()
  document.execCommand('insertText', false, text)
  
  if (currentDoc.value?.pages[pageIndex]) {
    currentDoc.value.pages[pageIndex].content = contentEl.innerHTML
  }
  saveHistory()
}

// 追加内容到指定页面
const appendContent = (text, pageIndex = activePageIndex.value) => {
  const contentEl = contentRefs.value[pageIndex]
  if (!contentEl) return
  
  const currentHtml = contentEl.innerHTML
  const newHtml = currentHtml + text
  contentEl.innerHTML = newHtml
  
  if (currentDoc.value?.pages[pageIndex]) {
    currentDoc.value.pages[pageIndex].content = newHtml
  }
  saveHistory()
}

// 替换指定页面的内容
const replaceContent = (text, pageIndex = activePageIndex.value) => {
  const contentEl = contentRefs.value[pageIndex]
  if (!contentEl) return
  
  contentEl.innerHTML = text
  
  if (currentDoc.value?.pages[pageIndex]) {
    currentDoc.value.pages[pageIndex].content = text
  }
  saveHistory()
}

// 获取当前所有文档内容
const getDocumentContent = () => {
  return currentDoc.value?.pages.map(page => page.content || '') || []
}

// 获取当前页内容
const getCurrentPageContent = () => {
  return contentRefs.value[activePageIndex.value]?.innerHTML || ''
}

// 暴露方法给父组件
defineExpose({
  updateDocumentContent,
  insertAtCursor,
  appendContent,
  replaceContent,
  getDocumentContent,
  getCurrentPageContent,
  createNewDocument: createDoc,
  switchPage: switchDoc
})

// ========== 后端接口预留 - 消息监听 ==========
const handleExternalMessage = (event) => {
  const { type, data } = event.data || {}
  
  if (!type) return
  
  switch (type) {
    case 'UPDATE_CONTENT':
      updateDocumentContent(data.content)
      break
    case 'INSERT_AT_CURSOR':
      insertAtCursor(data.text, data.pageIndex)
      break
    case 'APPEND_CONTENT':
      appendContent(data.text, data.pageIndex)
      break
    case 'GET_CONTENT':
      const content = getDocumentContent()
      window.postMessage({ type: 'CONTENT_RESPONSE', data: content }, '*')
      break
    default:
      console.log('未知消息类型:', type)
  }
}

// 清理
onUnmounted(() => {
  if (splitTimer) clearTimeout(splitTimer)
  window.removeEventListener('message', handleExternalMessage)
})

onMounted(() => {
  nextTick(() => {
    if (props.initialDocument) {
      documentList.value.push({ ...props.initialDocument, showPages: true })
      activeDocIndex.value = 0
      activePageIndex.value = 0
      saveToHistory()
    }
  })
  window.addEventListener('message', handleExternalMessage)
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.wps-editor {
  display: flex;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(
    to bottom,
    rgba(212, 245, 245, 0.2),
    rgba(130, 212, 215, 0.5) 25%,
    rgba(174, 230, 231, 0.5) 50%,
    rgba(189, 236, 236, 0.3) 75%,
    rgba(189, 236, 236, 0.3)
  );
  font-family: '宋体', 'SimSun', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 左侧面板包装器 - 负责滚动条，贴右侧边缘 */
.sidebar-wrapper {
  width: 220px;
  height: 100vh;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.5);
  position: relative;
}

/* 滚动条 - 紫色主题 */
.sidebar-wrapper::-webkit-scrollbar {
  width: 6px;
}

.sidebar-wrapper::-webkit-scrollbar-track {
  background: rgba(145, 167, 255, 0.1);
  border-radius: 10px;
}

.sidebar-wrapper::-webkit-scrollbar-thumb {
  background: #91a7ff;
  border-radius: 10px;
}

.sidebar-wrapper::-webkit-scrollbar-thumb:hover {
  background: #7c9eff;
}

/* 实际内容区域 - 无滚动条 */
.sidebar {
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px 16px;
  gap: 20px;
  box-sizing: border-box;
  background: transparent;
  backdrop-filter: none;
  border: none;
}

.new-btn {
  width: 100%;
  padding: 12px;
  border: 2px dashed rgba(145, 167, 255, 0.5);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.8);
  color: #1e3c5c;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 48px;
}

.new-btn:hover {
  border-color: #91a7ff;
  color: #91a7ff;
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-1px);
}

.doc-list {
  flex: 1;
  overflow-y: visible;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.doc-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.doc-item:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: #91a7ff;
}

.doc-item.active {
  background: rgba(145, 167, 255, 0.15);
  border-left: 3px solid #91a7ff;
}

.doc-item span {
  font-size: 14px;
  color: #1e293b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.del-doc {
  background: none;
  border: none;
  font-size: 18px;
  color: #94a3b8;
  cursor: pointer;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.del-doc:hover {
  background: #fee2e2;
  color: #ef4444;
}

/* 中间编辑区 */
.canvas {
  flex: 1;
  overflow-y: auto;
  padding: 32px 24px;
  background: rgba(255, 255, 255, 0.3);
}

.pages {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
  padding-bottom: 32px;
}

.page {
  width: 210mm;
  height: 297mm;
  background: white;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.page-content {
  height: 100%;
  padding: 2.54cm 3.17cm;
  font-size: 12pt;
  line-height: 1.5;
  font-family: '宋体', 'SimSun', serif;
  outline: none;
  white-space: pre-wrap;
  word-wrap: break-word;
  word-break: break-word;
  overflow: visible;
  cursor: text;
}

.page-content:focus {
  outline: none;
}

.page-content:empty:before {
  content: "点击开始输入...";
  color: #94a3b8;
  font-size: 12pt;
  pointer-events: none;
}

.page-num {
  position: absolute;
  bottom: 1.5cm;
  right: 3.17cm;
  font-size: 10pt;
  color: #94a3b8;
  font-family: '宋体', 'SimSun', serif;
  pointer-events: none;
}

.empty-tip {
  text-align: center;
  color: #94a3b8;
  font-size: 14px;
  margin-top: 100px;
}

.right-panel {
  display: flex;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255, 255, 255, 0.5);
  width: 280px;
  height: 100vh;
  flex-shrink: 0;
  padding: 0;
  margin: 0;
  overflow: hidden;
  position: relative;
}

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
  margin: 0;
  border: none;
  border-radius: 0;
  box-sizing: border-box;
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

.side-panel {
  width: 220px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  padding: 20px;
  overflow-y: auto;
  height: 100%;
  flex-shrink: 0;
  margin: 0;
  border: none;
  border-radius: 0;
  box-sizing: border-box;
}

.panel-header {
  margin-bottom: 20px;
}

.panel-header h3 {
  color: #1e3c5c;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(11, 167, 175, 0.2);
}

.panel-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.panel-section {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  padding: 12px;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.property-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.property-label {
  width: 35px;
  font-size: 12px;
  color: #1e3c5c;
}

.property-item input[type="color"] {
  width: 50px;
  height: 25px;
  padding: 2px;
  border: 1px solid #e0e7ff;
  border-radius: 4px;
}

/* 弹窗样式 */
.modal-overlay {
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

.modal-content {
  width: 500px;
  max-width: 90vw;
  max-height: 80vh;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-content.small {
  width: 350px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.modal-header h3 {
  color: white;
  font-size: 16px;
  margin: 0;
}

.close-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.3);
  color: white;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid #e0e7ff;
}

.cancel-btn {
  padding: 6px 12px;
  border: 1px solid #e0e7ff;
  border-radius: 4px;
  background: white;
  color: #1e3c5c;
  cursor: pointer;
}

.confirm-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  background: #91a7ff;
  color: white;
  cursor: pointer;
}

.find-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #e0e7ff;
  border-radius: 4px;
  outline: none;
}

/* 形状选择器 */
.shape-category {
  margin-bottom: 16px;
}

.shape-category h4 {
  color: #1e3c5c;
  font-size: 14px;
  margin-bottom: 8px;
}

.shape-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.shape-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  cursor: pointer;
  padding: 8px 4px;
  border-radius: 6px;
  transition: all 0.2s;
  background: #f8fafc;
}

.shape-item:hover {
  background: rgba(145, 167, 255, 0.1);
  transform: translateY(-1px);
}

.shape-preview {
  width: 36px;
  height: 36px;
  background-color: #91a7ff;
}

.shape-preview.rectangle { background-color: #91a7ff; }
.shape-preview.square { background-color: #91a7ff; }
.shape-preview.circle { border-radius: 50%; background-color: #91a7ff; }
.shape-preview.ellipse { border-radius: 50%; transform: scaleX(0.8); background-color: #91a7ff; }
.shape-preview.triangle {
  width: 0;
  height: 0;
  border-left: 18px solid transparent;
  border-right: 18px solid transparent;
  border-bottom: 36px solid #91a7ff;
  background: transparent;
}
.shape-preview.right-triangle {
  width: 0;
  height: 0;
  border-left: 0 solid transparent;
  border-right: 36px solid transparent;
  border-bottom: 36px solid #91a7ff;
  background: transparent;
}
.shape-preview.arrow-right {
  clip-path: polygon(0% 20%, 60% 20%, 60% 0%, 100% 50%, 60% 100%, 60% 80%, 0% 80%);
  background-color: #91a7ff;
}
.shape-preview.arrow-left {
  clip-path: polygon(40% 0%, 100% 20%, 100% 80%, 40% 100%, 0% 50%);
  background-color: #91a7ff;
}

.shape-item span {
  font-size: 10px;
  color: #1e3c5c;
}

.hidden-input {
  display: none;
}

.toast {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: #1e293b;
  color: white;
  padding: 8px 20px;
  border-radius: 24px;
  font-size: 13px;
  z-index: 1000;
  animation: fadeInUp 0.2s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* 滚动条 */
.canvas::-webkit-scrollbar,
.side-panel::-webkit-scrollbar,
.modal-body::-webkit-scrollbar,
.toolbar::-webkit-scrollbar {
  width: 4px;
}

.canvas::-webkit-scrollbar-track,
.side-panel::-webkit-scrollbar-track,
.modal-body::-webkit-scrollbar-track,
.toolbar::-webkit-scrollbar-track {
  background: rgba(145, 167, 255, 0.1);
  border-radius: 10px;
}

.canvas::-webkit-scrollbar-thumb,
.side-panel::-webkit-scrollbar-thumb,
.modal-body::-webkit-scrollbar-thumb,
.toolbar::-webkit-scrollbar-thumb {
  background: #91a7ff;
  border-radius: 10px;
}

@media print {
  .sidebar-wrapper, .right-panel {
    display: none;
  }
  .canvas {
    padding: 0;
    background: white;
  }
  .page {
    box-shadow: none;
    page-break-after: always;
    margin: 0;
  }
}
</style>