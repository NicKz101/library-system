import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Navbar from './components/Navbar'
import { ProtectedRoute, AdminRoute } from './components/ProtectedRoute'
import OverdueLoansWatcher from './components/OverdueLoansWatcher'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import BooksPage from './pages/BooksPage'
import MyLoansPage from './pages/MyLoansPage'
import AdminLoansPage from './pages/AdminLoansPage'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Navbar />
        <OverdueLoansWatcher />
        <Routes>
          <Route path="/" element={<Navigate to="/books" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/books"
            element={
              <ProtectedRoute>
                <BooksPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/my-loans"
            element={
              <ProtectedRoute>
                <MyLoansPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/loans"
            element={
              <AdminRoute>
                <AdminLoansPage />
              </AdminRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
