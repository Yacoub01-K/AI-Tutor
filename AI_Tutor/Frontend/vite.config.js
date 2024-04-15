import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path';
import monacoEditorPlugin from 'vite-plugin-monaco-editor';



export default defineConfig({
  root: '.', // The root of your source code, "." for project root
  base: '/', // Base public path when served in development or production
  publicDir: 'public',
  plugins: [vue(),
    monacoEditorPlugin({
    languageWorkers: ['typescript', 'javascript', 'css', 'html', 'json'],
    customDistPath: '/node_modules/monaco-editor/min/vs',
    globalAPI: true  // This can expose the editor API globally if needed
  
    })
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
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


  
})
