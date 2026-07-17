import React from 'react'
import { Link } from 'react-router-dom'
import { Menu, X, LogOut, Settings } from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { motion } from 'framer-motion'

interface NavbarProps {
  onMenuClick?: () => void
  isMenuOpen?: boolean
}

const Navbar: React.FC<NavbarProps> = ({ onMenuClick, isMenuOpen }) => {
  const { user, logout } = useAuthStore()

  return (
    <nav className="glass fixed top-0 left-0 right-0 z-50 border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">CA</span>
            </div>
            <span className="font-bold text-lg gradient-text">CampusAI</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-4">
            {user && (
              <>
                <span className="text-slate-400 text-sm">{user.full_name}</span>
                <button className="p-2 hover:bg-white/10 rounded-lg transition-colors">
                  <Settings size={20} />
                </button>
                <button
                  onClick={logout}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white/10 transition-colors text-red-400"
                >
                  <LogOut size={20} />
                  Logout
                </button>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={onMenuClick}
            className="md:hidden p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
