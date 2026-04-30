// src/api/client.js
import axios from 'axios'
import useAuthStore from '../store/authStore'

const client = axios.create({
  // Direct connection to backend to avoid proxy-induced CORS redirect issues.
  baseURL: import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000',
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.request.use(config => {
  const token = useAuthStore.getState().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

client.interceptors.response.use(
  r => r,
  err => {
    if (err.response?.status === 401) {
      useAuthStore.getState().logout()
    }
    return Promise.reject(err)
  }
)

export default client