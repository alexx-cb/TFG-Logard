import { createRouter, createWebHistory } from 'vue-router'
import Landing from '../views/Landing.vue'
import Login from '../views/Login.vue'
import Orders from '../views/Orders.vue'

const routes = [
        { path: '/', name: 'home',component: Landing,},
        { path: '/login', name: 'login',component: Login},
        { path: '/my-ordes',name: 'orders', meta: {requiresAuth: true},component: Orders }

]

const router = createRouter({
    history: createWebHistory(),
    routes
})



export default router
