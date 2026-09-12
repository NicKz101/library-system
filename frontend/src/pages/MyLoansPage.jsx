import { useEffect, useState } from 'react'
import { myLoans, returnLoan } from '../api/loans'
import { listBooks } from '../api/books'
import LoanTable from '../components/LoanTable'

export default function MyLoansPage() {
  const [loans, setLoans] = useState([])
  const [bookTitles, setBookTitles] = useState({})
  const [loading, setLoading] = useState(true)

  async function loadData() {
    setLoading(true)
    try {
      const [loansData, booksData] = await Promise.all([myLoans(), listBooks()])
      setLoans(loansData)
      setBookTitles(Object.fromEntries(booksData.map((b) => [b.id, b.title])))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  async function handleReturn(loanId) {
    await returnLoan(loanId)
    loadData()
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">My Loans</h1>
      {loading ? (
        <p className="text-gray-500 text-sm">Loading...</p>
      ) : (
        <LoanTable loans={loans} onReturn={handleReturn} bookTitles={bookTitles} />
      )}
    </div>
  )
}
