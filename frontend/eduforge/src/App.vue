<template>
  <!-- 路由出口：所有页面都会显示在这里 -->
  <router-view />
</template>

<script setup lang="ts">
// 这里什么都不用写，只留路由出口即可
</script>

<style scoped>
/* 全局基础样式，保证页面能显示 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html, body, #app {
  height: 100%;
}
</style>