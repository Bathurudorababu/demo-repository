import { Route, Routes, Navigate, Link } from 'react-router-dom'
import Login from './Login'
import Register from './Register'
import Dashboard from './Dashboard'
import Meals from './Meals'
import Foods from './Foods'
import Goals from './Goals'
import Profile from './Profile'
import Analytics from './Analytics'

function Protected({ children }: { children: JSX.Element }) {
  const token = localStorage.getItem('access_token')
  return token ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <div className="min-h-screen">
      <nav className="bg-white shadow sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-3 flex gap-4 items-center">
          <Link to="/dashboard" className="font-semibold text-xl text-blue-600">Calorie Tracker</Link>
          <div className="flex-1" />
          <Link to="/meals" className="text-sm">Meals</Link>
          <Link to="/foods" className="text-sm">Foods</Link>
          <Link to="/goals" className="text-sm">Goals</Link>
          <Link to="/analytics" className="text-sm">Analytics</Link>
          <Link to="/profile" className="text-sm">Profile</Link>
        </div>
      </nav>
      <div className="max-w-5xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
          <Route path="/meals" element={<Protected><Meals /></Protected>} />
          <Route path="/foods" element={<Protected><Foods /></Protected>} />
          <Route path="/goals" element={<Protected><Goals /></Protected>} />
          <Route path="/profile" element={<Protected><Profile /></Protected>} />
          <Route path="/analytics" element={<Protected><Analytics /></Protected>} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </div>
    </div>
  )
}
