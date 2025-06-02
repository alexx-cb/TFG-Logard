<script setup>
import { RouterLink, RouterView } from 'vue-router'
import {isAuthenticated} from "@/composables/useAuth.js";


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
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
</style>
