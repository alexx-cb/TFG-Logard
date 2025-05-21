<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import router from "@/router/index.js";


router.beforeEach((to, from, next)=>{
    const isAuthenticated = !localStorage.getItem('token')

    if(to.meta.requiresAuth && !isAuthenticated){
      next('/login')
    }else{
      next()
    }
})

</script>

<template>
  <header>

    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/my-orders">My Orders</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
</style>
