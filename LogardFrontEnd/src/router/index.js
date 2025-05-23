import { createRouter, createWebHistory } from 'vue-router'
import Landing from '../views/Landing.vue'
import Auth from '../views/Auth.vue'
import Orders from '../views/Orders.vue'
import Verify from "@/views/Verify.vue";
import Categories from "@/views/Categories.vue";

const routes = [
    { path: '/', name: 'home',component: Landing,},
    { path: '/login',name: 'login' ,component: Auth },
    { path: '/register',name:'register' ,component: Auth },
    { path: '/session',name:'your-session', component: Auth, meta: { requiresAuth: true }},
    { path: '/my-orders',name: 'orders', meta: {requiresAuth: true},component: Orders },
    { path: '/categories', name: 'categories-list', component: Categories},
    { path: '/verify', name: 'verify-user', component: Verify},
]

const router = createRouter({
    history: createWebHistory(),
    routes
})



export default router
