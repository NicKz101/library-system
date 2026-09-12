import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { isAuthenticated, isAdmin, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-brand-700 text-white shadow-md">
      <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="font-bold text-lg tracking-tight">
          📚 Library System
        </Link>

        <div className="flex items-center gap-4 text-sm">
          {isAuthenticated ? (
            <>
              <Link to="/books" className="hover:text-brand-100 transition">
                Books
              </Link>
              <Link to="/my-loans" className="hover:text-brand-100 transition">
                My Loans
              </Link>
              {isAdmin && (
                <Link to="/admin/loans" className="hover:text-brand-100 transition">
                  All Loans
                </Link>
              )}
              <button
                onClick={handleLogout}
                className="bg-brand-600 hover:bg-brand-500 px-3 py-1.5 rounded-md transition"
              >
                Log Out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-brand-100 transition">
                Log In
              </Link>
              <Link
                to="/register"
                className="bg-brand-600 hover:bg-brand-500 px-3 py-1.5 rounded-md transition"
              >
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
