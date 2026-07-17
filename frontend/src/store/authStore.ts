import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface User {
  id: number
  username: string
  email: string
  full_name: string
  role: 'admin' | 'faculty' | 'student'
  is_active: boolean
}

export interface AuthStore {
  user: User | null
  token: string | null
  refreshToken: string | null
  isLoading: boolean
  login: (user: User, token: string, refreshToken: string) => void
  logout: () => void
  setUser: (user: User) => void
  setLoading: (loading: boolean) => void
}

export const useAuthStore = create<AuthStore>(
  persist(
    (set) => ({
      user: null,
      token: null,
      refreshToken: null,
      isLoading: false,
      login: (user, token, refreshToken) => set({ user, token, refreshToken }),
      logout: () => set({ user: null, token: null, refreshToken: null }),
      setUser: (user) => set({ user }),
      setLoading: (loading) => set({ isLoading: loading }),
    }),
    {
      name: 'auth-store',
    }
  )
)
