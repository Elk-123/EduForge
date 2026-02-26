<template>
  <div class="course-generate-page">
    <!-- 1. 顶栏（页面最顶部，独立于侧边栏/主内容区） -->
    <div class="top-nav">
      <!-- 顶栏左侧：logo+标题 -->
      <div class="top-nav-left">
        <span class="top-title">智构古韵</span>
      </div>
      <!-- 顶栏右侧：操作按钮+用户信息（替代原top-bar） -->
      <div class="top-nav-right">
        <button class="nav-btn">帮助中心</button>
        <button class="nav-btn">设置</button>
        <img src="/icons/user-icon.png" alt="个人中心" class="user-icon" />
      </div>
    </div>

    <!-- 2. 侧边栏（顶栏下方左侧，宽度250px） -->
    <div class="sidebar">
      <div>
        <ul class="sidebar-nav">
          <li>
            <img src="/icons/home-icon.png" alt="首页" class="nav-icon" />
            首页
          </li>
          <li class="active" @click="goToChatPage">AI课件生成</li>
          <li>AI教学助手</li>
          <li>多模态识别</li>
          <li>知识库</li>
        </ul>
      </div>
      <div class="sidebar-footer">个人中心</div>
    </div>

    <!-- 3. 主内容区（顶栏下方右侧，适配250px侧边栏） -->
    <div class="main-content">
      <!-- 搜索栏（位置微调，避开顶栏） -->
      <div class="search-bar">
        <input
          type="text"
          placeholder="请输入教学课题，例如：斗拱结构，唐代建筑特点"
        />
        <button class="generate-btn">一键生成</button>
      </div>

      <!-- 功能卡片（适配250px侧边栏的居中） -->
      <div class="function-cards">
        <div class="card" v-for="(item, index) in cardList" :key="index">
          <h3>{{ item.title }}</h3>
          <p>{{ item.desc }}</p>
        </div>
      </div>

      <!-- 我的课件（适配250px侧边栏的左侧距离 + 滚动列表） -->
      <div class="my-courses">
        <!-- 我的课件头部：标题 + 搜索框 -->
        <div class="my-courses-header">
          <h2>我的课件</h2>
          <div class="course-search">
            <input type="text" placeholder="搜索我的课件" />
            <!-- 替换成你的图标：src改你自己的图标路径 -->
            <button class="search-btn">
              <img src="/icons/search.png" alt="搜索" class="search-icon" />
            </button>
          </div>
        </div>
        <!-- 👇 新增：一排4个PPT模板预览区 -->
        <div class="ppt-templates">
          <div class="template-item" v-for="(item, idx) in templateList" :key="idx">
            <div class="template-cover">
              <img :src="item.cover" alt="PPT封面" />
            </div>
            <div class="template-title">{{ item.title }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

import { useRouter } from 'vue-router'

// 初始化路由实例
const router = useRouter()

// 新增：跳转至ChatPage的函数
const goToChatPage = () => {
  // 跳转到/chat路径（对应ChatPage.vue）
  router.push('/chat')
}

const cardList = [
  { title: "导入文档生成PPT", desc: "支持多种格式，秒变PPT" },
  { title: "课件智能优化", desc: "润色内容，适配教学场景" },
  { title: "古建案例模板库", desc: "精选古建案例，一键复用" },
  { title: "课件素材库", desc: "海量素材，随心搭配" },
  { title: "更多功能", desc: "持续更新，满足需求" },
];

// 模拟我的课件列表（可替换成真实数据）
const courseList = [
  { title: "唐代建筑特点PPT" },
  { title: "斗拱结构教学课件" },
  { title: "故宫角楼结构拆解" },
  { title: "宋代木构建筑解析" },
  { title: "明清宫殿建筑特点" },
  { title: "徽派建筑马头墙设计" },
  { title: "山西古建斗拱工艺" },
  { title: "江南园林建筑布局" },
  { title: "长城建筑材料分析" },
  { title: "敦煌石窟建筑特色" },
];

// 模拟PPT模板数据（可替换成真实封面图）
const templateList = [
  { title: "唐代建筑特点PPT", cover: "/images/template1.png" },
  { title: "斗拱结构教学课件", cover: "/images/template2.png" },
  { title: "故宫角楼结构拆解", cover: "/images/template3.png" },
  { title: "宋代木构建筑解析", cover: "/images/template4.png" },
];
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Microsoft YaHei", sans-serif;
}

/* 页面容器：给顶栏留空间，整体flex布局 */
.course-generate-page {
  display: flex;
  height: 100vh;
  background-color: #f5f5f5;
  padding-top: 60px; /* 顶栏高度，避免内容被遮挡 */
  position: relative;
}

/* 顶栏样式（核心新增） */
.top-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background-color: #ffffff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  z-index: 999; /* 顶栏在最上层 */
}

.top-nav-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 36px;
  height: 36px;
}

.top-title {
  font-size: 24px;
  color: #333;
  font-weight: 600;
  font-family: "Microsoft YaHei", sans-serif;
}

.top-nav-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.nav-btn {
  padding: 6px 12px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 4px;
  color: #666;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.nav-btn:hover {
  background-color: #e0e0e0;
}

/* 侧边栏样式（适配250px宽度+顶栏 + 统一菜单样式） */
.sidebar {
  width: 250px; /* 你设置的宽度 */
  background-color: #ffffff;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px 0;
  position: fixed; /* 固定侧边栏，和顶栏对齐 */
  top: 60px; /* 顶栏高度，避开顶栏 */
  left: 0;
  bottom: 0;
  z-index: 1;
}

.sidebar-header {
  text-align: center;
  margin-bottom: 30px;
}

.sidebar-header h1 {
  font-size: 20px;
  color: #333;
  font-weight: 600;
}

.sidebar-nav {
  list-style: none;
}

/* 核心修改：左侧菜单样式和第二张图统一 */
.sidebar-nav li {
  padding: 10px 15px;
  margin: 4px 10px;
  border-radius: 6px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px; /* 和第二张图菜单字体大小一致 */
}

.nav-icon {
  width: 16px;
  height: 16px;
}

/* 核心修改：选中效果和第二张图一致 */
.sidebar-nav li.active {
  background-color: rgba(176, 106, 90, 0.2);
  color: rgba(176, 106, 90, 1);
  font-weight: 500;
}

.sidebar-nav li:hover {
  background-color: #f0f0f0;
}

.sidebar-footer {
  text-align: left;        /* 左对齐 */
  color: #666;
  padding: 0 20px;         /* 上下内边距去掉 */
  margin-top: -10px;       /* 往上一点（数字越大越上，比如 -15px） */
  cursor: pointer;
}

/* 主内容区样式（适配250px侧边栏+顶栏） */
.main-content {
  flex: 1;
  background-color: #B06A5A; /* 你设置的背景色 */
  background-image: url("/images/bg.png");
  background-size: 50% auto;
  background-position:  0px 0px;;
  background-repeat: no-repeat;
  background-blend-mode: multiply;
  opacity: 0.9;
  position: fixed; /* 固定主内容区，和侧边栏对齐 */
  top: 60px; /* 顶栏高度 */
  left: 250px; /* 侧边栏宽度，避开侧边栏 */
  right: 0;
  bottom: 0;
  overflow: hidden;
}

/* 用户图标（移到顶栏，尺寸保留你设置的38px） */
.user-icon {
  width: 38px; /* 你设置的尺寸 */
  height: 38px;
  cursor: pointer;
  border-radius: 0%; /* 圆形头像，更美观 */
}

/* 搜索栏（位置微调，避开顶栏） */
.search-bar {
  position: absolute;
  top: 75px; /* 从60px调整为80px，避开顶栏 */
  left: 50%;
  transform: translateX(-50%);
  width: 70%;
  display: flex;
  align-items: center;
}

.search-bar input {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 8px 0 0 8px;
  font-size: 14px;
  outline: none;
}

.generate-btn {
  padding: 12px 20px;
  background: linear-gradient(90deg, #ff7a45 0%, #c86b58 100%);
  border: none;
  border-radius: 0 8px 8px 0;
  color: #ffffff;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.generate-btn:hover {
  background: linear-gradient(90deg, #ff8a58 0%, #d87b68 100%);
}

/* 功能卡片样式（保留你设置的渐变） */
.function-cards {
  position: absolute;
  top: 180px; /* 从150px调整为180px，适配顶栏 */
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  display: grid;
  height: 100px;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}

.card {
  border-radius: 8px;
  padding: 12px 15px;
  text-align: left;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  font-size: 13px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  opacity: 0.9;
  background: linear-gradient(to bottom, #FFE6E6, #FFFFFF);
  /* 新增：让卡片内文字靠中下 */
  display: flex;
  flex-direction: column;
  justify-content: flex-end; /* 关键：文字靠下（中下） */
  height: 100%; /* 必须加，否则flex布局不生效 */
  padding-top: 0; /* 去掉顶部多余内边距，强化中下效果 */
  padding-bottom: 15px; /* 微调底部内边距，让文字更居中下 */
}

/* 👇 核心修改：卡片标题加粗 */
.card h3 {
  font-size: 13px;
  color: #333;
  margin-bottom: 5px;
  font-weight: bold; /* 加黑 */
  margin-top: 0; /* 去掉顶部margin */
}

/* 你设置的5个卡片渐变（保留） */
.card:nth-child(1) {
  background: linear-gradient(to bottom, #F5D3B8, #FFFFFF);
}
.card:nth-child(2) {
  background: linear-gradient(to bottom, #DFECF7, #FFFFFF);
}
.card:nth-child(3) {
  background: linear-gradient(to bottom, #DADAEB, #FFFFFF);
}
.card:nth-child(4) {
  background: linear-gradient(to bottom, #F3F5D3, #FFFFFF);
}
.card:nth-child(5) {
  background: linear-gradient(to bottom, #F5B8B8, #FFFFFF);
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  opacity: 1;
}

.card p {
  font-size: 11px;
  color: #666;
  line-height: 1.4;
}

/* 核心修改：我的课件区域 + 滚动列表 */
.my-courses {
  position: absolute;
  bottom: 100px; /* 调整位置，避免遮挡 */
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 200px; /* 固定高度，超出滚动 */
  display: flex;
  flex-direction: column;
}

/* 我的课件头部：标题 + 搜索框 */
.my-courses-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3); /* 白色横线 */
  margin-bottom: 10px;
}

/* 我的课件标题 - 左对齐横线 */
.my-courses h2 {
  font-size: 18px;
  color: #fff;
  margin: 0;
  white-space: nowrap;
}

/* 搜索框 - 右对齐横线（页面右侧） */
.course-search {
  display: flex;
  align-items: center; /* 新增：让输入框和按钮垂直居中 */
  background-color: #fff;
  border-radius: 8px;
  padding: 8px 15px;
  width: 200px;
  margin: 0;
  border: none;
  box-shadow: none;
  outline: none;
}

/* 可选：优化搜索框内输入框样式，更清爽 */
.course-search input {
  flex: 1; /* 新增：让输入框占满剩余空间 */
  border: none; /* 去掉输入框自带边框 */
  outline: none; /* 去掉输入框聚焦外框 */
  background: transparent; /* 输入框背景透明，和搜索框融在一起 */
  font-size: 14px; /* 统一字体大小 */
}

/* 搜索按钮：彻底去掉底纹，适配图标 */
.search-btn {
  background: transparent; /* 核心：透明背景，去掉白色底纹 */
  border: none;            /* 去掉边框 */
  outline: none;           /* 去掉聚焦外框 */
  cursor: pointer;         /* 保留鼠标手型 */
  padding: 0 5px;          /* 轻微内边距，避免图标贴边 */
  margin: 0;               /* 去掉默认边距 */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 自定义搜索图标样式 */
.search-icon {
  width: 16px;   /* 图标宽度，可自行调整 */
  height: 16px;  /* 图标高度，和宽度一致 */
  object-fit: contain; /* 保证图标不变形 */
  opacity: 0.8;  /* 轻微透明，更融入搜索框 */
  transition: opacity 0.2s; /* 过渡效果更丝滑 */
}

/* 鼠标移到图标上的效果 */
.search-btn:hover .search-icon {
  opacity: 1;    /* hover时变清晰 */
  transform: scale(1.05); /* 轻微放大，交互更友好 */
}

/* 👇 核心修改：一排4个PPT模板预览区 */
.ppt-templates {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 一排4个 */
  gap: 15px;
  margin-top: 10px;
}

.template-item {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s;
}

.template-item:hover {
  transform: translateY(-3px);
}

.template-cover {
  width: 100%;
  height: 120px;
  overflow: hidden;
}

.template-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.template-title {
  padding: 8px;
  font-size: 13px;
  color: #333;
  text-align: center;
}
</style>