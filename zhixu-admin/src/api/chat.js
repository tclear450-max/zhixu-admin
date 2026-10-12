import request from '../utils/request'
import { createSseParser } from '../utils/sseParser'

const url = '/chat'

export const chat = (data) => {
  return request({
    url: url + '/chat',
    method: 'post',
    data
  })
}

/**
 * SSE 流式聊天——使用 fetch + ReadableStream 手动解析 SSE 事件流
 *
 * 为什么用 fetch 而不是 EventSource？
 * - 聊天接口是 POST 请求，需要携带 JSON 请求体（对话内容、会话 ID 等）
 * - 浏览器原生 EventSource 只支持 GET，无法发送请求体
 * - 同时需要携带 httpOnly Cookie 做身份认证（credentials: 'include'）
 *
 * @param {Object} data - 请求体，包含 sessionId（兼容 conversationId）和 message
 * @param {Function} onToken - 收到 token 事件时回调，参数为单字符或短文本片段
 * @param {Function} onMeta - 收到 meta 事件时回调，参数为解析后的 JSON 对象（含 conversationId）
 * @param {Function} onError - 请求失败或网络异常时回调
 * @returns {Promise} fetch 链式调用的 Promise
 */
export const chatStream = async (data, onToken, onMeta, onError, onCitations) => {
  try {
    const response = await fetch('/api/chat/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
      credentials: 'include'
    })
    if (!response.ok) throw new Error('HTTP ' + response.status)
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let completed = false
    const parse = createSseParser((event, payload) => {
      if (event === 'token') {
        let token
        try { token = JSON.parse(payload) } catch (error) { token = payload }
        onToken(token)
      } else if (event === 'citations' && onCitations) onCitations(JSON.parse(payload))
      else if (event === 'meta') { completed = true; onMeta(JSON.parse(payload)) } else if (event === 'error') throw new Error(payload)
    })
    while (true) {
      const { done, value } = await reader.read()
      if (done) { parse(decoder.decode(), true); break }
      parse(decoder.decode(value, { stream: true }))
    }
    if (!completed) throw new Error('回答连接中断，请重试')
  } catch (error) { if (onError) onError(error) }
}

export const listConversations = () => {
  return request({
    url: url + '/conversations',
    method: 'get'
  })
}

export const queryConversation = (id) => {
  return request({
    url: url + '/conversations/' + id,
    method: 'get'
  })
}

export const queryMessages = (id, params) => {
  return request({
    url: url + '/conversations/' + id + '/messages',
    method: 'get',
    params
  })
}

export const deleteConversation = (id) => {
  return request({
    url: url + '/conversations/' + id,
    method: 'delete'
  })
}
