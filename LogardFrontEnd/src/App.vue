<script setup>
import { RouterLink, RouterView } from 'vue-router'
import {isAuthenticated, tryRefreshToken} from "@/composables/useAuth.js";
import {onMounted} from "vue";
import AnonymousCart from "@/views/Cart/AnonymousCart.vue";

onMounted(async () => {
  await tryRefreshToken();
})

</script>

<template>
  <header>

    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink  to="/login" v-if="!isAuthenticated">Login / Register</RouterLink>
        <RouterLink  to="/session" v-else>Your Session</RouterLink>
        <RouterLink to="/my-orders">My Orders</RouterLink>
        <RouterLink to="/categories">Categories</RouterLink>
        <RouterLink to="/cart" v-if="isAuthenticated">Cart</RouterLink>
        <RouterLink to="/anonymous-cart" v-else>AnonymousCart</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
</style>
