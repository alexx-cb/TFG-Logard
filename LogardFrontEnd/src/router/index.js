import { createRouter, createWebHistory } from 'vue-router'
import Landing from '../views/Landing.vue'
import Auth from '../views/Auth.vue'
import Orders from '../views/Orders/Orders.vue'
import Verify from "@/views/Verify.vue";
import Categories from "@/views/Categories/Categories.vue";
import DetailProducts from "@/views/Products/DetailProducts.vue";
import {isAuthenticated} from "@/composables/useAuth.js";
import Cart from "@/views/Cart/Cart.vue";
import AnonymousCart from "@/views/Cart/AnonymousCart.vue";
import NewOrder from "@/views/Orders/NewOrder.vue";
import PayPalCallBack from "@/views/PayPal/PayPalCallBack.vue";
import NotFound from "@/views/NotFound.vue";
import SuccessfullPayment from "@/views/PayPal/SuccessfullPayment.vue";
import ErrorPayment from "@/views/PayPal/ErrorPayment.vue";

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

    // Orders Routes (MY-ORDERS, NEW-ORDER)
    { path: '/my-orders',name: 'orders', meta: {requiresAuth: true},component: Orders },
    { path: '/new-order', name: 'new-order', meta: {requiresAuth: true}, component: NewOrder},

    // PayPal Routes (CALL-BACK)
    { path: '/paypal-callback', name:'paypal-callback', component: PayPalCallBack},
    { path: '/paypal-success', name:'paypal-success', component: PayPalCallBack},
    { path: '/payment-successful', name:'payment-succesful',meta: {requiresAuth: true} , component: SuccessfullPayment},
    { path: '/payment-error', name:'payment-error', meta:{requiresAuth: true} ,component: ErrorPayment},

    // Cart Routes (SHOW_CART, ANONYMOUS_CART)
    { path: '/cart', name:'cart',meta:{requiresAuth: true}, component: Cart},
    { path: '/anonymous-cart', name:'anonymous-cart', component: AnonymousCart},


    // Verify Account Route (VERIFY)
    { path: '/verify', name: 'verify-user', component: Verify},

    // Not Found Route (404)
    { path: '/:pathMatch(.*)*', name: 'not.found', component: NotFound}

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
