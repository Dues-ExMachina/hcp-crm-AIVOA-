import apiClient from './apiClient'

export const sendChatMessage = ({ message, repId = 1, chatHistory = [] }) =>
  apiClient.post('/chat/message', {
    message,
    rep_id: repId,
    chat_history: chatHistory,
  })
