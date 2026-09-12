import { createContext, useContext, useState, useEffect } from 'react'
import { login as apiLogin, register as apiRegister } from '../api/auth'
import api from '../api/client'

const AuthContext = createContext(null)

/**
 * Decode a JWT payload without verifying the signature (verification
 * happens server-side on every request). Used only to read the role
 * client-side for UI decisions like showing/hiding admin screens.
 */
function decodeJwtPayload(token) {
  try {
    return JSON.parse(atob(token.split('.')[1]))
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('access_token'))
  const [role, setRole] = useState(() => {
    const existing = localStorage.getItem('access_token')
    return existing ? decodeJwtPayload(existing)?.role ?? null : null
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (token) {
      localStorage.setItem('access_token', token)
      setRole(decodeJwtPayload(token)?.role ?? null)
    } else {
      localStorage.removeItem('access_token')
      setRole(null)
    }
  }, [token])

  async function login(email, password) {
    setLoading(true)
    setError(null)
    try {
      const { access_token } = await apiLogin(email, password)
      setToken(access_token)
      return true
    } catch (err) {
      setError(err.response?.data?.detail ?? 'Login failed')
      return false
    } finally {
      setLoading(false)
    }
  }

  async function register(email, password, fullName) {
    setLoading(true)
    setError(null)
    try {
      await apiRegister(email, password, fullName)
      return await login(email, password)
    } catch (err) {
      setError(err.response?.data?.detail ?? 'Registration failed')
      return false
    } finally {
      setLoading(false)
    }
  }

  function logout() {
    setToken(null)
  }

  const value = {
    token,
    role,
    isAuthenticated: !!token,
    isAdmin: role === 'ADMIN',
    loading,
    error,
    login,
    register,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider')
  return ctx
}

export { api }
