import api from './index'

/**
 * 获取可用模型列表
 */
export async function getModels() {
  const response = await api.get('/models/')
  return response
}

/**
 * 切换模型
 */
export async function switchModel(modelName) {
  const response = await api.post(`/models/switch?model_name=${modelName}`)
  return response
}

/**
 * 获取模型状态
 */
export async function getModelStatus() {
  const response = await api.get('/models/status')
  return response
}

/**
 * 加载模型
 */
export async function loadModel(modelName) {
  const response = await api.post(`/models/load?model_name=${modelName}`)
  return response
}

/**
 * 卸载模型
 */
export async function unloadModel(modelName) {
  const response = await api.post(`/models/unload?model_name=${modelName}`)
  return response
}
