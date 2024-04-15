// main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

self.MonacoEnvironment = {
    getWorkerUrl: function (moduleId, label) {
      if (label === 'typescript' || label === 'javascript') {
        return './ts.worker.bundle.js';
      } else if (label === 'json') {
        return './json.worker.bundle.js';
      } else if (label === 'css') {
        return './css.worker.bundle.js';
      } else if (label === 'html' || label === 'handlebars' || label === 'razor') {
        return './html.worker.bundle.js';
      } else {
        return './editor.worker.bundle.js'; // Fallback
      }
    }
  };

createApp(App).use(router).use(store).mount('#app')
