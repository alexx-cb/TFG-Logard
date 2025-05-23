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
    // Asumiendo que axios ya tiene baseURL configurada
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
    <h2>Verificación de Cuenta</h2>
    <p>{{ message }}</p>
    <button v-if="message.includes('correctamente')" @click="goToLogin">
      Ir a Iniciar Sesión
    </button>
  </div>
</template>
