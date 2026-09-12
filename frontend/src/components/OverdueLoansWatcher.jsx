import { useEffect, useRef, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { myLoans } from '../api/loans'
import { listBooks } from '../api/books'
import OverdueLoansModal from './OverdueLoansModal'

// Checks the logged-in member's loans right after login and pops up a
// warning if any are overdue. Runs once per login, not on every page
// change, and resets on logout so it checks again next time.
export default function OverdueLoansWatcher() {
  const { isAuthenticated } = useAuth()
  const [overdueLoans, setOverdueLoans] = useState([])
  const [bookTitles, setBookTitles] = useState({})
  const [dismissed, setDismissed] = useState(false)
  const hasCheckedRef = useRef(false)

  useEffect(() => {
    if (!isAuthenticated) {
      hasCheckedRef.current = false
      setOverdueLoans([])
      setDismissed(false)
      return
    }
    if (hasCheckedRef.current) return
    hasCheckedRef.current = true

    async function checkOverdueLoans() {
      try {
        const [loans, books] = await Promise.all([myLoans(), listBooks()])
        setBookTitles(Object.fromEntries(books.map((b) => [b.id, b.title])))
        setOverdueLoans(loans.filter((loan) => loan.status === 'OVERDUE'))
      } catch {
        // not critical - just skip the warning if this fails
      }
    }

    checkOverdueLoans()
  }, [isAuthenticated])

  if (dismissed) return null

  return (
    <OverdueLoansModal
      loans={overdueLoans}
      bookTitles={bookTitles}
      onClose={() => setDismissed(true)}
    />
  )
}
