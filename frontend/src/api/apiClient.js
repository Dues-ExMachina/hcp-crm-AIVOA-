import axios from 'axios'

const API_BASE_URL = import.meta.env.PROD 
  ? 'https://hcp-crm-aivoa.onrender.com/api' 
  : '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default apiClient
