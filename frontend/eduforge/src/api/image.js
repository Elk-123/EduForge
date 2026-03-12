// src/api/image.js
import axios from 'axios'

const api = axios.create({
  baseURL: '/api', // 后端接口前缀
  timeout: 10000
})

// 搜索图片
export const searchImages = async (keyword, page = 1, limit = 20) => {
  try {
    const response = await api.get('/images/search', {
      params: { keyword, page, limit }
    })
    return response.data
  } catch (error) {
    console.error('搜索图片失败:', error)
    throw error
  }
}

// 获取推荐图片
export const getRecommendedImages = async (slideId, limit = 8) => {
  try {
    const response = await api.get('/images/recommended', {
      params: { slideId, limit }
    })
    return response.data
  } catch (error) {
    console.error('获取推荐图片失败:', error)
    throw error
  }
}

// 上传图片
export const uploadImage = async (file) => {
  const formData = new FormData()
  formData.append('image', file)
  
  try {
    const response = await api.post('/images/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  } catch (error) {
    console.error('上传图片失败:', error)
    throw error
  }
}

// 获取图片详情
export const getImageDetail = async (imageId) => {
  try {
    const response = await api.get(`/images/${imageId}`)
    return response.data
  } catch (error) {
    console.error('获取图片详情失败:', error)
    throw error
  }
}