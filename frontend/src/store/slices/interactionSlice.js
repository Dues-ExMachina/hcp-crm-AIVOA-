import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { submitInteraction } from '../../api/interactionApi'

const initialState = {
  hcpName: '',
  hcpId: null,
  interactionType: 'Meeting',
  date: new Date().toISOString().split('T')[0],
  time: '',
  attendees: [],
  topicsDiscussed: '',
  materialsShared: [],
  samplesDistributed: [],
  sentiment: 'Neutral',
  outcomes: '',
  followUpActions: '',
  aiSuggestedFollowups: [],
  aiSummary: '',
  status: 'idle',   // idle | loading | success | error
  error: null,
  savedInteractionId: null,
}

export const saveInteraction = createAsyncThunk(
  'interaction/save',
  async (formData, { rejectWithValue }) => {
    try {
      const response = await submitInteraction(formData)
      return response.data
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || err.message)
    }
  }
)

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    updateField: (state, action) => {
      const { field, value } = action.payload
      state[field] = value
    },
    populateFromChat: (state, action) => {
      const data = action.payload
      if (data.hcp_name)            state.hcpName            = data.hcp_name
      if (data.hcp_id)              state.hcpId              = data.hcp_id
      if (data.interaction_type)    state.interactionType    = data.interaction_type
      if (data.interaction_date)    state.date               = data.interaction_date
      if (data.interaction_time)    state.time               = data.interaction_time
      if (data.topics_discussed)    state.topicsDiscussed    = data.topics_discussed
      if (data.sentiment)           state.sentiment          = data.sentiment
      if (data.outcomes)            state.outcomes           = data.outcomes
      if (data.follow_up_actions)   state.followUpActions    = data.follow_up_actions
      if (data.attendees)           state.attendees          = data.attendees
      if (data.materials_shared)    state.materialsShared    = data.materials_shared
      if (data.samples_distributed) state.samplesDistributed = data.samples_distributed
    },
    setSuggestedFollowups: (state, action) => {
      state.aiSuggestedFollowups = action.payload
    },
    addTag: (state, action) => {
      const { field, value } = action.payload
      if (value && !state[field].includes(value)) {
        state[field] = [...state[field], value]
      }
    },
    removeTag: (state, action) => {
      const { field, index } = action.payload
      state[field] = state[field].filter((_, i) => i !== index)
    },
    resetForm: () => initialState,
  },
  extraReducers: (builder) => {
    builder
      .addCase(saveInteraction.pending, (s) => {
        s.status = 'loading'
        s.error = null
      })
      .addCase(saveInteraction.fulfilled, (s, a) => {
        s.status = 'success'
        s.aiSummary = a.payload.ai_summary || ''
        s.savedInteractionId = a.payload.id
      })
      .addCase(saveInteraction.rejected, (s, a) => {
        s.status = 'error'
        s.error = a.payload || 'Failed to save interaction'
      })
  },
})

export const {
  updateField,
  populateFromChat,
  setSuggestedFollowups,
  addTag,
  removeTag,
  resetForm,
} = interactionSlice.actions
export default interactionSlice.reducer
