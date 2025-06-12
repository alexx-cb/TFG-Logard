<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { isAuthenticated, tryRefreshToken } from "@/composables/useAuth.js";
import { onMounted, ref } from "vue";
import Footer from "@/views/Footer.vue"

const menuOpen = ref(false);

onMounted(async () => {
  await tryRefreshToken();
});
</script>

<template>
  <header class="main-header">
    <div class="nav-container">
      <button class="hamburger" @click="menuOpen = !menuOpen" aria-label="Menú">
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
      </button>

      <div class="nav-left">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/categories">Categories</RouterLink>
      </div>

      <div class="nav-center">
        <RouterLink to="/" class="logo">
          <img src="../public/img/Logard.png" alt="logo" class="logo-img" />
        </RouterLink>
      </div>

      <div class="nav-right">
        <RouterLink v-if="isAuthenticated" to="/my-orders">My Orders</RouterLink>
        <RouterLink v-if="!isAuthenticated" to="/login">Login</RouterLink>
        <RouterLink v-else to="/session">Session</RouterLink>
        <RouterLink v-if="isAuthenticated" to="/cart">Cart</RouterLink>
        <RouterLink v-else to="/anonymous-cart">Cart</RouterLink>
      </div>
    </div>

    <!-- Menú móvil -->
    <nav class="mobile-menu" :class="{ open: menuOpen }">
      <RouterLink to="/" @click="menuOpen = false">Home</RouterLink>
      <RouterLink to="/categories" @click="menuOpen = false">Categories</RouterLink>
      <RouterLink v-if="isAuthenticated" to="/my-orders" @click="menuOpen = false">My Orders</RouterLink>
      <RouterLink v-if="!isAuthenticated" to="/login" @click="menuOpen = false">Login</RouterLink>
      <RouterLink v-else to="/session" @click="menuOpen = false">Session</RouterLink>
      <RouterLink v-if="isAuthenticated" to="/cart" @click="menuOpen = false">Cart</RouterLink>
      <RouterLink v-else to="/anonymous-cart" @click="menuOpen = false">Cart</RouterLink>
    </nav>
    <div v-if="menuOpen" class="backdrop" @click="menuOpen = false"></div>
  </header>
  <hr class="header-divider" />
  <RouterView />

  <Footer></Footer>
</template>

<style scoped>
.header-divider {
  border: none;
  border-bottom: 1px solid #ffd700;
  margin: 0;
  width: 100%;
  box-shadow: 0 1px 8px #111a;
}

.main-header {
  background-color: black;
  padding: 1.5rem 2rem;
  position: relative;
  z-index: 100;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #ffd700;
  font-weight: bold;
  font-size: 1.2rem;
  position: relative;
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
  flex: 1;
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

a, .router-link-active {
  color: #ffd700;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

/* Hamburguesa */
.hamburger {
  display: none;
  flex-direction: column;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  z-index: 110;
  margin-right: 12px;
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
}

.hamburger span {
  display: block;
  width: 28px;
  height: 3px;
  background: #ffd700;
  border-radius: 2px;
  transition: all 0.3s;
}

.hamburger span.open:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}
.hamburger span.open:nth-child(2) {
  opacity: 0;
}
.hamburger span.open:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* Menú móvil */
.mobile-menu {
  display: none;
}

.backdrop {
  display: none;
}

/* Responsive */
@media (max-width: 768px) {
  .main-header {
    padding: 0.7rem 0.5rem;
  }
  .nav-container {
    flex-direction: row;
    padding: 0;
    font-size: 1rem;
  }
  .nav-left,
  .nav-right {
    display: none;
  }
  .nav-center {
    flex: 1;
    justify-content: center;
  }
  .logo-img {
    width: 90px;
    height: 44px;
  }
  .hamburger {
    display: flex;
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
  }
  .mobile-menu {
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0;
    right: 0;
    width: 80vw;
    max-width: 320px;
    height: 100vh;
    background: #000;
    box-shadow: -2px 0 12px #111a;
    z-index: 120;
    gap: 0;
    padding: 80px 0 0 0;
    transform: translateX(100%);
    opacity: 0;
    pointer-events: none;
    transition: transform 0.3s, opacity 0.3s;
  }
  .mobile-menu.open {
    transform: translateX(0);
    opacity: 1;
    pointer-events: all;
  }
  .mobile-menu a {
    color: #ffd700;
    text-decoration: none;
    font-weight: bold;
    font-size: 1.15rem;
    padding: 18px 32px;
    border-bottom: 1px solid #222;
    transition: background 0.2s;
  }
  .mobile-menu a:last-child {
    border-bottom: none;
  }
  .mobile-menu a:hover {
    background: #222;
  }
  .backdrop {
    display: block;
    position: fixed;
    inset: 0;
    background: #000a;
    z-index: 110;
  }
}
@media (max-width: 400px) {
  .logo-img {
    width: 60px;
    height: 28px;
  }
  .mobile-menu a {
    font-size: 1rem;
    padding: 14px 16px;
  }
}
</style>