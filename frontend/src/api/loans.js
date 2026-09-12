import api from './client'

export async function borrowBook(bookId, durationDays, quantity = 1) {
  const { data } = await api.post('/loans/', {
    book_id: bookId,
    duration_days: durationDays,
    quantity,
  })
  return data
}

export async function returnLoan(loanId) {
  const { data } = await api.post(`/loans/${loanId}/return`)
  return data
}

export async function myLoans() {
  const { data } = await api.get('/loans/me')
  return data
}

export async function allLoans() {
  const { data } = await api.get('/loans/')
  return data
}
