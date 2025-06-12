<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

function goHome() {
  router.push('/');
}
</script>

<template>
  <div class="error404-container">
    <div class="error-content">
      <div class="error-icon">🚫</div>
      <h1>Error 404</h1>
      <p>the page you search does not exits</p>
      <button @click="goHome" class="home-btn">Back Home</button>
    </div>
  </div>
</template>

<style scoped>
.error404-container {
  min-height: 100vh;
  background: #000;
  color: #ffe600;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Arial', sans-serif;
}

.error-content {
  text-align: center;
}

.error-icon {
  font-size: 5rem;
  margin-bottom: 24px;
}

h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 12px;
}

p {
  font-size: 1.2rem;
  margin-bottom: 32px;
}

.home-btn {
  background: #444;
  color: #ffe600;
  border: none;
  padding: 12px 36px;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.home-btn:hover {
  background: #222;
}
</style>
