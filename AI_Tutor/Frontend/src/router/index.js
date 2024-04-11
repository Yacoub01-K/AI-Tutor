import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import HomeView from '../views/HomeView.vue';
import AIView from '../views/AIView.vue';
import RegisterView from '../views/RegisterView.vue';
import intro from '../views/intro.vue';
import CodeView from '../views/CodeView.vue';


const routes = [
    {
        path:'/',
        name:'Intro',
        component: intro,
    },
    {
        path: '/Login',
        name: 'Login',
        component: LoginView,
    },
    {
        path: '/ai',
        name: 'AI',
        component: AIView,
    },
    {
        path: '/home',
        name: 'Home',
        component: HomeView,
    },
    {
        path:'/register',
        name:'Register',
        component: RegisterView,
    },
    {
        path: '/problems',
        name: 'Class',
        component: CodeView,
    }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

export default router;
