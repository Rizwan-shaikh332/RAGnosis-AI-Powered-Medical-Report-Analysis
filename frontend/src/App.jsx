import { Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import LandingPage from './pages/LandingPage'
import RegisterPage from './pages/RegisterPage'
import LoginPage from './pages/LoginPage'
import Dashboard from './pages/Dashboard'
import SystemAnimation from './pages/SystemAnimation'
import { AuthProvider, useAuth } from './context/AuthContext'

function PrivateRoute({ children }) {
    const { user, loading } = useAuth()
    if (loading) return (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
            <div className="spinner" />
        </div>
    )
    return user ? children : <Navigate to="/login" replace />
}

function AppRoutes() {
    const { user } = useAuth()
    return (
        <>
            <Navbar />
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/system" element={<SystemAnimation />} />
                <Route path="/register" element={user ? <Navigate to="/dashboard" /> : <RegisterPage />} />
                <Route path="/login" element={user ? <Navigate to="/dashboard" /> : <LoginPage />} />
                <Route path="/dashboard/*" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
                <Route path="*" element={<Navigate to="/" />} />
            </Routes>
        </>
    )
}

export default function App() {
    return (
        <AuthProvider>
            <AppRoutes />
        </AuthProvider>
    )
}
