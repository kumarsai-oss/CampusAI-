import React from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown } from 'lucide-react'

interface StatsCardProps {
  title: string
  value: string | number
  icon: React.ReactNode
  trend?: number
  color?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger'
}

const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  icon,
  trend,
  color = 'primary',
}) => {
  const colorClasses = {
    primary: 'from-primary-500/20 to-primary-500/5',
    secondary: 'from-secondary-500/20 to-secondary-500/5',
    success: 'from-green-500/20 to-green-500/5',
    warning: 'from-yellow-500/20 to-yellow-500/5',
    danger: 'from-red-500/20 to-red-500/5',
  }

  return (
    <motion.div
      whileHover={{ y: -5 }}
      className={`glass p-6 bg-gradient-to-br ${colorClasses[color]} rounded-xl border border-white/10 hover:border-white/20 transition-all duration-300`}
    >
      <div className="flex justify-between items-start">
        <div>
          <p className="text-slate-400 text-sm font-medium mb-2">{title}</p>
          <p className="text-2xl font-bold text-white">{value}</p>
          {trend !== undefined && (
            <div className={`flex items-center gap-1 mt-2 text-sm ${
              trend >= 0 ? 'text-green-400' : 'text-red-400'
            }`}>
              {trend >= 0 ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
              <span>{Math.abs(trend)}% from last month</span>
            </div>
          )}
        </div>
        <div className="p-3 rounded-lg bg-white/5 text-primary-400">
          {icon}
        </div>
      </div>
    </motion.div>
  )
}

export default StatsCard
