import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import ProtectedRoute from './components/ProtectedRoute'

// Pages
import LoginPage from './pages/auth/LoginPage'
import RegisterPage from './pages/auth/RegisterPage'
import ForgotPasswordPage from './pages/auth/ForgotPasswordPage'
import RoleSelectionPage from './pages/auth/RoleSelectionPage'

import AdminDashboard from './pages/admin/AdminDashboard'
import StudentDashboard from './pages/student/StudentDashboard'
import FacultyDashboard from './pages/faculty/FacultyDashboard'

import StudentManagement from './pages/admin/StudentManagement'
import FacultyManagement from './pages/admin/FacultyManagement'
import AttendanceAdmin from './pages/admin/AttendanceAdmin'
import TimetableAdmin from './pages/admin/TimetableAdmin'
import FeesAdmin from './pages/admin/FeesAdmin'
import NoticesAdmin from './pages/admin/NoticesAdmin'

import NotFound from './pages/NotFound'

function App() {
  const { user, isLoading } = useAuthStore()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-slate-950">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    )
  }

  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/select-role" element={<RoleSelectionPage />} />

        {/* Admin Routes */}
        <Route
          path="/admin/*"
          element={
            <ProtectedRoute requiredRole="admin">
              <Routes>
                <Route path="" element={<AdminDashboard />} />
                <Route path="students" element={<StudentManagement />} />
                <Route path="faculty" element={<FacultyManagement />} />
                <Route path="attendance" element={<AttendanceAdmin />} />
                <Route path="timetable" element={<TimetableAdmin />} />
                <Route path="fees" element={<FeesAdmin />} />
                <Route path="notices" element={<NoticesAdmin />} />
              </Routes>
            </ProtectedRoute>
          }
        />

        {/* Faculty Routes */}
        <Route
          path="/faculty/*"
          element={
            <ProtectedRoute requiredRole="faculty">
              <Routes>
                <Route path="" element={<FacultyDashboard />} />
              </Routes>
            </ProtectedRoute>
          }
        />

        {/* Student Routes */}
        <Route
          path="/student/*"
          element={
            <ProtectedRoute requiredRole="student">
              <Routes>
                <Route path="" element={<StudentDashboard />} />
              </Routes>
            </ProtectedRoute>
          }
        />

        {/* Home Route */}
        <Route
          path="/"
          element={
            user ? (
              <Navigate to={`/${user.role}`} />
            ) : (
              <Navigate to="/login" />
            )
          }
        />

        {/* 404 */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  )
}

export default App
