import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import axios from 'axios'
import App from './App.jsx'
import './index.css'

// Configure axios to use backend API
// Use environment variable, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
axios.defaults.baseURL = API_BASE_URL

// For debugging (remove in production)
console.log('🔗 API Base URL:', API_BASE_URL)

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <BrowserRouter>
            <App />
            <Toaster
                position="top-right"
                toastOptions={{
                    style: {
                        background: 'var(--bg-card)',
                        color: 'var(--text-primary)',
                        border: '1px solid var(--border)',
                        borderRadius: '12px',
                        fontFamily: 'Inter, sans-serif',
                    },
                    success: { iconTheme: { primary: '#00d4aa', secondary: '#0a0f1e' } },
                    error: { iconTheme: { primary: '#ff4d6d', secondary: '#0a0f1e' } },
                }}
            />
        </BrowserRouter>
    </React.StrictMode>
)
