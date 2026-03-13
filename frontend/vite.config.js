import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        proxyTimeout: 180000,   // 3 min – BART can be slow on first load
        timeout: 180000,
        configure: (proxy) => {
          proxy.on('error', (err) => console.log('proxy err', err.message))
        },
      }
    }
  }
})

