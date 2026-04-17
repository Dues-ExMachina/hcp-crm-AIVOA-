import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { sendChatMessage } from '../../api/chatApi'
import { populateFromChat, setSuggestedFollowups } from './interactionSlice'

export const sendMessage = createAsyncThunk(
  'chat/sendMessage',
  async ({ message, repId = 1, chatHistory = [] }, { dispatch, rejectWithValue }) => {
    try {
      const response = await sendChatMessage({ message, repId, chatHistory })
      const data = response.data

      // If agent extracted interaction data, auto-fill the form
      if (data.extracted_fields && Object.keys(data.extracted_fields).length > 0) {
        dispatch(populateFromChat(data.extracted_fields))
      }

      // If follow-up suggestions came back, update them
      if (data.suggested_followups && data.suggested_followups.length > 0) {
        dispatch(setSuggestedFollowups(data.suggested_followups))
      }

      return data
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || err.message)
    }
  }
)

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [
      {
        id: 0,
        role: 'assistant',
        content: "Hi! I'm your AI interaction assistant. Describe your HCP visit in natural language and I'll extract and populate the form for you.\n\nTry: *\"Met Dr. Sharma today at 2pm, discussed OncoBoost Phase III, she was positive, shared the PDF brochure.\"*",
      }
    ],
    isLoading: false,
    error: null,
  },
  reducers: {
    addUserMessage: (state, action) => {
      state.messages.push({
        id: Date.now(),
        role: 'user',
        content: action.payload,
      })
    },
    clearChat: (state) => {
      state.messages = state.messages.slice(0, 1)
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (s) => {
        s.isLoading = true
        s.error = null
      })
      .addCase(sendMessage.fulfilled, (s, a) => {
        s.isLoading = false
        s.messages.push({
          id: Date.now(),
          role: 'assistant',
          content: a.payload.reply,
          toolUsed: a.payload.tool_used,
          interactionId: a.payload.interaction_id,
        })
      })
      .addCase(sendMessage.rejected, (s, a) => {
        s.isLoading = false
        s.error = a.payload
        s.messages.push({
          id: Date.now(),
          role: 'assistant',
          content: `⚠️ Error: ${a.payload || 'Could not reach the AI agent. Please check the backend is running.'}`,
        })
      })
  },
})

export const { addUserMessage, clearChat } = chatSlice.actions
export default chatSlice.reducer
