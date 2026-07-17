import React from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { UserCheck, Briefcase, Users } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'

const roles = [
  {
    id: 'admin',
    title: 'Administrator',
    description: 'Manage students, faculty, and campus operations',
    icon: Users,
    color: 'from-primary-500 to-blue-600',
  },
  {
    id: 'faculty',
    title: 'Faculty Member',
    description: 'Manage classes, attendance, and student grades',
    icon: Briefcase,
    color: 'from-secondary-500 to-purple-600',
  },
  {
    id: 'student',
    title: 'Student',
    description: 'View attendance, results, and campus notices',
    icon: UserCheck,
    color: 'from-green-500 to-teal-600',
  },
]

const RoleSelectionPage: React.FC = () => {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { user, login } = useAuthStore()
  const mode = searchParams.get('mode') // 'register' or 'login'

  const handleRoleSelect = (roleId: 'admin' | 'faculty' | 'student') => {
    if (user) {
      const updatedUser = { ...user, role: roleId }
      login(updatedUser, 'mock-token', 'mock-refresh-token')
      navigate(`/${roleId}`)
    } else {
      navigate(`/login?role=${roleId}`)
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
        className="w-full max-w-4xl relative z-10"
      >
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold gradient-text mb-2">Select Your Role</h1>
          <p className="text-slate-400 text-lg">Choose how you'll use CampusAI</p>
        </div>

        {/* Role Cards */}
        <div className="grid md:grid-cols-3 gap-6">
          {roles.map((role, index) => {
            const Icon = role.icon
            return (
              <motion.button
                key={role.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -10 }}
                onClick={() => handleRoleSelect(role.id as 'admin' | 'faculty' | 'student')}
                className="group glass p-8 rounded-2xl border border-white/10 hover:border-white/20 transition-all duration-300 text-left"
              >
                {/* Icon */}
                <div className={`inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br ${role.color} rounded-xl mb-4 group-hover:scale-110 transition-transform`}>
                  <Icon className="w-8 h-8 text-white" />
                </div>

                {/* Content */}
                <h2 className="text-xl font-bold text-white mb-2">{role.title}</h2>
                <p className="text-slate-400 text-sm mb-6">{role.description}</p>

                {/* Button */}
                <div className={`inline-block px-4 py-2 rounded-lg bg-gradient-to-r ${role.color} text-white font-medium group-hover:shadow-lg transition-all duration-300`}>
                  Select
                </div>
              </motion.button>
            )
          })}
        </div>

        {/* Info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-12 glass p-6 rounded-xl border border-white/10 text-center"
        >
          <p className="text-slate-400">You can change your role anytime from your account settings</p>
        </motion.div>
      </motion.div>
    </div>
  )
}

export default RoleSelectionPage
