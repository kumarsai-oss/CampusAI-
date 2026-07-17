import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Mail, AlertCircle, CheckCircle, ArrowLeft } from 'lucide-react'

const forgotPasswordSchema = z.object({
  email: z.string().email('Invalid email address'),
})

type ForgotPasswordFormData = z.infer<typeof forgotPasswordSchema>

const ForgotPasswordPage: React.FC = () => {
  const navigate = useNavigate()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const { register, handleSubmit, formState: { errors } } = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(forgotPasswordSchema),
  })

  const onSubmit = async (data: ForgotPasswordFormData) => {
    setIsLoading(true)
    setError('')

    try {
      // Mock password reset
      await new Promise((resolve) => setTimeout(resolve, 1500))
      setSuccess(true)
    } catch (err) {
      setError('Failed to send reset email')
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
          <p className="text-slate-400">Reset Your Password</p>
        </div>

        {/* Form Card */}
        <div className="glass p-8 rounded-2xl border border-white/10">
          {success ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center py-8"
            >
              <CheckCircle className="w-16 h-16 text-green-400 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white mb-2">Check Your Email</h2>
              <p className="text-slate-400 mb-6">
                We've sent a password reset link to your email address.
              </p>
              <Link
                to="/login"
                className="inline-block px-6 py-2 rounded-lg bg-gradient-to-r from-primary-500 to-secondary-500 text-white font-medium hover:from-primary-600 hover:to-secondary-600 transition-all duration-300"
              >
                Back to Login
              </Link>
            </motion.div>
          ) : (
            <>
              <h2 className="text-2xl font-bold text-white mb-2">Forgot Password?</h2>
              <p className="text-slate-400 mb-6">Enter your email and we'll send you a link to reset your password.</p>

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
                {/* Email */}
                <div>
                  <label className="block text-sm font-medium text-slate-200 mb-2">
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 text-slate-400" size={20} />
                    <input
                      type="email"
                      placeholder="john@example.com"
                      {...register('email')}
                      className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:border-primary-500/50 focus:outline-none focus:ring-1 focus:ring-primary-500/30 transition-all"
                    />
                  </div>
                  {errors.email && (
                    <p className="text-red-400 text-sm mt-1">{errors.email.message}</p>
                  )}
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
                      Sending...
                    </>
                  ) : (
                    'Send Reset Link'
                  )}
                </button>
              </form>

              {/* Back to Login */}
              <Link
                to="/login"
                className="flex items-center justify-center gap-2 text-slate-400 hover:text-slate-200 mt-6 transition-colors"
              >
                <ArrowLeft size={20} />
                Back to Login
              </Link>
            </>
          )}
        </div>
      </motion.div>
    </div>
  )
}

export default ForgotPasswordPage
