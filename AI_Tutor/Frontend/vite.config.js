import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  root: '.', // The root of your source code, "." for project root
  base: '/', // Base public path when served in development or production
  publicDir: 'public',
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    proxy: {
      // Proxy API endpoints to the Flask backend
      '/api': {
        target: 'http://localhost:5000', // Flask backend address
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
    }
  }
})