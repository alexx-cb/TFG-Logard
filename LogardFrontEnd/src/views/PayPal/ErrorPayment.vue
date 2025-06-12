<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const error = ref('There was an error obtaining your order information.')

const errorParam = route.query.error

onMounted(() => {
  if (errorParam === 'notfound') {
    error.value = 'Not found the id of your order.'
  } else if (errorParam === 'server') {
    error.value = 'Server Error processing your order.'
  }
})

function volverAlInicio() {
  router.push('/')
}
</script>

<template>
  <div class="verification-container">
    <div class="verification-box">
      <h2>Failed Payment</h2>
      <p>{{ error }}</p>
      <button @click="volverAlInicio" class="verification-button">
        Back to Home
      </button>
    </div>
  </div>
</template>

<style scoped>
.verification-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #000;
  color: #fff;
  width: 100vw;
  height: 100vh;
  font-family: 'Arial', sans-serif;
}

.verification-box {
  background-color: rgba(25, 25, 25, 0.95);
  border: 1px solid #333;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 0 10px #000;
  max-width: 400px;
  width: 90%;
}

.verification-box h2 {
  color: #FF4444;
  margin-bottom: 20px;
  font-size: 24px;
}

.verification-box p {
  margin-bottom: 20px;
  font-size: 16px;
}

.verification-button {
  background-color: #FFD700;
  border: none;
  padding: 10px 20px;
  color: #000;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.verification-button:hover {
  background-color: #FFA500;
}
</style>