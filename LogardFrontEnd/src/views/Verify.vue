<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const message = ref('Verificando usuario...')

async function goToLogin() {
  await router.push('/login')
}

onMounted(async () => {
  const token = route.query.token
  if (!token) {
    message.value = 'Token no encontrado en la URL.'
    return
  }

  try {
    const response = await axios.get('/verify/', {
      params: { token }
    })
    message.value = response.data.detail || 'Usuario verificado correctamente.'
  } catch (error) {
    message.value = error.response?.data?.detail || 'Error en la verificación.'
  }
})
</script>

<template>
  <div class="verification-container">
    <div class="verification-box">
      <h2>Verificación de Cuenta</h2>
      <p>{{ message }}</p>
      <button
        v-if="message.includes('correctamente')"
        @click="goToLogin"
        class="verification-button"
      >
        Ir a Iniciar Sesión
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
  color: #FFD700;
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
