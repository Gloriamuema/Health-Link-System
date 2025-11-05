import axios from 'axios'
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:4000/api'
const instance = axios.create({ baseURL: API_BASE, timeout: 10000 })
instance.interceptors.request.use(cfg => {
  const token = localStorage.getItem('token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})
export default instance
