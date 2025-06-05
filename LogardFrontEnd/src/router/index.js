import { createRouter, createWebHistory } from 'vue-router'
import Landing from '../views/Landing.vue'
import Auth from '../views/Auth.vue'
import Orders from '../views/Orders.vue'
import Verify from "@/views/Verify.vue";
import Categories from "@/views/Categories/Categories.vue";
import DetailProducts from "@/views/Products/DetailProducts.vue";
import {isAuthenticated} from "@/composables/useAuth.js";
import Cart from "@/views/Cart/Cart.vue";

const routes = [
    // Landing Page
    { path: '/', name: 'home',component: Landing,},

    // User Routes (LOGIN, REGISTER, SESSION)
    { path: '/login',name: 'login' ,component: Auth },
    { path: '/register',name:'register' ,component: Auth },
    { path: '/session',name:'your-session', component: Auth, meta: { requiresAuth: true }},

    // Products Routes (DETAIL)
    { path: '/detail-product/:id', name: 'detail-product', component: DetailProducts},

    // Categories Routes (SHOW-CATEGORIES)
    { path: '/categories', name: 'categories-list', component: Categories},

    // Orders Routes (MY-ORDERS)
    { path: '/my-orders',name: 'orders', meta: {requiresAuth: true},component: Orders },

    // Cart Routes (SHOW_CART)
    { path: '/cart', name:'cart', meta:{requiresAuth: true}, component: Cart},

    // Verify Account Route (VERIFY)
    { path: '/verify', name: 'verify-user', component: Verify},

]

const router = createRouter({
    history: createWebHistory(),
    routes
})
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next('/login')
  } else {
    next()
  }
})


export default router
