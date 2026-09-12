import api from './client'

export async function listBooks(category) {
  const { data } = await api.get('/books/', { params: category ? { category } : {} })
  return data
}

export async function createBook(book) {
  const { data } = await api.post('/books/', book)
  return data
}

export async function updateBook(bookId, updates) {
  const { data } = await api.put(`/books/${bookId}`, updates)
  return data
}

export async function deleteBook(bookId) {
  await api.delete(`/books/${bookId}`)
}
