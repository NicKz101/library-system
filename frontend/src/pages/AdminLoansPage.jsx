import { useEffect, useState } from 'react'
import { allLoans, returnLoan } from '../api/loans'
import { listBooks } from '../api/books'
import { listUsers } from '../api/users'
import LoanTable from '../components/LoanTable'

export default function AdminLoansPage() {
  const [loans, setLoans] = useState([])
  const [bookTitles, setBookTitles] = useState({})
  const [memberNames, setMemberNames] = useState({})
  const [loading, setLoading] = useState(true)

  async function loadData() {
    setLoading(true)
    try {
      const [loansData, booksData, usersData] = await Promise.all([
        allLoans(),
        listBooks(),
        listUsers(),
      ])
      setLoans(loansData)
      setBookTitles(Object.fromEntries(booksData.map((b) => [b.id, b.title])))
      setMemberNames(
        Object.fromEntries(usersData.map((u) => [u.id, `${u.full_name} (${u.email})`]))
      )
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
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">All Loans</h1>
      {loading ? (
        <p className="text-gray-500 text-sm">Loading...</p>
      ) : (
        <LoanTable
          loans={loans}
          onReturn={handleReturn}
          bookTitles={bookTitles}
          memberNames={memberNames}
          showMemberColumn
        />
      )}
    </div>
  )
}
