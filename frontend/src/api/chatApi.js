import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

export const sendChatMessage = ({ message, repId = 1, chatHistory = [] }) =>
  api.post('/chat/message', {
    message,
    rep_id: repId,
    chat_history: chatHistory,
  })
