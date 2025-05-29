import { createRouter, createWebHistory } from 'vue-router'
import Landing from '../views/Landing.vue'
import Auth from '../views/Auth.vue'
import Orders from '../views/Orders.vue'
import Verify from "@/views/Verify.vue";
import Categories from "@/views/Categories.vue";
import CreateProduct from "@/views/Products/CreateProduct.vue";
import DetailProducts from "@/views/Products/DetailProducts.vue";

const routes = [
    { path: '/', name: 'home',component: Landing,},

    // User Routes (LOGIN, REGISTER, SESSION)
    { path: '/login',name: 'login' ,component: Auth },
    { path: '/register',name:'register' ,component: Auth },
    { path: '/session',name:'your-session', component: Auth, meta: { requiresAuth: true }},

    // Products Routes (CREATE-PRODUCT, DETAIL)
    { path: '/create-product', name: 'create-product',meta:{requiresAuth: true}, component: CreateProduct},
    { path: '/detail-product', name: 'detail-product', component: DetailProducts},

    // Categories Routes (SHOW-CATEGORIES)
    { path: '/categories', name: 'categories-list', component: Categories},

    // Orders Routes (MY-ORDERS)
    { path: '/my-orders',name: 'orders', meta: {requiresAuth: true},component: Orders },

    // Verify Account Route (VERIFY)
    { path: '/verify', name: 'verify-user', component: Verify},

]

const router = createRouter({
    history: createWebHistory(),
    routes
})



export default router
