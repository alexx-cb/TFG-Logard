<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { isAuthenticated, tryRefreshToken } from "@/composables/useAuth.js";
import { onMounted } from "vue";

onMounted(async () => {
  await tryRefreshToken();
});
</script>

<template>
  <header class="main-header">
    <div class="nav-container">
      <!-- Izquierda -->
      <div class="nav-left">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/categories">Categories</RouterLink>
      </div>

      <!-- Centro (Logo) -->
      <div class="nav-center">
        <RouterLink to="/" class="logo">
          <img src="@/assets/Logard.png" alt="logo" class="logo-img" />
        </RouterLink>
      </div>

      <!-- Derecha -->
      <div class="nav-right">
        <RouterLink v-if="isAuthenticated" to="/my-orders">My Orders</RouterLink>
        <RouterLink v-if="!isAuthenticated" to="/login">Login</RouterLink>
        <RouterLink v-else to="/session">Session</RouterLink>
        <RouterLink v-if="isAuthenticated" to="/cart">Cart</RouterLink>
        <RouterLink v-else to="/anonymous-cart">Cart</RouterLink>
      </div>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
.main-header {
  background-color: black;
  padding: 1.5rem 2rem;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #ffd700;
  font-weight: bold;
  font-size: 1.2rem;
}

.nav-left,
.nav-right {
  display: flex;
  gap: 2rem;
}

.nav-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ffd700;
  text-decoration: none;
}

.logo-img {
  width: 125px;
  height: 65px;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
}

a {
  color: #ffd700;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
