// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import HomeView from '../views/HomeView.vue';

const routes = [
    {
        path: '/',
        name: 'Login',
        component: LoginView,
    },
    {
        path: '/home',
        name: 'Home',
        component: HomeView,
    }
    // Add more routes here
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

export default router;
