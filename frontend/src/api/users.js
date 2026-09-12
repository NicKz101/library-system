import api from './client'

export async function listUsers() {
  const { data } = await api.get('/users/')
  return data
}
