import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  Users,
  BookOpen,
  Clock,
  FileText,
  AlertCircle,
  DollarSign,
  Bell,
  LogOut,
  ChevronLeft,
} from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { motion } from 'framer-motion'

interface SidebarProps {
  isOpen?: boolean
  onClose?: () => void
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen = true, onClose }) => {
  const { user, logout } = useAuthStore()
  const location = useLocation()

  const adminMenuItems = [
    { icon: LayoutDashboard, label: 'Dashboard', href: '/admin' },
    { icon: Users, label: 'Students', href: '/admin/students' },
    { icon: BookOpen, label: 'Faculty', href: '/admin/faculty' },
    { icon: Clock, label: 'Attendance', href: '/admin/attendance' },
    { icon: FileText, label: 'Timetable', href: '/admin/timetable' },
    { icon: DollarSign, label: 'Fees', href: '/admin/fees' },
    { icon: Bell, label: 'Notices', href: '/admin/notices' },
  ]

  const facultyMenuItems = [
    { icon: LayoutDashboard, label: 'Dashboard', href: '/faculty' },
    { icon: Clock, label: 'Attendance', href: '/faculty/attendance' },
    { icon: FileText, label: 'Timetable', href: '/faculty/timetable' },
    { icon: Users, label: 'Students', href: '/faculty/students' },
  ]

  const studentMenuItems = [
    { icon: LayoutDashboard, label: 'Dashboard', href: '/student' },
    { icon: Clock, label: 'Attendance', href: '/student/attendance' },
    { icon: FileText, label: 'Results', href: '/student/results' },
    { icon: FileText, label: 'Timetable', href: '/student/timetable' },
    { icon: DollarSign, label: 'Fees', href: '/student/fees' },
    { icon: Bell, label: 'Notices', href: '/student/notices' },
  ]

  const menuItems = user?.role === 'admin' ? adminMenuItems : user?.role === 'faculty' ? facultyMenuItems : studentMenuItems

  const isActive = (href: string) => location.pathname === href || location.pathname.startsWith(href + '/')

  return (
    <motion.aside
      initial={{ x: -300 }}
      animate={{ x: isOpen ? 0 : -300 }}
      transition={{ duration: 0.3 }}
      className="fixed left-0 top-16 bottom-0 w-64 glass border-r border-white/10 overflow-y-auto md:translate-x-0 z-40"
    >
      <div className="p-6">
        <nav className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon
            const active = isActive(item.href)

            return (
              <Link
                key={item.href}
                to={item.href}
                onClick={onClose}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 ${
                  active
                    ? 'bg-gradient-to-r from-primary-500/20 to-secondary-500/20 text-primary-300 border border-primary-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                }`}
              >
                <Icon size={20} />
                <span className="font-medium">{item.label}</span>
              </Link>
            )
          })}
        </nav>

        <div className="border-t border-white/10 mt-6 pt-6">
          <button
            onClick={logout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-red-400 hover:bg-red-500/10 transition-all duration-300"
          >
            <LogOut size={20} />
            <span className="font-medium">Logout</span>
          </button>
        </div>
      </div>
    </motion.aside>
  )
}

export default Sidebar
