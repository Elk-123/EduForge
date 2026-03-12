<template>
  <div class="gradient-container" :class="{ 'has-outline': showOutline }">
    <!-- 返回按钮 -->
    <div class="button-group">
      <button class="back-button outline-button icon-button" @click="handleBack">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
    </div>

    <!-- 主标题区域 -->
    <div class="page-title">
      <h1>生成</h1>
      <p>您今天想创作什么？</p>
    </div>
    
    <!-- 两个方块：演示文稿和文档 -->
    <div class="block-container">
      <!-- 1 演示文稿 -->
      <div class="white-block block-item" 
           :class="{ active: activeBlock === 1 }"
           @click="handleBlockClick(1)">
        <div class="icon-wrapper">
          <span class="iconfont icon-xinjian_PPTyanshiwengao block-icon"></span>
        </div>
        <div class="block-text">演示文稿</div>
      </div>

      <!-- 2 文档 -->
      <div class="white-block block-item" 
           :class="{ active: activeBlock === 2 }"
           @click="handleBlockClick(2)">
        <div class="icon-wrapper">
          <span class="iconfont icon-wendang block-icon"></span>
        </div>
        <div class="block-text">文档</div>
      </div>
    </div>

    <!-- 下拉选择栏 -->
    <div class="select-bar">
      <!-- 卡片数量下拉 -->
      <div class="select-item" @click.stop="toggleDropdown('cardCount')">
        <span>{{ cardCount }}张卡片</span>
        <span class="iconfont icon-xiala select-arrow" :class="{ rotated: dropdownOpen.cardCount }"></span>
        <div v-if="dropdownOpen.cardCount" class="dropdown-menu">
          <div class="dropdown-item" @click.stop="selectCardCount(5)">5张卡片</div>
          <div class="dropdown-item" @click.stop="selectCardCount(10)">10张卡片</div>
          <div class="dropdown-item" @click.stop="selectCardCount(15)">15张卡片</div>
          <div class="dropdown-item" @click.stop="selectCardCount(20)">20张卡片</div>
        </div>
      </div>

      <!-- 语言下拉 -->
      <div class="select-item" @click.stop="toggleDropdown('language')">
        <span class="iconfont icon-yuyan select-icon"></span>
        <span>{{ selectedLanguage }}</span>
        <span class="iconfont icon-xiala select-arrow" :class="{ rotated: dropdownOpen.language }"></span>
        <div v-if="dropdownOpen.language" class="dropdown-menu">
          <div class="dropdown-item" @click.stop="selectLanguage('简体中文')">简体中文</div>
          <div class="dropdown-item" @click.stop="selectLanguage('繁体中文')">繁体中文</div>
          <div class="dropdown-item" @click.stop="selectLanguage('English')">English</div>
          <div class="dropdown-item" @click.stop="selectLanguage('日本語')">日本語</div>
        </div>
      </div>
    </div>

    <!-- 大输入框 -->
    <div class="input-container">
      <input 
        type="text" 
        class="main-input" 
        v-model="inputValue" 
        placeholder="描述您想生成的内容" 
        @keyup.enter="handleSend"
      />
      <button class="send-button" @click="handleSend" :disabled="isLoading">
        <svg v-if="!isLoading" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span v-else class="loading-spinner"></span>
      </button>
    </div>

    <!-- 大纲区域 - 生成后显示，替换示例提示 -->
    <div class="outline-section" v-if="showOutline" ref="outlineSectionRef">
      <!-- 白色底框 -->
      <div class="outline-white-box" ref="whiteBoxRef">
        <!-- 大纲标题 - 不可编辑 -->
        <div class="outline-header">
          <h2 class="outline-main-title">{{ mainTitle }}</h2>
          <span class="outline-main-subtitle">{{ subtitle }}</span>
        </div>

        <!-- 左键菜单 - 使用绝对定位，相对于白色底框，只在点击数字时显示 -->
        <div v-if="showContextMenu" class="context-menu" :style="{ 
          top: contextMenuY + 'px', 
          left: contextMenuX + 'px',
          position: 'absolute'
        }">
          <div class="context-menu-item" @click.stop="addBulletPoint">
            <span class="iconfont icon-tianjia"></span>
            添加要点
          </div>
          <div class="context-menu-item" @click.stop="addMultipleBulletPoints">
            <span class="iconfont icon-tianjia"></span>
            批量添加要点 (3个)
          </div>
          <div class="context-menu-divider"></div>
          <div class="context-menu-item" @click.stop="insertCardAbove">
            <span class="iconfont icon-xiala" style="transform: rotate(90deg);"></span>
            在上方插入卡片
          </div>
          <div class="context-menu-item" @click.stop="insertCardBelow">
            <span class="iconfont icon-xiala" style="transform: rotate(-90deg);"></span>
            在下方插入卡片
          </div>
          <div class="context-menu-divider"></div>
          <div class="context-menu-item delete" @click.stop="deleteCard">
            <span class="iconfont icon-shanchu"></span>
            删除卡片
          </div>
        </div>

        <!-- 大纲列表 - 彩色卡片，可编辑 -->
        <div class="outline-list">
          <div 
            v-for="(item, index) in outlineItems" 
            :key="index" 
            class="outline-item-wrapper"
          >
            <div 
              class="outline-item"
              :style="{ backgroundColor: getItemColor(index) }"
            >
              <div 
                class="item-number" 
                :class="{ 'clickable': true, 'ripple-active': activeNumber === index }"
                @click.left="handleNumberClick($event, index)"
                @animationend="activeNumber = null"
              >{{ index + 1 }}</div>
              <div class="item-content">
                <!-- 标题不可编辑，只显示 -->
                <div class="item-title">{{ item.title }}</div>
                
                <div v-if="item.description" class="item-description">{{ item.description }}</div>
                
                <!-- 子项列表 - 可编辑和删除 -->
                <div v-if="item.children && item.children.length" class="item-children">
                  <div 
                    v-for="(child, childIdx) in item.children" 
                    :key="childIdx + '-' + child + '-' + index"
                    class="child-item"
                  >
                    <span class="bullet">·</span>
                    <!-- 子项编辑模式 -->
                    <template v-if="editingChildIndex?.itemIndex === index && editingChildIndex?.childIndex === childIdx">
                      <input 
                        v-model="editChildText" 
                        class="edit-child-input"
                        @keyup.enter="saveChildEdit"
                        @keyup.esc="cancelChildEdit"
                        @blur="saveChildEdit"
                        ref="childInput"
                        @click.stop
                        @mousedown.stop
                      />
                    </template>
                    <!-- 子项显示模式 -->
                    <template v-else>
                      <span 
                        class="child-text" 
                        @click.left="handleChildLeftClick($event, index, childIdx, child)"
                      >{{ child }}</span>
                    </template>
                    <!-- 删除按钮 -->
                    <button class="delete-child-btn" @click.stop="deleteChildItem(index, childIdx)" title="删除">
                      <span class="iconfont icon-shanchu"></span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 添加卡片按钮 -->
          <div class="add-card-wrapper" @click.stop="handleAddCard">
            <button class="add-card-btn" :disabled="isAddingCard">
              <span class="iconfont icon-tianjia"></span>
              {{ isAddingCard ? '添加中...' : '添加卡片' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 底部操作栏 - 方块按钮样式 -->
      <div class="outline-footer">
        <div class="footer-content">
          <div class="footer-left">
            <div class="footer-label">请选择您的字体</div>
            <div class="style-blocks">
              <div 
                v-for="style in styleOptions" 
                :key="style"
                class="style-block" 
                :class="{ active: cardStyle === style }" 
                @click.stop="cardStyle = style"
              >
                {{ style }}
              </div>
            </div>
          </div>
          
          <div class="footer-right">
            <span class="total-cards">总共{{ outlineItems.length }}{{ activeBlock === 1 ? '张卡片' : '章节' }}</span>
            <button class="generate-btn" @click.stop="handleFinalGenerate">生成</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 示例提示区域 - 未生成时显示 -->
    <div class="example-section" v-else>
      <div class="example-title">示例提示</div>
      <div class="example-grid">
        <div class="example-card" v-for="(example, index) in exampleList" :key="index" @click="handleExampleClick(example)">
          <div class="example-content">
            <span class="iconfont icon-a-gongxiaoshanguangliangdian example-icon"></span>
            <span class="example-text">{{ example }}</span>
          </div>
          <div class="example-add">+</div>
        </div>
      </div>
      <button class="refresh-button" @click="handleRefreshExample">
        <span class="iconfont icon-xiala refresh-icon" style="transform: rotate(90deg);"></span>
        换一组
      </button>
    </div>

    <!-- 帮助按钮 -->
    <div class="help-button" @click="handleHelp">?</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, nextTick, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const activeBlock = ref<number | null>(null)
const inputValue = ref('')
const showOutline = ref(false)
const cardStyle = ref('简约')
const isLoading = ref(false)
const isAddingCard = ref(false)

// 主标题和副标题 - 不可编辑
const mainTitle = ref('')
const subtitle = ref('')

// 子项编辑相关
const editingChildIndex = ref<{ itemIndex: number; childIndex: number } | null>(null)
const editChildText = ref('')
const childInput = ref<HTMLInputElement | null>(null)

// 左键菜单相关 - 只在点击数字时显示
const showContextMenu = ref(false)
const contextMenuX = ref(0)
const contextMenuY = ref(0)
const contextMenuItemIndex = ref<number | null>(null)
const contextMenuChildIndex = ref<number | null>(null)

// 点击数字动画相关
const activeNumber = ref<number | null>(null)

// 引用白色底框元素
const whiteBoxRef = ref<HTMLElement | null>(null)

const dropdownOpen = ref({
  cardCount: false,
  language: false
})

const cardCount = ref(10)
const selectedLanguage = ref('简体中文')

// API 基础URL
const API_BASE_URL = 'http://localhost:8000/api/v1'

// 根据类型显示不同的样式选项
const styleOptions = computed(() => {
  return activeBlock.value === 1 ? ['简约', '简洁', '详细', '宽泛'] : ['简约', '标准', '详细', '学术']
})

const exampleList = ref<string[]>([
  "我从100多位首席执行官身上学到的时间管理秘诀",
  "为失去动力的创作者提供3个建议",
  "给'过于和蔼可亲'的教师的课堂管理建议",
  "从0到1000个订阅者：我希望拥有的路线图",
  "每个人都在做却没人在会议上承认的事",
  "职场沟通的高效表达技巧"
])

// 清新配色
const itemColors = [
  'rgba(74, 208, 226, 0.15)',
  'rgba(243, 156, 18, 0.12)',
  'rgba(155, 89, 182, 0.12)',
  'rgba(46, 204, 113, 0.12)',
  'rgba(231, 76, 60, 0.12)',
  'rgba(52, 152, 219, 0.12)',
  'rgba(241, 196, 15, 0.12)',
  'rgba(26, 188, 156, 0.12)'
]

// 大纲数据
const outlineTitle = computed(() => {
  return activeBlock.value === 1 
    ? '大数据教材精华：开启数据时代的大门'
    : '大数据教材：从入门到精通'
})

const outlineSubtitle = computed(() => {
  return activeBlock.value === 1
    ? '什么是大数据？'
    : '一本全面介绍大数据技术与应用的教材'
})

// 初始化主标题和副标题
watch([outlineTitle, outlineSubtitle], ([newTitle, newSubtitle]) => {
  if (showOutline.value) {
    mainTitle.value = newTitle
    subtitle.value = newSubtitle
  }
})

interface OutlineItem {
  title: string
  description: string
  children: string[]
}

const outlineItems = ref<OutlineItem[]>([])

// 根据卡片数量生成不同的大纲
const generateOutlineByCount = (count: number, type: number): OutlineItem[] => {
  if (type === 2) {
    // 文档类型 - 最多10种
    const docTemplates: OutlineItem[] = [
      {
        title: '大数据概述',
        description: '了解大数据的基本概念、发展历程和应用场景。',
        children: [
          '大数据的定义和特征（4V特征）',
          '大数据的发展历程和现状',
          '大数据的应用场景和行业案例'
        ]
      },
      {
        title: '大数据技术架构',
        description: '深入理解大数据技术的核心架构和生态系统。',
        children: [
          'Hadoop生态系统概述',
          'HDFS分布式文件系统',
          'MapReduce计算框架'
        ]
      },
      {
        title: '数据采集与预处理',
        description: '学习如何采集和预处理各类数据。',
        children: [
          '数据源的类型和特点',
          '数据采集工具（Flume、Sqoop）',
          '数据清洗和预处理方法'
        ]
      },
      {
        title: '数据存储与管理',
        description: '掌握大数据存储技术和管理策略。',
        children: [
          'NoSQL数据库介绍',
          'HBase列式存储',
          'Hive数据仓库'
        ]
      },
      {
        title: '数据处理与分析',
        description: '学习数据处理和分析的方法。',
        children: [
          '批处理与流处理',
          'Spark计算框架',
          'Flink实时计算'
        ]
      },
      {
        title: '数据可视化',
        description: '掌握数据可视化工具和技术。',
        children: [
          '可视化设计原则',
          'ECharts使用',
          'Tableau应用'
        ]
      },
      {
        title: '机器学习基础',
        description: '了解机器学习在数据分析中的应用。',
        children: [
          '监督学习',
          '无监督学习',
          '深度学习简介'
        ]
      },
      {
        title: '大数据安全',
        description: '学习大数据安全保护措施。',
        children: [
          '数据加密',
          '访问控制',
          '隐私保护'
        ]
      },
      {
        title: '性能优化',
        description: '掌握大数据系统性能优化方法。',
        children: [
          '查询优化',
          '资源调度',
          '缓存策略'
        ]
      },
      {
        title: '案例分析',
        description: '实际大数据项目案例分析。',
        children: [
          '电商推荐系统',
          '金融风控',
          '智慧城市'
        ]
      }
    ]
    return docTemplates.slice(0, Math.min(count, docTemplates.length))
  } else {
    // PPT类型 - 最多20种
    const pptTemplates: OutlineItem[] = [
      {
        title: '数据量巨大，预计2020年全球数据量达35ZB，约是2010年的30倍',
        description: '',
        children: [
          '数据类型多样，90%为非结构化数据，如文本、图片、视频等',
          '处理速度快，实时决策成为可能'
        ]
      },
      {
        title: '大数据的三大特征（3V）',
        description: '',
        children: []
      },
      {
        title: 'Volume（海量）：数据规模爆炸式增长',
        description: '',
        children: []
      },
      {
        title: 'Velocity（高速）：数据生成与处理速度极快',
        description: '',
        children: []
      },
      {
        title: 'Variety（多样）：结构化、半结构化与非结构化数据共存',
        description: '',
        children: []
      },
      {
        title: '大数据技术架构核心',
        description: '',
        children: []
      },
      {
        title: 'Hadoop生态系统：分布式存储（HDFS）与计算（MapReduce）',
        description: '',
        children: []
      },
      {
        title: 'NoSQL数据库：灵活存储非结构化数据，如HBase',
        description: '',
        children: []
      },
      {
        title: 'Spark计算框架：内存计算引擎',
        description: '',
        children: [
          '比MapReduce快100倍',
          '支持SQL、流处理、机器学习'
        ]
      },
      {
        title: 'Flink实时计算：事件驱动的流处理',
        description: '',
        children: [
          'Exactly-once语义',
          '低延迟高吞吐'
        ]
      },
      {
        title: '数据湖架构：统一数据存储',
        description: '',
        children: [
          '支持结构化、半结构化数据',
          'ACID事务支持'
        ]
      },
      {
        title: '实时数据处理应用场景',
        description: '',
        children: [
          '实时风控',
          '实时推荐',
          '实时监控'
        ]
      },
      {
        title: '批处理应用场景',
        description: '',
        children: [
          '离线报表',
          '数据仓库ETL',
          '历史数据分析'
        ]
      },
      {
        title: '数据可视化工具对比',
        description: '',
        children: [
          'Tableau',
          'Power BI',
          'ECharts'
        ]
      },
      {
        title: '机器学习在大数据中的应用',
        description: '',
        children: [
          '用户画像',
          '异常检测',
          '预测分析'
        ]
      },
      {
        title: '数据治理框架',
        description: '',
        children: [
          '元数据管理',
          '数据血缘',
          '数据质量'
        ]
      },
      {
        title: '云原生大数据平台',
        description: '',
        children: [
          '弹性伸缩',
          '容器化部署',
          'Serverless架构'
        ]
      },
      {
        title: '大数据安全与隐私保护',
        description: '',
        children: [
          '数据加密',
          '访问控制',
          '差分隐私'
        ]
      },
      {
        title: '大数据项目实践',
        description: '',
        children: [
          '电商数据分析平台',
          '用户行为分析',
          '实时推荐系统'
        ]
      },
      {
        title: '大数据未来趋势',
        description: '',
        children: [
          'AI与大数据融合',
          '实时智能决策',
          '数据网格架构'
        ]
      }
    ]
    return pptTemplates.slice(0, Math.min(count, pptTemplates.length))
  }
}

// 监听卡片数量变化
watch(cardCount, () => {
  if (showOutline.value && activeBlock.value !== null) {
    outlineItems.value = generateOutlineByCount(cardCount.value, activeBlock.value)
  }
})

// 监听类型变化
watch(activeBlock, () => {
  if (showOutline.value && activeBlock.value !== null) {
    outlineItems.value = generateOutlineByCount(cardCount.value, activeBlock.value)
  }
})

// 全局点击事件处理
const handleGlobalClick = (e: MouseEvent) => {
  const target = e.target as HTMLElement
  
  // 关闭左键菜单
  const contextMenu = document.querySelector('.context-menu')
  if (contextMenu && !contextMenu.contains(target)) {
    closeContextMenu()
  }
  
  // 取消编辑状态 - 点击任何非编辑区域
  const isClickOnChildInput = target.closest('.edit-child-input')
  const isClickOnChildText = target.closest('.child-text')
  const isClickOnDeleteBtn = target.closest('.delete-child-btn')
  const isClickOnContextMenu = target.closest('.context-menu')
  const isClickOnItemNumber = target.closest('.item-number')
  
  // 如果不是点击在编辑输入框、子项文本、删除按钮、菜单或数字上，就取消编辑
  if (!isClickOnChildInput && !isClickOnChildText && !isClickOnDeleteBtn && 
      !isClickOnContextMenu && !isClickOnItemNumber) {
    if (editingChildIndex.value !== null) {
      saveChildEdit()
    }
  }
}

onMounted(() => {
  activeBlock.value = 1
  
  // 从路由参数获取初始值
  if (route.query.text) {
    inputValue.value = route.query.text as string;
  } else if (route.query.template) {
    inputValue.value = `使用模板：${route.query.template}。请帮我生成...`;
  }

  // 自动切换文档/PPT方块高亮
  if (route.query.type === 'document') {
    activeBlock.value = 2;
  } else {
    activeBlock.value = 1;
  }
  
  // 添加全局点击事件监听
  document.addEventListener('click', handleGlobalClick)
  
  // 关闭所有下拉菜单
  document.addEventListener('click', () => {
    Object.keys(dropdownOpen.value).forEach(key => {
      dropdownOpen.value[key as keyof typeof dropdownOpen.value] = false
    })
  })
})

onUnmounted(() => {
  // 移除全局点击事件监听
  document.removeEventListener('click', handleGlobalClick)
})

// 监听showOutline变化，控制页面是否可滚动
watch(showOutline, (newVal) => {
  const container = document.querySelector('.gradient-container')
  if (container) {
    if (newVal) {
      (container as HTMLElement).style.overflowY = 'auto'
    } else {
      (container as HTMLElement).style.overflowY = 'hidden'
    }
  }
})

const handleBack = () => {
  router.back()
}

const handleBlockClick = (index: number) => {
  activeBlock.value = index
}

const toggleDropdown = (menu: string) => {
  Object.keys(dropdownOpen.value).forEach(key => {
    if (key !== menu) {
      dropdownOpen.value[key as keyof typeof dropdownOpen.value] = false
    }
  })
  dropdownOpen.value[menu as keyof typeof dropdownOpen.value] = !dropdownOpen.value[menu as keyof typeof dropdownOpen.value]
}

const selectCardCount = (count: number) => {
  cardCount.value = count
  dropdownOpen.value.cardCount = false
}

const selectLanguage = (language: string) => {
  selectedLanguage.value = language
  dropdownOpen.value.language = false
}

const handleExampleClick = (example: string) => {
  inputValue.value = example
}

// 发送按钮 - 生成大纲
const handleSend = async () => {
  if (!inputValue.value.trim()) {
    console.log('发送内容为空，不执行');
    return;
  }

  if (activeBlock.value === null) {
    alert("请先选择要生成的内容类型（演示文稿/文档）！");
    return;
  }

  isLoading.value = true

  try {
    // 调用后端API生成大纲
    const response = await axios.post(`${API_BASE_URL}/generate-outline`, {
      prompt: inputValue.value,
      type: activeBlock.value === 1 ? 'presentation' : 'document',
      cardCount: cardCount.value,
      language: selectedLanguage.value
    })

    const responseData = response.data as any

    if (responseData && responseData.outline) {
      // 使用后端返回的数据
      outlineItems.value = responseData.outline
    } else {
      // 如果API返回空，使用前端生成
      outlineItems.value = generateOutlineByCount(cardCount.value, activeBlock.value)
    }

    // 设置主标题和副标题
    mainTitle.value = outlineTitle.value
    subtitle.value = outlineSubtitle.value
    
    showOutline.value = true
  } catch (error) {
    console.error('生成大纲失败:', error)
    // 如果API调用失败，使用前端生成
    outlineItems.value = generateOutlineByCount(cardCount.value, activeBlock.value)
    mainTitle.value = outlineTitle.value
    subtitle.value = outlineSubtitle.value
    showOutline.value = true
  } finally {
    isLoading.value = false
  }
}

// 获取条目颜色
const getItemColor = (index: number) => {
  return itemColors[index % itemColors.length]
}

// 点击数字处理 - 显示圆形阴影并打开菜单
const handleNumberClick = (event: MouseEvent, index: number) => {
  // 如果正在编辑任何内容，先保存并取消
  if (editingChildIndex.value !== null) {
    saveChildEdit()
  }
  
  event.preventDefault()
  event.stopPropagation()
  
  // 触发圆形阴影动画
  activeNumber.value = index
  
  // 关闭已打开的菜单
  closeContextMenu()
  
  // 获取点击位置相对于白色底框的坐标
  if (whiteBoxRef.value) {
    const rect = whiteBoxRef.value.getBoundingClientRect()
    const scrollTop = whiteBoxRef.value.scrollTop || 0
    const scrollLeft = whiteBoxRef.value.scrollLeft || 0
    
    // 计算相对于白色底框的位置
    contextMenuX.value = event.clientX - rect.left + scrollLeft
    contextMenuY.value = event.clientY - rect.top + scrollTop
    
    contextMenuItemIndex.value = index
    contextMenuChildIndex.value = null
    
    // 使用 nextTick 确保在下一帧显示菜单
    nextTick(() => {
      showContextMenu.value = true
    })
  }
}

// 点击子项文字处理 - 打开编辑
const handleChildLeftClick = (event: MouseEvent, itemIndex: number, childIndex: number, childText: string) => {
  event.preventDefault()
  event.stopPropagation()
  
  // 直接进入编辑模式
  startChildEdit(itemIndex, childIndex, childText)
}

// 子项编辑相关
const startChildEdit = (itemIndex: number, childIndex: number, childText: string | undefined) => {
  // 关闭可能打开的菜单
  closeContextMenu()
  
  // 先取消任何现有的编辑
  if (editingChildIndex.value !== null) {
    cancelChildEdit()
  }
  
  editingChildIndex.value = { itemIndex, childIndex }
  editChildText.value = childText || ''
  nextTick(() => {
    if (childInput.value) {
      childInput.value.focus()
    }
  })
}

const saveChildEdit = () => {
  if (editingChildIndex.value) {
    const { itemIndex, childIndex } = editingChildIndex.value
    const item = outlineItems.value[itemIndex]
    if (item && item.children[childIndex] !== undefined) {
      // 如果内容为空，删除该子项
      if (!editChildText.value.trim()) {
        deleteChildItem(itemIndex, childIndex)
      } else {
        item.children[childIndex] = editChildText.value.trim()
      }
    }
  }
  cancelChildEdit()
}

const cancelChildEdit = () => {
  editingChildIndex.value = null
  editChildText.value = ''
}

// 删除子项
const deleteChildItem = (itemIndex: number, childIndex: number) => {
  const item = outlineItems.value[itemIndex]
  if (item && item.children.length > 0) {
    item.children.splice(childIndex, 1)
  }
}

const closeContextMenu = () => {
  showContextMenu.value = false
  contextMenuItemIndex.value = null
  contextMenuChildIndex.value = null
}

// 添加要点
const addBulletPoint = () => {
  if (contextMenuItemIndex.value !== null) {
    const item = outlineItems.value[contextMenuItemIndex.value]
    if (item) {
      if (!item.children) {
        item.children = []
      }
      item.children.push('新要点')
    }
  }
  closeContextMenu()
}

// 批量添加多个要点
const addMultipleBulletPoints = () => {
  if (contextMenuItemIndex.value !== null) {
    const item = outlineItems.value[contextMenuItemIndex.value]
    if (item) {
      if (!item.children) {
        item.children = []
      }
      // 添加3个新要点
      item.children.push('要点 1', '要点 2', '要点 3')
    }
  }
  closeContextMenu()
}

// 在上方插入卡片
const insertCardAbove = () => {
  if (contextMenuItemIndex.value !== null) {
    const newCard: OutlineItem = {
      title: '新卡片',
      description: '',
      children: []
    }
    outlineItems.value.splice(contextMenuItemIndex.value, 0, newCard)
  }
  closeContextMenu()
}

// 在下方插入卡片
const insertCardBelow = () => {
  if (contextMenuItemIndex.value !== null) {
    const newCard: OutlineItem = {
      title: '新卡片',
      description: '',
      children: []
    }
    outlineItems.value.splice(contextMenuItemIndex.value + 1, 0, newCard)
  }
  closeContextMenu()
}

// 删除卡片
const deleteCard = () => {
  if (contextMenuItemIndex.value !== null) {
    outlineItems.value.splice(contextMenuItemIndex.value, 1)
  }
  closeContextMenu()
}

// 添加卡片
const handleAddCard = async () => {
  if (isAddingCard.value) return
  
  isAddingCard.value = true
  
  try {
    const response = await axios.post(`${API_BASE_URL}/generate-card`, {
      type: activeBlock.value === 1 ? 'presentation' : 'document',
      previousCards: outlineItems.value,
      context: inputValue.value
    })

    const responseData = response.data as any

    if (responseData && responseData.card) {
      outlineItems.value.push(responseData.card)
    } else {
      outlineItems.value.push({
        title: activeBlock.value === 1 ? '新卡片' : '新章节',
        description: '',
        children: []
      })
    }
  } catch (error) {
    console.error('添加卡片失败:', error)
    outlineItems.value.push({
      title: activeBlock.value === 1 ? '新卡片' : '新章节',
      description: '',
      children: []
    })
  } finally {
    isAddingCard.value = false
  }
}

const handleRefreshExample = () => {
  const exampleGroups: string[][] = [
    ["我从100多位首席执行官身上学到的时间管理秘诀", "为失去动力的创作者提供3个建议", "给'过于和蔼可亲'的教师的课堂管理建议", "从0到1000个订阅者：我希望拥有的路线图", "每个人都在做却没人在会议上承认的事", "职场沟通的高效表达技巧"],
    ["如何打造高转化的内容矩阵", "团队协作中的冲突解决策略", "远程办公的效率提升方法", "职场新人的快速成长指南", "管理者的激励员工技巧", "职业规划的5年规划法"],
    ["人工智能在办公中的应用", "机器学习入门指南", "深度学习框架对比", "自然语言处理基础", "计算机视觉应用", "强化学习实战"]
  ]
  
  const randomIndex = Math.floor(Math.random() * exampleGroups.length)
  exampleList.value = exampleGroups[randomIndex] || exampleGroups[0] || []
}

const handleHelp = () => {
  alert('点击数字打开操作菜单，可添加要点、批量添加要点、插入卡片、删除卡片；点击子项可直接编辑，点击其他地方自动保存')
}

const handleFinalGenerate = () => {
  console.log('生成最终内容', {
    mainTitle: mainTitle.value,
    subtitle: subtitle.value,
    items: outlineItems.value
  })
  if (activeBlock.value === 1) {
    router.push({
      path: '/editor',
      query: {
        outline: JSON.stringify({
          title: mainTitle.value,
          subtitle: subtitle.value,
          items: outlineItems.value
        }),
        type: 'presentation'
      }
    })
  } else {
    router.push({
      path: '/editor/doc',
      query: {
        outline: JSON.stringify({
          title: mainTitle.value,
          subtitle: subtitle.value,
          items: outlineItems.value
        }),
        type: 'document'
      }
    })
  }
}
</script>

<style scoped>
/* 全局样式重置 - 完全按照 AICourseGenerate 的模式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* 渐变背景容器 - 完全按照 AICourseGenerate 的模式 */
.gradient-container {
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
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 有内容时允许滚动 */
.gradient-container.has-outline {
  overflow-y: auto;
}

.button-group {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
}

.back-button {
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
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: scale(1.05);
}

/* 页面标题样式 - 按照 AICourseGenerate 的模式 */
.page-title {
  text-align: center;
  padding-top: 80px;
  margin-bottom: 30px;
}

.page-title h1 {
  font-size: 48px;
  color: #2c3e50;
  font-weight: 700;
  margin-bottom: 8px;
}

.page-title p {
  font-size: 18px;
  color: #34495e;
}

.block-container {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.white-block {
  width: 180px;
  height: 100px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.white-block.active {
  border: 2px solid rgb(11, 167, 175);
  background-color: #f0f8ff;
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.2);
}

.icon-wrapper {
  margin-top: -10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.block-icon {
  font-size: 40px;
  color: #71cdd1;
}

.white-block.active .block-icon {
  color: #4ad0e2;
}

.block-text {
  margin-top: 5px;
  font-size: 14px;
  color: #34495e;
}

.white-block.active .block-text {
  color: #4ad0e2;
}

.select-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  position: relative;
  z-index: 100;
}

.select-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  color: #34495e;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
}

.select-item:hover {
  background: #f8f9fa;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.select-arrow {
  transition: transform 0.3s ease;
  font-size: 12px;
}

.select-arrow.rotated {
  transform: rotate(180deg);
}

.select-icon {
  color: #34495e;
  font-size: 16px;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  min-width: 120px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  overflow: hidden;
  z-index: 1000;
  animation: dropdownFade 0.2s ease;
}

@keyframes dropdownFade {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  padding: 10px 16px;
  font-size: 14px;
  color: #34495e;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.dropdown-item:hover {
  background: #f0f8ff;
  color: rgb(11, 167, 175);
}

.input-container {
  width: 60%;
  max-width: 800px;
  margin-bottom: 30px;
  position: relative;
  display: flex;
  align-items: center;
}

.main-input {
  width: 100%;
  padding: 16px 50px 16px 20px;
  border-radius: 30px;
  border: none;
  font-size: 16px;
  color: #34495e;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  outline: none;
  transition: all 0.2s ease;
}

.main-input:focus {
  box-shadow: 0 4px 12px rgba(11, 167, 175, 0.2);
}

.main-input::placeholder {
  color: #999;
}

.send-button {
  position: absolute;
  right: 8px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgb(11, 167, 175);
  border: none;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.send-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.send-button:hover:not(:disabled) {
  background: rgb(8, 130, 136);
  transform: scale(1.05);
}

.send-button:active:not(:disabled) {
  transform: scale(0.95);
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #ffffff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 大纲区域样式 */
.outline-section {
  width: 60%;
  max-width: 800px;
  margin-top: 20px;
  margin-bottom: 40px;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 白色底框 - 作为定位参考 */
.outline-white-box {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 24px;
  margin-bottom: 20px;
  width: 100%;
  box-sizing: border-box;
  position: relative;
}

.outline-header {
  margin-bottom: 24px;
  padding-left: 8px;
}

.outline-main-title {
  font-size: 24px;
  color: #2c3e50;
  margin-bottom: 4px;
  font-weight: 600;
}

.outline-main-subtitle {
  font-size: 16px;
  color: #34495e;
  font-weight: 500;
  display: inline-block;
}

.outline-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.outline-item-wrapper {
  position: relative;
  margin-bottom: 4px;
}

.outline-item {
  padding: 16px;
  border-radius: 12px;
  transition: all 0.2s ease;
  display: flex;
  gap: 16px;
  width: 100%;
  box-sizing: border-box;
}

.outline-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.item-number {
  font-size: 18px;
  font-weight: 600;
  color: #34495e;
  min-width: 30px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 50%;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
}

.item-number.clickable:hover {
  background-color: rgba(11, 167, 175, 0.1);
}

/* 圆形阴影动画 */
.item-number.ripple-active {
  animation: numberRipple 0.3s ease-out;
}

@keyframes numberRipple {
  0% {
    box-shadow: 0 0 0 0 rgba(11, 167, 175, 0.7);
    background-color: rgba(11, 167, 175, 0.2);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(11, 167, 175, 0);
    background-color: rgba(11, 167, 175, 0.1);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(11, 167, 175, 0);
    background-color: transparent;
  }
}

.item-content {
  flex: 1;
}

.item-title {
  font-size: 16px;
  color: #2c3e50;
  font-weight: 500;
  margin-bottom: 8px;
  line-height: 1.5;
}

.item-description {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  line-height: 1.5;
}

.item-children {
  list-style: none;
  padding: 0;
  margin: 8px 0 0 0;
}

.child-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 4px;
  line-height: 1.5;
  position: relative;
}

.child-item:hover .delete-child-btn {
  opacity: 1;
}

.bullet {
  color: #999;
  font-size: 14px;
  min-width: 8px;
}

.child-text {
  font-size: 14px;
  color: #666;
  cursor: pointer;
  padding: 2px 4px;
  margin: -2px -4px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
  flex: 1;
}

.child-text:hover {
  background-color: rgba(11, 167, 175, 0.1);
}

.delete-child-btn {
  opacity: 0;
  background: none;
  border: none;
  color: #ff6b6b;
  cursor: pointer;
  font-size: 14px;
  padding: 2px 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-child-btn:hover {
  background-color: rgba(255, 107, 107, 0.1);
  transform: scale(1.1);
}

.edit-child-input {
  width: 100%;
  padding: 4px 8px;
  border: 2px solid rgb(11, 167, 175);
  border-radius: 8px;
  font-size: 14px;
  color: #2c3e50;
  background: white;
  outline: none;
  font-family: inherit;
  flex: 1;
}

.edit-child-input:focus {
  box-shadow: 0 0 0 3px rgba(11, 167, 175, 0.2);
}

.add-card-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 16px;
  padding-top: 8px;
  border-top: 1px dashed #ddd;
}

.add-card-btn {
  background: none;
  border: none;
  padding: 8px 24px;
  font-size: 14px;
  color: #34495e;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  border-radius: 20px;
}

.add-card-btn:hover:not(:disabled) {
  background: #f5f5f5;
  color: rgb(11, 167, 175);
}

.add-card-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 左键菜单样式 - 使用绝对定位，相对于白色底框 */
.context-menu {
  position: absolute;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  padding: 8px 0;
  z-index: 1000;
  min-width: 180px;
  animation: menuFade 0.2s ease;
  border: 1px solid rgba(0,0,0,0.05);
}

@keyframes menuFade {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.context-menu-item {
  padding: 10px 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #34495e;
  transition: all 0.2s ease;
}

.context-menu-item:hover {
  background: rgba(11, 167, 175, 0.1);
  color: rgb(11, 167, 175);
}

.context-menu-item.delete:hover {
  background: rgba(255, 107, 107, 0.1);
  color: #ff6b6b;
}

.context-menu-item .iconfont {
  font-size: 16px;
  color: #71cdd1;
}

.context-menu-item:hover .iconfont {
  color: rgb(11, 167, 175);
}

.context-menu-item.delete:hover .iconfont {
  color: #ff6b6b;
}

.context-menu-divider {
  height: 1px;
  background: rgba(0,0,0,0.05);
  margin: 8px 0;
}

/* 底部操作栏 - 新样式 */
.outline-footer {
  background: white;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  width: 100%;
  box-sizing: border-box;
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.footer-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-label {
  font-size: 12px;
  color: #999;
}

/* 四个方块按钮样式 */
.style-blocks {
  display: flex;
  gap: 8px;
}

.style-block {
  width: 60px;
  height: 60px;
  background: #f5f5f5;
  border: 2px solid transparent;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.style-block.active {
  background: rgb(11, 167, 175);
  color: white;
  border-color: rgb(8, 130, 136);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(11, 167, 175, 0.3);
}

.style-block:hover:not(.active) {
  background: #e0e0e0;
  transform: translateY(-1px);
}

.footer-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.total-cards {
  font-size: 14px;
  color: #34495e;
  white-space: nowrap;
}

.generate-btn {
  background: rgb(11, 167, 175);
  color: white;
  border: none;
  padding: 8px 24px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.generate-btn:hover {
  background: rgb(8, 130, 136);
  transform: scale(1.02);
}

/* 示例提示区域 */
.example-section {
  width: 60%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.example-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
  position: relative;
  width: 100%;
  text-align: center;
}

.example-title::before,
.example-title::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40%;
  height: 1px;
  background: #ddd;
}

.example-title::before {
  left: 0;
}

.example-title::after {
  right: 0;
}

.example-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
  width: 100%;
}

.example-card {
  background: rgba(255,255,255,0.8);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  min-height: 80px;
  box-sizing: border-box;
}

.example-card:hover {
  background: rgba(255,255,255,1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.example-content {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 14px;
  color: #34495e;
  line-height: 1.5;
  flex: 1;
  min-width: 0;
  word-wrap: break-word;
  word-break: break-word;
}

.example-icon {
  color: #34495e;
  flex-shrink: 0;
  font-size: 16px;
  margin-top: 2px;
}

.example-text {
  white-space: normal;
  line-height: 1.5;
}

.example-add {
  font-size: 18px;
  color: #666;
  font-weight: bold;
  flex-shrink: 0;
  margin-left: 8px;
  width: 20px;
  text-align: center;
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  padding: 8px 16px;
  border-radius: 20px;
  border: none;
  font-size: 14px;
  color: #34495e;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
}

.refresh-button:hover {
  background: #f8f9fa;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.refresh-icon {
  color: #34495e;
  font-size: 14px;
}

/* 帮助按钮 */
.help-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #34495e;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
  z-index: 1000;
}

.help-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>