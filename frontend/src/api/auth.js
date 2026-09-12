import api from './client'

export async function login(email, password) {
  // FastAPI's OAuth2PasswordRequestForm expects form-encoded data,
  // with the email sent in the 'username' field.
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', password)

  const { data } = await api.post('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return data // { access_token, token_type }
}

export async function register(email, password, fullName) {
  const { data } = await api.post('/auth/register', {
    email,
    password,
    full_name: fullName,
  })
  return data
}
