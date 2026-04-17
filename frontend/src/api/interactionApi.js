import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

export const submitInteraction = (data) => api.post('/interactions/', {
  hcp_id: data.hcpId || null,
  hcp_name: data.hcpName || null,
  rep_id: 1,
  interaction_type: data.interactionType,
  interaction_date: data.date,
  interaction_time: data.time || null,
  attendees: data.attendees,
  topics_discussed: data.topicsDiscussed,
  materials_shared: data.materialsShared,
  samples_distributed: data.samplesDistributed,
  sentiment: data.sentiment,
  outcomes: data.outcomes,
  follow_up_actions: data.followUpActions,
  raw_chat_input: null,
})

export const searchHCPs = (q) => api.get('/hcps/search', { params: { q } })

export const getInteractions = (params) => api.get('/interactions/', { params })

export const deleteInteraction = (id) => api.delete(`/interactions/${id}`)
