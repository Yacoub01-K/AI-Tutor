import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  // Define your routes here
  { path: '/', component: () => import('../views/HomeView.vue') },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router