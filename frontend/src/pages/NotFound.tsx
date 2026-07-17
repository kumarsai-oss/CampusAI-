import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Home, AlertCircle } from 'lucide-react'

const NotFound: React.FC = () => {
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
      </div>

      {/* Content */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center relative z-10"
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
          className="inline-block mb-8"
        >
          <AlertCircle className="w-24 h-24 text-yellow-500" />
        </motion.div>
        <h1 className="text-6xl font-bold gradient-text mb-4">404</h1>
        <p className="text-2xl text-white mb-2">Page Not Found</p>
        <p className="text-slate-400 mb-8 max-w-md">Sorry, the page you're looking for doesn't exist or has been moved.</p>

        <Link
          to="/"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-gradient-to-r from-primary-500 to-secondary-500 text-white font-medium hover:from-primary-600 hover:to-secondary-600 transition-all duration-300 shadow-lg hover:shadow-xl"
        >
          <Home size={20} />
          Go to Home
        </Link>
      </motion.div>
    </div>
  )
}

export default NotFound
