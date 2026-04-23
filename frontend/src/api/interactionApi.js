import apiClient from './apiClient'

export const submitInteraction = (data) => apiClient.post('/interactions/', {
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

export const searchHCPs = (q) => apiClient.get('/hcps/search', { params: { q } })

export const getInteractions = (params) => apiClient.get('/interactions/', { params })

export const deleteInteraction = (id) => apiClient.delete(`/interactions/${id}`)
