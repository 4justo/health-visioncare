import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const healthApi = {
  check: async () => {
    const response = await axios.get(`${API_URL}/api/v1/health`)
    return response.data
  },
  dbCheck: async () => {
    const response = await axios.get(`${API_URL}/api/v1/health/db`)
    return response.data
  }
}