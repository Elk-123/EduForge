<!-- src/components/GifEditor.fixed.vue - 完整版，包含实时渲染接口 -->
<template>
  <div class="gif-editor">
    <!-- 左侧缩略图 -->
    <div class="sidebar-wrapper">
      <Sidebar
        :slides="gifs"
        :current-slide="currentGif"
        @select-slide="selectGif"
        @add-slide="addGif"
      />
    </div>

    <!-- 中间编辑画布 -->
    <div class="canvas-wrapper">
      <div class="gif-workspace">
        <!-- 动画预览区域 -->
        <div class="preview-area">
          <div class="preview-stage">
            <!-- 白板背景 -->
            <div class="stage-content" :style="stageStyle">
              <!-- 动画元素 -->
              <div v-for="element in currentElements" :key="element.id" 
                   class="anim-element"
                   :class="{ selected: selectedElement?.id === element.id }"
                   @click="selectElement(element)"
                   @mousedown="startDrag($event, element)"
                   :style="elementStyle(element)">
                
                <!-- 文本元素 - 双击弹窗编辑 -->
                <div v-if="element.type === 'text'" 
                     class="text-display"
                     :style="{ color: element.color, fontSize: element.fontSize + 'px' }"
                     @dblclick="openTextEdit(element)">
                  {{ element.content }}
                </div>
                
                <!-- 图片元素 -->
                <img v-if="element.type === 'image'" :src="element.url" class="element-image" draggable="false" />
                
                <!-- 形状元素 -->
                <div v-if="element.type === 'shape'" 
                     class="element-shape" 
                     :class="element.shapeType"
                     :style="shapeStyle(element)"></div>
              </div>
            </div>
            
            <!-- 播放控制 -->
            <div class="preview-controls">
              <button class="control-btn" @click="togglePlay" :title="currentGif?.isPlaying ? '暂停' : '播放'">
                <span class="iconfont" :class="currentGif?.isPlaying ? 'icon-zanting' : 'icon-bofang'"></span>
              </button>
              <button class="control-btn" @click="stopPlay" title="停止">
                <span class="iconfont icon-tingzhi"></span>
              </button>
              <div class="frame-indicator">
                {{ currentFrameIndex + 1 }} / {{ currentGif?.frames?.length || 1 }}
              </div>
            </div>
          </div>
        </div>

        <!-- 时间轴区域 -->
        <div class="timeline-area">
          <div class="timeline-header">
            <h3>时间轴</h3>
            <div class="timeline-tools">
              <button class="timeline-btn" @click="addFrame" title="添加帧">
                <span class="iconfont icon-jia"></span>
              </button>
              <button class="timeline-btn" @click="duplicateFrame" title="复制帧">
                <span class="iconfont icon-fuzhi"></span>
              </button>
              <button class="timeline-btn" @click="deleteFrame" title="删除帧">
                <span class="iconfont icon-shanchu"></span>
              </button>
              <span class="tool-divider"></span>
              <button class="timeline-btn" @click="undo" title="撤销">
                <span class="iconfont icon-chexiao1-copy"></span>
              </button>
              <button class="timeline-btn" @click="redo" title="还原">
                <span class="iconfont icon-zhongzuo"></span>
              </button>
            </div>
          </div>
          
          <!-- 帧列表 -->
          <div class="frames-list">
            <div v-for="(frame, index) in currentGif?.frames" :key="frame.id" 
                 class="frame-item"
                 :class="{ active: currentFrameIndex === index }"
                 @click="selectFrame(index)">
              <div class="frame-preview">
                <div class="frame-thumb">
                  <span class="frame-num">{{ index + 1 }}</span>
                </div>
              </div>
              <div class="frame-info">
                <div class="frame-duration">
                  <input type="number" 
                         v-model.number="frame.duration"
                         @change="updateFrame(frame)"
                         min="50"
                         max="2000"
                         step="50"
                         class="duration-input" />
                  <span class="duration-unit">ms</span>
                </div>
                <input type="text" 
                       v-model="frame.desc"
                       @change="updateFrame(frame)"
                       placeholder="帧描述"
                       class="frame-desc-input" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧工具栏 -->
    <div class="right-panel">
      <div class="gif-toolbar">
        <button class="tool-btn" @click="addTextElement" title="添加文字">
          <i class="iconfont icon-wenziyangshi"></i>
        </button>
        <button class="tool-btn" @click="showShapeSelector = true" title="添加形状">
          <i class="iconfont icon-xingzhuang"></i>
        </button>
        <button class="tool-btn" @click="openImageSelector" title="添加图片">
          <i class="iconfont icon-tupian"></i>
        </button>
        <button class="tool-btn" @click="openAIGenerate" title="AI生成动画">
          <i class="iconfont icon-jiqiren_o"></i>
        </button>
        <button class="tool-btn" @click="togglePlay" :title="currentGif?.isPlaying ? '暂停' : '播放'">
          <i class="iconfont" :class="currentGif?.isPlaying ? 'icon-zanting' : 'icon-bofang'"></i>
        </button>
        <button class="tool-btn" @click="stopPlay" title="停止">
          <i class="iconfont icon-tingzhi"></i>
        </button>
        <button class="tool-btn" @click="exportGif" title="导出GIF">
          <i class="iconfont icon-daochu"></i>
        </button>
        <button class="tool-btn" @click="undo" title="撤销">
          <i class="iconfont icon-chexiao1-copy"></i>
        </button>
        <button class="tool-btn" @click="redo" title="还原">
          <i class="iconfont icon-zhongzuo"></i>
        </button>
      </div>
      
      <!-- 右侧属性面板 -->
      <div class="side-panel">
        <div class="panel-header">
          <h3>元素属性</h3>
        </div>
        
        <div class="panel-content">
          <!-- 元素属性面板 -->
          <div class="panel-section" v-if="selectedElement">
            <div class="property-item">
              <span class="property-label">X:</span>
              <input type="number" v-model.number="selectedElement.x" @change="updateElement" />
            </div>
            <div class="property-item">
              <span class="property-label">Y:</span>
              <input type="number" v-model.number="selectedElement.y" @change="updateElement" />
            </div>
            <div class="property-item">
              <span class="property-label">宽:</span>
              <input type="number" v-model.number="selectedElement.width" @change="updateElement" />
            </div>
            <div class="property-item">
              <span class="property-label">高:</span>
              <input type="number" v-model.number="selectedElement.height" @change="updateElement" />
            </div>
            <div class="property-item">
              <span class="property-label">透明:</span>
              <input type="range" v-model.number="selectedElement.opacity" min="0" max="1" step="0.1" @change="updateElement" />
            </div>
            <div class="property-item">
              <span class="property-label">旋转:</span>
              <input type="range" v-model.number="selectedElement.rotation" min="0" max="360" step="1" @change="updateElement" />
            </div>
            <div class="property-item">
              <span class="property-label">缩放:</span>
              <input type="range" v-model.number="selectedElement.scale" min="0.1" max="3" step="0.1" @change="updateElement" />
            </div>
            <div class="property-item" v-if="selectedElement.type === 'text'">
              <span class="property-label">字号:</span>
              <input type="number" v-model.number="selectedElement.fontSize" min="8" max="72" @change="updateElement" />
            </div>
            <div class="property-item" v-if="selectedElement.type === 'text'">
              <span class="property-label">颜色:</span>
              <input type="color" v-model="selectedElement.color" @change="updateElement" />
            </div>
            <div class="property-item" v-if="selectedElement.type === 'shape'">
              <span class="property-label">填充:</span>
              <input type="color" v-model="selectedElement.fillColor" @change="updateElement" />
            </div>
            <div class="property-item" v-if="selectedElement.type === 'shape'">
              <span class="property-label">边框:</span>
              <input type="color" v-model="selectedElement.strokeColor" @change="updateElement" />
            </div>
            <div class="property-item" v-if="selectedElement.type === 'shape'">
              <span class="property-label">边框宽:</span>
              <input type="number" v-model.number="selectedElement.strokeWidth" min="0" max="10" @change="updateElement" />
            </div>
          </div>

          <!-- 白板背景设置 -->
          <div class="panel-section">
            <h4>白板背景</h4>
            <div class="property-item">
              <span class="property-label">颜色:</span>
              <input type="color" v-model="stageBgColor" @change="updateStageBgColor" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 搜索面板 -->
    <SearchPanel 
      v-if="showSearch"
      :slides="gifs"
      @close="showSearch = false"
      @navigate="goToGif"
    />

    <!-- 预览弹窗 -->
    <div v-if="showPreview" class="preview-modal" @click.self="showPreview = false">
      <div class="preview-content">
        <div class="preview-header">
          <h3>动画预览</h3>
          <button class="close-preview" @click="showPreview = false">×</button>
        </div>
        <div class="preview-slides">
          <div 
            v-for="(gif, index) in gifs" 
            :key="gif.id"
            class="preview-slide"
            :style="{ background: gif.bgColor }"
          >
            <h2>{{ gif.title || '无标题' }}</h2>
            <div class="preview-frames" v-if="gif.frames?.length">
              <div v-for="(frame, fIndex) in gif.frames" :key="frame.id" class="preview-frame">
                <span class="frame-num">{{ fIndex + 1 }}</span>
                <span class="frame-desc">{{ frame.desc }}</span>
                <span class="frame-duration">{{ frame.duration }}ms</span>
              </div>
            </div>
            <div class="preview-index">{{ index + 1 }}/{{ gifs.length }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 文字编辑弹窗 -->
    <Teleport to="body">
      <div v-if="showTextEditor" class="modal-overlay" @click.self="closeTextEditor">
        <div class="modal-content small">
          <div class="modal-header">
            <h3>编辑文字</h3>
            <button class="close-btn" @click="closeTextEditor">×</button>
          </div>
          <div class="modal-body">
            <textarea 
              v-model="editingText" 
              class="text-editor-modal"
              :style="{ fontSize: editingElement?.fontSize + 'px', color: editingElement?.color }"
              rows="4"
              placeholder="输入文字内容..."
              autofocus></textarea>
          </div>
          <div class="modal-footer">
            <button class="cancel-btn" @click="closeTextEditor">取消</button>
            <button class="confirm-btn" @click="saveTextEdit">确定</button>
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
            <!-- 基础形状 -->
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

            <!-- 多边形 -->
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
                <div class="shape-item" @click="addShapeElement('pentagon')">
                  <div class="shape-preview pentagon"></div>
                  <span>五边形</span>
                </div>
                <div class="shape-item" @click="addShapeElement('hexagon')">
                  <div class="shape-preview hexagon"></div>
                  <span>六边形</span>
                </div>
              </div>
            </div>

            <!-- 箭头 -->
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
                <div class="shape-item" @click="addShapeElement('arrowUp')">
                  <div class="shape-preview arrow-up"></div>
                  <span>上箭头</span>
                </div>
                <div class="shape-item" @click="addShapeElement('arrowDown')">
                  <div class="shape-preview arrow-down"></div>
                  <span>下箭头</span>
                </div>
              </div>
            </div>

            <!-- 特殊形状 -->
            <div class="shape-category">
              <h4>特殊形状</h4>
              <div class="shape-grid">
                <div class="shape-item" @click="addShapeElement('heart')">
                  <div class="shape-preview heart"></div>
                  <span>心形</span>
                </div>
                <div class="shape-item" @click="addShapeElement('star5')">
                  <div class="shape-preview star5"></div>
                  <span>五角星</span>
                </div>
                <div class="shape-item" @click="addShapeElement('diamond')">
                  <div class="shape-preview diamond"></div>
                  <span>菱形</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 图片选择器弹窗 -->
    <Teleport to="body">
      <div v-if="showSelector" class="modal-overlay" @click.self="closeSelector">
        <div class="modal-content">
          <div class="modal-header">
            <h3>选择图片</h3>
            <button class="close-btn" @click="closeSelector">×</button>
          </div>
          <div class="modal-body">
            <div class="image-selector-grid">
              <div v-for="img in images" :key="img.id" class="image-selector-item" @click="addImageElement(img)">
                <img :src="img.url" :alt="img.name" />
              </div>
              <div class="image-selector-item upload-item" @click="uploadImage">
                <span class="iconfont icon-shangchuan"></span>
                <span>上传</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- AI生成弹窗 -->
    <Teleport to="body">
      <div v-if="showAIPanel" class="modal-overlay" @click.self="showAIPanel = false">
        <div class="modal-content">
          <div class="modal-header">
            <h3>AI生成动画</h3>
            <button class="close-btn" @click="showAIPanel = false">×</button>
          </div>
          
          <div class="modal-body">
            <div class="ai-prompt">
              <label>输入提示词：</label>
              <textarea 
                v-model="aiPrompt" 
                placeholder="例如：一个小球从左向右滚动，同时放大并变色"
                rows="4"
                :disabled="aiGenerating"
              ></textarea>
            </div>
            
            <div v-if="aiGenerating" class="ai-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: aiProgress + '%' }"></div>
              </div>
              <div class="progress-text">生成中... {{ aiProgress }}%</div>
            </div>
            
            <div class="ai-suggestions">
              <h4>示例提示词：</h4>
              <div class="suggestion-chips">
                <span @click="aiPrompt = '一个红色小球弹跳'">一个红色小球弹跳</span>
                <span @click="aiPrompt = '文字从左边飞入，旋转放大'">文字从左边飞入，旋转放大</span>
                <span @click="aiPrompt = '渐变色圆形脉动效果'">渐变色圆形脉动效果</span>
                <span @click="aiPrompt = '箭头指示路径移动'">箭头指示路径移动</span>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button class="cancel-btn" @click="showAIPanel = false" :disabled="aiGenerating">取消</button>
            <button 
              class="confirm-btn" 
              @click="submitAIGenerate" 
              :disabled="!aiPrompt.trim() || aiGenerating"
            >
              {{ aiGenerating ? '生成中...' : '开始生成' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 保存提示 -->
    <div v-if="showToast" class="toast">{{ toastMessage }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './Sidebar.vue'
import SearchPanel from './SearchPanel.vue'

const route = useRoute()

// GIF数据
const gifs = ref([])
const currentIndex = ref(0)
const currentGif = computed(() => gifs.value[currentIndex.value])

const currentFrameIndex = ref(0)
const selectedElement = ref(null)
const animationTimer = ref(null)

// 拖拽相关
const isDragging = ref(false)
const dragOffset = ref({ x: 0, y: 0 })
const dragElement = ref(null)

// 白板背景颜色
const stageBgColor = ref('#ffffff')

// 图片管理
const images = ref([])
const showSelector = ref(false)

// 形状选择器
const showShapeSelector = ref(false)

// 文字编辑
const showTextEditor = ref(false)
const editingElement = ref(null)
const editingText = ref('')

// AI生成
const showAIPanel = ref(false)
const aiPrompt = ref('')
const aiGenerating = ref(false)
const aiProgress = ref(0)
const aiTaskId = ref(null)

// 预览和提示
const showPreview = ref(false)
const showSearch = ref(false)
const showToast = ref(false)
const toastMessage = ref('')
const history = ref([])
const historyIndex = ref(-1)

// 模拟图片数据
const mockImages = [
  { id: 1, name: '图片1', url: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200&h=200&fit=crop' },
  { id: 2, name: '图片2', url: 'https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=200&h=200&fit=crop' },
  { id: 3, name: '图片3', url: 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=200&h=200&fit=crop' },
  { id: 4, name: '图片4', url: 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=200&h=200&fit=crop' }
]

// 生成唯一ID
const generateId = () => {
  return 'id_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
}

// 当前帧的元素
const currentElements = computed(() => {
  return currentGif.value?.frames?.[currentFrameIndex.value]?.elements || []
})

// 舞台样式 - 白板
const stageStyle = computed(() => {
  return {
    width: (currentGif.value?.width || 800) + 'px',
    height: (currentGif.value?.height || 450) + 'px',
    position: 'relative',
    overflow: 'hidden',
    backgroundColor: stageBgColor.value,
    border: '1px solid #e0e7ff'
  }
})

// 元素样式
const elementStyle = (element) => {
  return {
    left: element.x + 'px',
    top: element.y + 'px',
    width: element.width + 'px',
    height: element.height + 'px',
    opacity: element.opacity,
    transform: `rotate(${element.rotation}deg) scale(${element.scale})`,
    transition: currentGif.value?.isPlaying ? `all ${currentGif.value.frameDuration/1000}s linear` : 'none',
    cursor: isDragging.value && dragElement.value?.id === element.id ? 'grabbing' : 'grab',
    position: 'absolute',
    zIndex: selectedElement.value?.id === element.id ? 100 : 1,
    userSelect: 'none'
  }
}

// 形状样式
const shapeStyle = (element) => {
  const baseStyles = {
    width: '100%',
    height: '100%',
    backgroundColor: element.fillColor || '#91a7ff',
    borderColor: element.strokeColor || '#a5b9ff',
    borderWidth: (element.strokeWidth || 1) + 'px',
    borderStyle: 'solid',
    boxSizing: 'border-box'
  }

  switch (element.shapeType) {
    case 'circle':
      return { ...baseStyles, borderRadius: '50%' }
    case 'ellipse':
      return { ...baseStyles, borderRadius: '50%', transform: 'scaleX(0.8)' }
    case 'triangle':
      return {
        width: 0,
        height: 0,
        borderLeft: (element.width/2) + 'px solid transparent',
        borderRight: (element.width/2) + 'px solid transparent',
        borderBottom: element.height + 'px solid ' + (element.fillColor || '#91a7ff'),
        backgroundColor: 'transparent',
        borderColor: `transparent transparent ${element.fillColor || '#91a7ff'} transparent`
      }
    case 'rightTriangle':
      return {
        width: 0,
        height: 0,
        borderLeft: '0 solid transparent',
        borderRight: element.width + 'px solid transparent',
        borderBottom: element.height + 'px solid ' + (element.fillColor || '#91a7ff'),
        backgroundColor: 'transparent',
        borderColor: `transparent transparent ${element.fillColor || '#91a7ff'} transparent`
      }
    case 'pentagon':
      return { ...baseStyles, clipPath: 'polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%)' }
    case 'hexagon':
      return { ...baseStyles, clipPath: 'polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%)' }
    case 'arrowRight':
      return { ...baseStyles, clipPath: 'polygon(0% 20%, 60% 20%, 60% 0%, 100% 50%, 60% 100%, 60% 80%, 0% 80%)' }
    case 'arrowLeft':
      return { ...baseStyles, clipPath: 'polygon(40% 0%, 100% 20%, 100% 80%, 40% 100%, 0% 50%)' }
    case 'arrowUp':
      return { ...baseStyles, clipPath: 'polygon(50% 0%, 100% 40%, 80% 40%, 80% 100%, 20% 100%, 20% 40%, 0% 40%)' }
    case 'arrowDown':
      return { ...baseStyles, clipPath: 'polygon(50% 100%, 100% 60%, 80% 60%, 80% 0%, 20% 0%, 20% 60%, 0% 60%)' }
    case 'heart':
      return { ...baseStyles, clipPath: 'path("M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z")' }
    case 'diamond':
      return { ...baseStyles, clipPath: 'polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)' }
    default:
      return baseStyles
  }
}

// 保存到历史记录
const saveToHistory = () => {
  const snapshot = JSON.parse(JSON.stringify(gifs.value))
  history.value = history.value.slice(0, historyIndex.value + 1)
  history.value.push(snapshot)
  historyIndex.value = history.value.length - 1
}

// 初始化
onMounted(() => {
  const title = route.query.title || '新动画页'
  gifs.value = [{
    id: generateId(),
    title: title,
    width: 800,
    height: 450,
    isPlaying: false,
    frameDuration: 300,
    bgColor: '#f5f0ff',
    frames: [
      {
        id: generateId(),
        desc: '初始状态',
        duration: 500,
        elements: [
          {
            id: generateId(),
            type: 'text',
            content: '双击编辑文字',
            x: 300,
            y: 200,
            width: 200,
            height: 50,
            fontSize: 24,
            color: '#1e3c5c',
            opacity: 1,
            rotation: 0,
            scale: 1
          }
        ]
      },
      {
        id: generateId(),
        desc: '中间状态',
        duration: 300,
        elements: [
          {
            id: generateId(),
            type: 'text',
            content: '动画进行中',
            x: 350,
            y: 200,
            width: 200,
            height: 50,
            fontSize: 28,
            color: '#ffaa00',
            opacity: 1,
            rotation: 5,
            scale: 1.2
          }
        ]
      },
      {
        id: generateId(),
        desc: '结束状态',
        duration: 500,
        elements: [
          {
            id: generateId(),
            type: 'text',
            content: '动画完成',
            x: 300,
            y: 200,
            width: 200,
            height: 50,
            fontSize: 24,
            color: '#91a7ff',
            opacity: 1,
            rotation: 0,
            scale: 1
          }
        ]
      }
    ]
  }]
  images.value = mockImages
  saveToHistory()
  
  // 添加消息监听
  window.addEventListener('message', handleExternalMessage)
})

// 卸载时清理
onUnmounted(() => {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  if (animationTimer.value) {
    clearInterval(animationTimer.value)
  }
  // 移除消息监听
  window.removeEventListener('message', handleExternalMessage)
})

// 播放控制
const togglePlay = () => {
  if (!currentGif.value) return
  currentGif.value.isPlaying = !currentGif.value.isPlaying
  
  if (currentGif.value.isPlaying) {
    startPlayback()
  } else {
    stopPlayback()
  }
}

const stopPlay = () => {
  if (!currentGif.value) return
  currentGif.value.isPlaying = false
  stopPlayback()
  currentFrameIndex.value = 0
}

const startPlayback = () => {
  if (animationTimer.value) clearInterval(animationTimer.value)
  
  animationTimer.value = setInterval(() => {
    const nextIndex = (currentFrameIndex.value + 1) % (currentGif.value?.frames?.length || 1)
    currentFrameIndex.value = nextIndex
  }, currentGif.value?.frameDuration || 300)
}

const stopPlayback = () => {
  if (animationTimer.value) {
    clearInterval(animationTimer.value)
    animationTimer.value = null
  }
}

// 页面管理
const selectGif = (gif) => { 
  currentIndex.value = gifs.value.findIndex(g => g.id === gif.id)
  currentFrameIndex.value = 0
  selectedElement.value = null
  dragElement.value = null
}

const addGif = () => {
  const newGif = { 
    id: generateId(),
    title: '新动画页',
    width: 800,
    height: 450,
    isPlaying: false,
    frameDuration: 300,
    bgColor: '#f5f0ff',
    frames: [{
      id: generateId(),
      desc: '新帧',
      duration: 300,
      elements: []
    }]
  }
  gifs.value.push(newGif)
  saveToHistory()
  showMessage('新动画页面添加成功')
}

// 帧管理
const selectFrame = (index) => {
  currentFrameIndex.value = index
  selectedElement.value = null
  dragElement.value = null
}

const addFrame = () => {
  if (!currentGif.value) return
  
  const lastFrame = currentGif.value.frames[currentGif.value.frames.length - 1]
  const newFrame = {
    id: generateId(),
    desc: '新帧',
    duration: 300,
    elements: lastFrame ? JSON.parse(JSON.stringify(lastFrame.elements)).map(e => {
      e.id = generateId()
      return e
    }) : []
  }
  currentGif.value.frames.push(newFrame)
  saveToHistory()
  showMessage('帧添加成功')
}

const duplicateFrame = () => {
  if (!currentGif.value) return
  
  const currentFrame = currentGif.value.frames[currentFrameIndex.value]
  if (currentFrame) {
    const newFrame = JSON.parse(JSON.stringify(currentFrame))
    newFrame.id = generateId()
    newFrame.desc = currentFrame.desc + ' (复制)'
    currentGif.value.frames.splice(currentFrameIndex.value + 1, 0, newFrame)
    saveToHistory()
    showMessage('帧复制成功')
  }
}

const deleteFrame = () => {
  if (!currentGif.value || currentGif.value.frames.length <= 1) {
    showMessage('至少保留一帧')
    return
  }
  
  currentGif.value.frames.splice(currentFrameIndex.value, 1)
  if (currentFrameIndex.value >= currentGif.value.frames.length) {
    currentFrameIndex.value = currentGif.value.frames.length - 1
  }
  selectedElement.value = null
  dragElement.value = null
  saveToHistory()
  showMessage('帧删除成功')
}

const updateFrame = (frame) => {
  saveToHistory()
}

// 元素管理
const selectElement = (element) => {
  if (!isDragging.value) {
    selectedElement.value = element
  }
}

// 文字编辑 - 弹窗方式
const openTextEdit = (element) => {
  editingElement.value = element
  editingText.value = element.content
  showTextEditor.value = true
}

const closeTextEditor = () => {
  showTextEditor.value = false
  editingElement.value = null
  editingText.value = ''
}

const saveTextEdit = () => {
  if (editingElement.value) {
    editingElement.value.content = editingText.value
    saveToHistory()
  }
  closeTextEditor()
}

// 拖拽功能 - 简单版本
const startDrag = (event, element) => {
  event.preventDefault()
  event.stopPropagation()
  
  isDragging.value = true
  dragElement.value = element
  selectedElement.value = element
  
  const rect = event.target.closest('.anim-element').getBoundingClientRect()
  dragOffset.value = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  }
  
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}

const onDrag = (event) => {
  if (!isDragging.value || !dragElement.value) return
  
  event.preventDefault()
  
  const stage = document.querySelector('.stage-content')
  if (!stage) return
  
  const stageRect = stage.getBoundingClientRect()
  
  let newX = event.clientX - stageRect.left - dragOffset.value.x
  let newY = event.clientY - stageRect.top - dragOffset.value.y
  
  newX = Math.max(0, Math.min(newX, stageRect.width - dragElement.value.width))
  newY = Math.max(0, Math.min(newY, stageRect.height - dragElement.value.height))
  
  dragElement.value.x = Math.round(newX)
  dragElement.value.y = Math.round(newY)
}

const stopDrag = () => {
  if (isDragging.value) {
    isDragging.value = false
    if (dragElement.value) {
      saveToHistory()
    }
    dragElement.value = null
    document.removeEventListener('mousemove', onDrag)
    document.removeEventListener('mouseup', stopDrag)
  }
}

// 添加文字元素
const addTextElement = () => {
  if (!currentGif.value) return
  
  const newElement = {
    id: generateId(),
    type: 'text',
    content: '新文字',
    x: 100,
    y: 100,
    width: 150,
    height: 40,
    fontSize: 20,
    color: '#1e3c5c',
    opacity: 1,
    rotation: 0,
    scale: 1
  }
  
  currentGif.value.frames[currentFrameIndex.value].elements.push(newElement)
  selectedElement.value = newElement
  saveToHistory()
  showMessage('文字添加成功')
}

// 添加形状元素
const addShapeElement = (shapeType) => {
  if (!currentGif.value) return
  
  const newElement = {
    id: generateId(),
    type: 'shape',
    shapeType: shapeType,
    x: 100,
    y: 100,
    width: 100,
    height: 100,
    fillColor: '#91a7ff',
    strokeColor: '#a5b9ff',
    strokeWidth: 1,
    opacity: 1,
    rotation: 0,
    scale: 1
  }
  
  // 根据形状类型调整默认宽高
  switch (shapeType) {
    case 'triangle':
    case 'rightTriangle':
      newElement.width = 100
      newElement.height = 86.6
      break
    case 'arrowRight':
    case 'arrowLeft':
      newElement.width = 120
      newElement.height = 80
      break
    case 'arrowUp':
    case 'arrowDown':
      newElement.width = 80
      newElement.height = 120
      break
  }
  
  currentGif.value.frames[currentFrameIndex.value].elements.push(newElement)
  selectedElement.value = newElement
  saveToHistory()
  showShapeSelector.value = false
  showMessage('形状添加成功')
}

// 添加图片元素
const addImageElement = (img) => {
  if (!currentGif.value) return
  
  const newElement = {
    id: generateId(),
    type: 'image',
    url: img.url,
    x: 100,
    y: 100,
    width: 200,
    height: 150,
    opacity: 1,
    rotation: 0,
    scale: 1
  }
  
  currentGif.value.frames[currentFrameIndex.value].elements.push(newElement)
  selectedElement.value = newElement
  saveToHistory()
  showSelector.value = false
  showMessage('图片添加成功')
}

const updateElement = () => {
  saveToHistory()
}

// 白板背景颜色
const updateStageBgColor = () => {
  // 这个只修改预览区域的背景色
  // 不保存到GIF数据中
}

// 图片选择器
const openImageSelector = () => {
  showSelector.value = true
}

const closeSelector = () => {
  showSelector.value = false
}

// 上传图片 - 预留后端接口
const uploadImage = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.multiple = true
  input.onchange = (e) => {
    const files = Array.from(e.target.files)
    
    // TODO: 替换为真实后端接口
    /*
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    
    const response = await fetch('/api/images/upload', {
      method: 'POST',
      body: formData
    })
    const data = await response.json()
    images.value = [...images.value, ...data.images]
    */
    
    // 模拟上传
    files.forEach(file => {
      const reader = new FileReader()
      reader.onload = (e) => {
        images.value.push({
          id: Date.now() + Math.random(),
          name: file.name,
          url: e.target.result
        })
      }
      reader.readAsDataURL(file)
    })
    showMessage(`${files.length}张图片上传成功`)
  }
  input.click()
}

// 搜索
const search = () => {
  showSearch.value = true
}

const goToGif = (gifId) => {
  const gif = gifs.value.find(g => g.id === gifId)
  if (gif) {
    selectGif(gif)
    showSearch.value = false
  }
}

// 导出GIF - 预留后端接口
const exportGif = () => {
  showMessage('正在导出GIF...')
  
  // TODO: 替换为真实后端接口
  /*
  // 调用导出接口
  const response = await fetch('/api/export/gif', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      projectId: currentGif.value.id,
      fps: 10,
      quality: 'high'
    })
  })
  const data = await response.json()
  
  // 轮询导出进度
  const taskId = data.taskId
  const interval = setInterval(async () => {
    const progressRes = await fetch(`/api/export/tasks/${taskId}`)
    const progressData = await progressRes.json()
    if (progressData.status === 'completed') {
      clearInterval(interval)
      window.location.href = `/api/export/download/${taskId}`
      showMessage('导出成功！')
    }
  }, 1000)
  */
  
  // 模拟导出
  setTimeout(() => {
    showMessage('导出成功！')
  }, 1000)
}

// 撤销 - 向后撤销
const undo = () => {
  if (historyIndex.value > 0) {
    historyIndex.value--
    gifs.value = JSON.parse(JSON.stringify(history.value[historyIndex.value]))
    currentGif.value = gifs.value[0]
    currentFrameIndex.value = 0
    selectedElement.value = null
    dragElement.value = null
    showMessage('撤销成功')
  } else {
    showMessage('没有可以撤销的操作')
  }
}

// 还原 - 向前撤销
const redo = () => {
  if (historyIndex.value < history.value.length - 1) {
    historyIndex.value++
    gifs.value = JSON.parse(JSON.stringify(history.value[historyIndex.value]))
    currentGif.value = gifs.value[0]
    currentFrameIndex.value = 0
    selectedElement.value = null
    dragElement.value = null
    showMessage('还原成功')
  } else {
    showMessage('没有可以还原的操作')
  }
}

// AI生成相关
const openAIGenerate = () => {
  showAIPanel.value = true
  aiPrompt.value = ''
  aiProgress.value = 0
}

// 提交AI生成任务 - 预留后端接口
const submitAIGenerate = async () => {
  if (!aiPrompt.value.trim() || !currentGif.value) return
  
  aiGenerating.value = true
  aiProgress.value = 0
  
  // TODO: 替换为真实后端接口
  /*
  try {
    const response = await fetch('/api/ai/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: aiPrompt.value,
        width: currentGif.value.width,
        height: currentGif.value.height,
        frameCount: 5,
        style: 'cartoon'
      })
    })
    const data = await response.json()
    
    // 轮询任务进度
    const taskId = data.taskId
    const interval = setInterval(async () => {
      const progressRes = await fetch(`/api/ai/tasks/${taskId}`)
      const progressData = await progressRes.json()
      aiProgress.value = progressData.progress
      
      if (progressData.status === 'completed') {
        clearInterval(interval)
        aiGenerating.value = false
        showAIPanel.value = false
        currentGif.value.frames = progressData.frames
        saveToHistory()
        showMessage('AI生成完成！')
      } else if (progressData.status === 'failed') {
        clearInterval(interval)
        aiGenerating.value = false
        showMessage('AI生成失败')
      }
    }, 1000)
  } catch (error) {
    console.error('AI生成失败:', error)
    aiGenerating.value = false
  }
  */
  
  // 模拟AI生成
  setTimeout(() => {
    // 生成示例帧
    const newFrames = []
    for (let i = 0; i < 5; i++) {
      newFrames.push({
        id: generateId(),
        desc: `AI生成帧 ${i + 1}`,
        duration: 300,
        elements: [
          {
            id: generateId(),
            type: 'text',
            content: `${aiPrompt.value} - ${i + 1}`,
            x: 300 + i * 20,
            y: 200,
            width: 150,
            height: 40,
            fontSize: 20 + i,
            color: `hsl(${i * 60}, 70%, 50%)`,
            opacity: 1,
            rotation: i * 10,
            scale: 1 + i * 0.1
          }
        ]
      })
    }
    currentGif.value.frames = newFrames
    saveToHistory()
    aiGenerating.value = false
    showAIPanel.value = false
    showMessage('AI生成完成！')
  }, 2000)
}

// ========== 实时渲染接口 ==========

// 添加新帧（动画帧）
const addFrameFromAI = (frameData) => {
  if (!currentGif.value) return
  
  const newFrame = {
    id: generateId(),
    desc: frameData.desc || `AI生成帧 ${currentGif.value.frames.length + 1}`,
    duration: frameData.duration || 300,
    elements: frameData.elements || []
  }
  
  currentGif.value.frames.push(newFrame)
  saveToHistory()
  showMessage('新帧添加成功')
  
  if (frameData.autoSelect) {
    currentFrameIndex.value = currentGif.value.frames.length - 1
  }
}

// 更新指定帧的元素
const updateFrameElements = (frameIndex, elements) => {
  if (!currentGif.value?.frames[frameIndex]) return
  
  currentGif.value.frames[frameIndex].elements = elements
  saveToHistory()
  showMessage('帧元素已更新')
}

// 添加元素到当前帧
const addElementToCurrentFrame = (elementData) => {
  if (!currentGif.value) return
  
  const newElement = {
    id: generateId(),
    ...elementData
  }
  
  currentGif.value.frames[currentFrameIndex.value].elements.push(newElement)
  saveToHistory()
  showMessage('元素添加成功')
}

// 更新动画属性
const updateAnimationProperty = (property, value) => {
  if (!currentGif.value) return
  currentGif.value[property] = value
  saveToHistory()
}

// 获取当前动画数据
const getAnimationData = () => {
  return currentGif.value
}

// 导出方法
defineExpose({
  addFrameFromAI,
  updateFrameElements,
  addElementToCurrentFrame,
  updateAnimationProperty,
  getAnimationData,
  addGif,
  selectFrame
})

// ========== 后端接口预留 - 消息监听 ==========
const handleExternalMessage = (event) => {
  const { type, data } = event.data || {}
  
  if (!type) return
  
  switch (type) {
    case 'ADD_FRAME':
      addFrameFromAI(data)
      break
    case 'UPDATE_FRAME_ELEMENTS':
      updateFrameElements(data.frameIndex, data.elements)
      break
    case 'ADD_ELEMENT':
      addElementToCurrentFrame(data)
      break
    case 'UPDATE_ANIMATION':
      updateAnimationProperty(data.property, data.value)
      break
    case 'GET_ANIMATION':
      const animationData = getAnimationData()
      window.postMessage({ type: 'ANIMATION_RESPONSE', data: animationData }, '*')
      break
    default:
      console.log('未知消息类型:', type)
  }
}

// 提示消息
const showMessage = (msg) => {
  toastMessage.value = msg
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 2000)
}
</script>

<style scoped>
/* 样式部分保持不变，和之前一样 */
.gif-editor {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: linear-gradient(
    to bottom,
    rgba(212, 245, 245, 0.2),
    rgba(130, 212, 215, 0.5) 25%,
    rgba(174, 230, 231, 0.5) 50%,
    rgba(189, 236, 236, 0.3) 75%,
    rgba(189, 236, 236, 0.3)
  );
  position: relative;
}

/* 左侧缩略图包装器 - 滚动条贴边 */
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

/* 实际内容区域 */
:deep(.sidebar) {
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

/* 新建按钮 */
:deep(.add-btn) {
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
  margin-top: 0;
  height: 48px;
}

:deep(.add-btn:hover) {
  border-color: #91a7ff;
  color: #91a7ff;
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-1px);
}

/* 缩略图项样式 */
:deep(.thumb-list) {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

:deep(.thumb-item) {
  cursor: pointer;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.8);
}

:deep(.thumb-item:hover) {
  background: rgba(255, 255, 255, 0.95);
  border-color: #91a7ff;
  transform: translateX(4px);
}

:deep(.thumb-item.active) {
  background: rgba(145, 167, 255, 0.15);
  border-left: 3px solid #91a7ff;
  border-radius: 8px;
}

:deep(.thumb-item.active .thumb-preview) {
  outline: none;
  box-shadow: none;
}

:deep(.thumb-preview) {
  width: 100%;
  height: 100px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1e293b;
  font-size: 12px;
  font-weight: 500;
  position: relative;
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  padding: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

:deep(.thumb-title) {
  background: rgba(255, 255, 255, 0.9) !important;
  color: #1e293b !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
  border-radius: 4px;
  padding: 4px 8px;
}

/* 画布区域 */
.canvas-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 30px;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(4px);
  overflow: auto;
}

.gif-workspace {
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(212, 245, 245, 0.2),
    rgba(130, 212, 215, 0.5) 25%,
    rgba(174, 230, 231, 0.5) 50%,
    rgba(189, 236, 236, 0.3) 75%,
    rgba(189, 236, 236, 0.3)
  );
  color: #1e3c5c;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

/* 预览区域 */
.preview-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  min-height: 0;
}

.preview-stage {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(145, 167, 255, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid rgba(145, 167, 255, 0.3);
}

.stage-content {
  background: #ffffff;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(145, 167, 255, 0.1);
  border: 1px solid #e0e7ff;
}

.anim-element {
  position: absolute;
  user-select: none;
  border: 2px solid transparent;
}

.anim-element:hover {
  border-color: #91a7ff;
}

.anim-element.selected {
  border-color: #ffaa00;
}

.text-display {
  width: 100%;
  height: 100%;
  padding: 4px;
  word-break: break-word;
  cursor: grab;
  overflow-y: auto;
  color: #1e3c5c;
}

.element-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  pointer-events: none;
}

.element-shape {
  width: 100%;
  height: 100%;
  pointer-events: none;
}

/* 播放控制 */
.preview-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
}

.control-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.3);
  color: #1e3c5c;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all 0.2s;
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.5);
  transform: scale(1.1);
}

.frame-indicator {
  background: rgba(255, 255, 255, 0.3);
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  color: #1e3c5c;
  margin-left: 10px;
}

/* 时间轴区域 - 浅色 */
.timeline-area {
  height: 240px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(145, 167, 255, 0.3);
  display: flex;
  flex-direction: column;
  padding: 15px 20px;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.timeline-header h3 {
  color: #1e3c5c;
  font-size: 16px;
  margin: 0;
}

.timeline-tools {
  display: flex;
  gap: 8px;
  align-items: center;
}

.tool-divider {
  width: 1px;
  height: 24px;
  background: rgba(145, 167, 255, 0.3);
  margin: 0 4px;
}

.timeline-btn {
  background: rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(145, 167, 255, 0.2);
  border-radius: 6px;
  color: #1e3c5c;
  padding: 6px 10px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s;
}

.timeline-btn:hover {
  background: rgba(255, 255, 255, 0.5);
  border-color: #91a7ff;
}

.frames-list {
  flex: 1;
  display: flex;
  gap: 15px;
  overflow-x: auto;
  padding: 5px 0;
}

.frame-item {
  width: 140px;
  flex-shrink: 0;
  background: white;
  border-radius: 8px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
  box-shadow: 0 2px 8px rgba(145, 167, 255, 0.1);
}

.frame-item:hover {
  border-color: #91a7ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(145, 167, 255, 0.2);
}

.frame-item.active {
  border-color: #91a7ff;
  background: rgba(145, 167, 255, 0.1);
}

.frame-preview {
  margin-bottom: 8px;
}

.frame-thumb {
  height: 80px;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.frame-num {
  font-size: 14px;
  color: white;
  font-weight: 600;
}

.frame-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.frame-duration {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.duration-input {
  width: 60px;
  background: white;
  border: 1px solid #e0e7ff;
  border-radius: 4px;
  padding: 4px;
  color: #1e3c5c;
  font-size: 12px;
}

.duration-input:focus {
  border-color: #91a7ff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(145, 167, 255, 0.2);
}

.duration-unit {
  color: #91a7ff;
}

.frame-desc-input {
  width: 100%;
  background: white;
  border: 1px solid #e0e7ff;
  border-radius: 4px;
  padding: 4px;
  color: #1e3c5c;
  font-size: 12px;
}

.frame-desc-input:focus {
  border-color: #91a7ff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(145, 167, 255, 0.1);
}

.frame-desc-input::placeholder {
  color: #a5b9ff;
}

.right-panel {
  display: flex;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255, 255, 255, 0.5);
  width: 280px;
  height: 100vh;
}

/* GIF工具栏 - 紫色渐变 */
.gif-toolbar {
  width: 60px;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
  gap: 12px;
  height: 100%;
  overflow-y: auto;
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
  font-size: 20px;
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

/* 右侧属性面板 */
.side-panel {
  flex: 1;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  padding: 15px;
  overflow-y: auto;
  height: 100%;
}

.panel-header {
  margin-bottom: 15px;
}

.panel-header h3 {
  color: #1e3c5c;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
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

.panel-section h4 {
  color: #1e3c5c;
  font-size: 13px;
  margin: 0 0 10px 0;
  font-weight: 500;
}

.property-item {
  display: flex;
  align-items: center;
  margin-bottom: 6px;
  gap: 6px;
}

.property-label {
  width: 35px;
  font-size: 12px;
  color: #1e3c5c;
}

.property-item input[type="number"] {
  width: 70px;
  background: white;
  border: 1px solid #e0e7ff;
  border-radius: 4px;
  padding: 4px;
  color: #1e3c5c;
  font-size: 12px;
}

.property-item input[type="range"] {
  flex: 1;
  padding: 0;
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

/* AI生成面板样式 */
.ai-prompt {
  margin-bottom: 20px;
}

.ai-prompt label {
  display: block;
  margin-bottom: 8px;
  color: #1e3c5c;
  font-size: 14px;
}

.ai-prompt textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e7ff;
  border-radius: 8px;
  font-size: 14px;
  resize: vertical;
  outline: none;
}

.ai-prompt textarea:focus {
  border-color: #91a7ff;
  box-shadow: 0 0 0 2px rgba(145, 167, 255, 0.1);
}

.ai-progress {
  margin: 20px 0;
}

.progress-bar {
  height: 8px;
  background: #e0e7ff;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: #91a7ff;
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  font-size: 13px;
  color: #1e3c5c;
}

.ai-suggestions {
  margin-top: 20px;
}

.ai-suggestions h4 {
  color: #1e3c5c;
  font-size: 14px;
  margin-bottom: 12px;
}

.suggestion-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.suggestion-chips span {
  padding: 6px 12px;
  background: #f8fafc;
  border: 1px solid #e0e7ff;
  border-radius: 20px;
  font-size: 12px;
  color: #1e3c5c;
  cursor: pointer;
  transition: all 0.2s;
}

.suggestion-chips span:hover {
  background: #91a7ff;
  color: white;
  border-color: #91a7ff;
}

/* 文字编辑弹窗 */
.text-editor-modal {
  width: 100%;
  padding: 8px;
  border: 1px solid #e0e7ff;
  border-radius: 4px;
  font-family: inherit;
  resize: vertical;
  outline: none;
  color: #1e3c5c;
}

.text-editor-modal:focus {
  border-color: #91a7ff;
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
.shape-preview.pentagon { clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%); background-color: #91a7ff; }
.shape-preview.hexagon { clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%); background-color: #91a7ff; }
.shape-preview.arrow-right { clip-path: polygon(0% 20%, 60% 20%, 60% 0%, 100% 50%, 60% 100%, 60% 80%, 0% 80%); background-color: #91a7ff; }
.shape-preview.arrow-left { clip-path: polygon(40% 0%, 100% 20%, 100% 80%, 40% 100%, 0% 50%); background-color: #91a7ff; }
.shape-preview.arrow-up { clip-path: polygon(50% 0%, 100% 40%, 80% 40%, 80% 100%, 20% 100%, 20% 40%, 0% 40%); background-color: #91a7ff; }
.shape-preview.arrow-down { clip-path: polygon(50% 100%, 100% 60%, 80% 60%, 80% 0%, 20% 0%, 20% 60%, 0% 60%); background-color: #91a7ff; }
.shape-preview.heart { clip-path: path("M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"); background-color: #91a7ff; }
.shape-preview.diamond { clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%); background-color: #91a7ff; }
.shape-preview.star5 { clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%); background-color: #91a7ff; }

.shape-item span {
  font-size: 10px;
  color: #1e3c5c;
}

/* 图片选择器 */
.image-selector-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.image-selector-item {
  aspect-ratio: 1;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.image-selector-item:hover {
  border-color: #91a7ff;
  transform: scale(1.02);
}

.image-selector-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-item {
  background: rgba(255, 255, 255, 0.6);
  border: 2px dashed rgba(145, 167, 255, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #91a7ff;
  font-size: 12px;
}

.upload-item .iconfont {
  font-size: 20px;
  margin-bottom: 2px;
}

/* 预览弹窗 */
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
  width: 600px;
  max-width: 90vw;
  max-height: 80vh;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: linear-gradient(135deg, #91a7ff, #e3eeff);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.preview-header h3 {
  color: white;
  font-size: 16px;
  margin: 0;
}

.close-preview {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.3);
  color: white;
  font-size: 16px;
  cursor: pointer;
}

.preview-slides {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.preview-slide {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(145, 167, 255, 0.1);
  position: relative;
  margin-bottom: 12px;
  border: 1px solid #e0e7ff;
}

.preview-slide h2 {
  font-size: 16px;
  color: #1e3c5c;
  margin-bottom: 8px;
}

.preview-frames {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.preview-frame {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  background: #f8fafc;
  border-radius: 4px;
  font-size: 12px;
  border: 1px solid #e0e7ff;
}

.preview-index {
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 10px;
  color: #91a7ff;
  background: rgba(255,255,255,0.9);
  padding: 2px 6px;
  border-radius: 10px;
  border: 1px solid #e0e7ff;
}

/* 提示 */
.toast {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: #91a7ff;
  color: white;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 13px;
  z-index: 3000;
  animation: slideUp 0.3s;
  box-shadow: 0 4px 12px rgba(145, 167, 255, 0.3);
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

/* 滚动条 */
.side-panel::-webkit-scrollbar,
.frames-list::-webkit-scrollbar,
.modal-body::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

.side-panel::-webkit-scrollbar-track,
.frames-list::-webkit-scrollbar-track,
.modal-body::-webkit-scrollbar-track {
  background: rgba(145, 167, 255, 0.1);
  border-radius: 10px;
}

.side-panel::-webkit-scrollbar-thumb,
.frames-list::-webkit-scrollbar-thumb,
.modal-body::-webkit-scrollbar-thumb {
  background: #91a7ff;
  border-radius: 10px;
}
</style>