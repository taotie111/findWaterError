import api from './index'

/**
 * 单张图像检测
 */
export async function detectImage(file, modelName = null) {
  const formData = new FormData()
  formData.append('image', file)
  if (modelName) {
    formData.append('model_name', modelName)
  }
  
  const response = await api.post('/detect/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response
}

/**
 * 批量图像检测
 */
export async function detectBatch(files, modelName = null) {
  const formData = new FormData()
  files.forEach(file => {
    formData.append('images', file)
  })
  if (modelName) {
    formData.append('model_name', modelName)
  }
  
  const response = await api.post('/detect/batch', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response
}

/**
 * 获取检测结果
 */
export async function getDetectionResult(recordId) {
  const response = await api.get(`/detect/${recordId}`)
  return response
}
