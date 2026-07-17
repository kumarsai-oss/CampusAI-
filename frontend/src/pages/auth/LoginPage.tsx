import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Eye, EyeOff, Mail, Lock, AlertCircle } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'

const loginSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})

type LoginFormData = z.infer<typeof loginSchema>

const LoginPage: React.FC = () => {
  const navigate = useNavigate()
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const { login } = useAuthStore()
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true)
    setError('')

    try {
      // Mock login - replace with actual API call
      const mockUser = {
        id: 1,
        username: data.username,
        email: `${data.username}@campusai.com`,
        full_name: 'Test User',
        role: data.username === 'admin' ? 'admin' : data.username === 'faculty' ? 'faculty' : 'student',
        is_active: true,
      }

      login(mockUser, 'mock-token', 'mock-refresh-token')
      navigate(`/${mockUser.role}`)
    } catch (err) {
      setError('Invalid credentials')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      {/* Animated background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <motion.div
          animate={{
            x: [0, 100, 0],
            y: [0, -100, 0],
          }}
          transition={{ duration: 20, repeat: Infinity }}
          className="absolute top-0 left-1/4 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl"
        />
        <motion.div
          animate={{
            x: [0, -100, 0],
            y: [0, 100, 0],
          }}
          transition={{ duration: 20, repeat: Infinity }}
          className="absolute bottom-0 right-1/4 w-96 h-96 bg-secondary-500/20 rounded-full blur-3xl"
        />
      </div>

      {/* Content */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md relative z-10"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-2xl mb-4">
            <span className="text-white font-bold text-2xl">CA</span>
          </div>
          <h1 className="text-3xl font-bold gradient-text mb-2">CampusAI</h1>
          <p className="text-slate-400">Campus Management System</p>
        </div>

        {/* Form Card */}
        <div className="glass p-8 rounded-2xl border border-white/10">
          <h2 className="text-2xl font-bold text-white mb-6">Welcome Back</h2>

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg flex items-center gap-3 text-red-400"
            >
              <AlertCircle size={20} />
              <span>{error}</span>
            </motion.div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {/* Username */}
            <div>
              <label className="block text-sm font-medium text-slate-200 mb-2">
                Username
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 text-slate-400" size={20} />
                <input
                  type="text"
                  placeholder="Enter your username"
                  {...register('username')}
                  className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:border-primary-500/50 focus:outline-none focus:ring-1 focus:ring-primary-500/30 transition-all"
                />
              </div>
              {errors.username && (
                <p className="text-red-400 text-sm mt-1">{errors.username.message}</p>
              )}
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-slate-200 mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 text-slate-400" size={20} />
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  {...register('password')}
                  className="w-full pl-10 pr-10 py-3 bg-white/5 border border-white/10 rounded-lg focus:border-primary-500/50 focus:outline-none focus:ring-1 focus:ring-primary-500/30 transition-all"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-3 text-slate-400 hover:text-slate-200"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
              {errors.password && (
                <p className="text-red-400 text-sm mt-1">{errors.password.message}</p>
              )}
            </div>

            {/* Remember & Forgot */}
            <div className="flex justify-between items-center">
              <label className="flex items-center gap-2 text-sm text-slate-400 hover:text-slate-300">
                <input type="checkbox" className="rounded" />
                Remember me
              </label>
              <Link to="/forgot-password" className="text-sm text-primary-400 hover:text-primary-300">
                Forgot Password?
              </Link>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 rounded-lg bg-gradient-to-r from-primary-500 to-secondary-500 text-white font-medium hover:from-primary-600 hover:to-secondary-600 disabled:from-slate-600 disabled:to-slate-600 transition-all duration-300 shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Signing In...
                </>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="my-6 flex items-center gap-4">
            <div className="flex-1 h-px bg-white/10" />
            <span className="text-slate-400 text-sm">OR</span>
            <div className="flex-1 h-px bg-white/10" />
          </div>

          {/* Sign Up Link */}
          <p className="text-center text-slate-400">
            Don't have an account?{' '}
            <Link to="/register" className="text-primary-400 hover:text-primary-300 font-medium">
              Sign Up
            </Link>
          </p>

          {/* Demo Credentials */}
          <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
            <p className="text-xs text-blue-400 font-medium mb-2">Demo Credentials:</p>
            <div className="space-y-1 text-xs text-blue-300">
              <p>Admin: admin / admin123456</p>
              <p>Faculty: faculty / faculty123456</p>
              <p>Student: student / student123456</p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default LoginPage
