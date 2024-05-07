import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'



export default defineConfig({
  root: '.', // The root of your source code, "." for project root
  base: '/', // Base public path when served in development or production
  publicDir: 'public',
  plugins: [vue()],

  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      'ace-builds': resolve(__dirname, './node_modules/ace-builds')
    },
  },
  server: {
    fs: {
      allow: ['..', '/app/node_modules']
    },

    host: '0.0.0.0',

    proxy: {
      // Proxy API endpoints to the Flask backend
      '/api/*': {
        target: 'http://localhost:8000', // Flask backend address
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
    },
  },
  
});
