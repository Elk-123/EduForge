// src/api/ppt.js
import axios from 'axios'

const api = axios.create({
  baseURL: '/api', // 后端接口前缀
  timeout: 5000
})

// 获取所有幻灯片
export const fetchSlides = async (pptId = null) => {
  if (pptId) {
    // 获取指定PPT
    return Promise.resolve({
      id: pptId,
      title: '加载的PPT',
      slides: [
        {
          id: 1,
          title: '首页',
          content: 'PPT 实时编辑器',
          bgColor: '#ffffff',
          steps: [
            { id: 1, title: '第一步', desc: '开始编辑' }
          ]
        }
      ]
    })
  }
  // 临时 mock 数据
  return Promise.resolve([
    {
      id: 1,
      title: '首页',
      content: '点击编辑标题和内容',
      bgColor: '#ffffff',
      image: null,
      steps: [
        { id: 1, title: '第一步', desc: '这是第一步的描述' },
        { id: 2, title: '第二步', desc: '这是第二步的描述' }
      ]
    },
    {
      id: 2,
      title: '第二页',
      content: '可以添加更多内容',
      bgColor: '#f8f9fa',
      image: null,
      steps: []
    }
  ])
}

// 新增幻灯片
export const createSlide = async (data) => {
  return Promise.resolve({
    id: Date.now(),
    ...data
  })
}

// 更新幻灯片
export const updateSlide = async (id, data) => {
  // 实时保存到后端
  console.log('保存幻灯片:', id, data)
  return Promise.resolve({ id, ...data })
}

// 更新步骤
export const updateStep = async (id, data) => {
  console.log('保存步骤:', id, data)
  return Promise.resolve({ id, ...data })
}