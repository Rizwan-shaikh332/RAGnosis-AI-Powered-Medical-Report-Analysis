import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import toast from 'react-hot-toast'

export default function Navbar() {
    const { user, logout } = useAuth()
    const location = useLocation()
    const navigate = useNavigate()

    const handleLogout = () => {
        logout()
        toast.success('Logged out successfully')
        navigate('/')
    }

    const isActive = (path) => location.pathname === path ? 'active' : ''

    return (
        <nav className="navbar">
            <div className="container navbar-inner">
                <Link to="/" className="navbar-logo">
                    <div className="logo-icon">R</div>
                    <span>RAG<span className="gradient-text">nosis</span></span>
                </Link>

                <ul className="navbar-links">
                    <li><Link to="/" className={isActive('/')}>Home</Link></li>
                    <li><Link to="/system" className={isActive('/system')}>How It Works</Link></li>
                    {user && <li><Link to="/dashboard" className={isActive('/dashboard')}>Dashboard</Link></li>}
                </ul>

                <div className="navbar-actions">
                    {user ? (
                        <>
                            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                                👋 {user.name?.split(' ')[0]}
                            </span>
                            <button className="btn-ghost" onClick={handleLogout} style={{ padding: '8px 16px', fontSize: '0.85rem' }}>
                                Logout
                            </button>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="btn-ghost" style={{ padding: '8px 16px', fontSize: '0.85rem' }}>Login</Link>
                            <Link to="/register" className="btn-primary" style={{ padding: '8px 18px', fontSize: '0.85rem' }}>Get Started</Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    )
}
