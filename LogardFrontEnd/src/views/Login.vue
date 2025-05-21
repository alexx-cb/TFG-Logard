<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref(null)
const router = useRouter()

const login = async () => {
  try {
    const response = await axios.post('/api/token/', {
      username: username.value,
      password: password.value
    })
    localStorage.setItem('access', response.data.access)
    localStorage.setItem('refresh', response.data.refresh)
    axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
    await router.push('/productos')
  } catch (err) {
    error.value = 'Usuario o contraseña incorrectos.'
  }
}
</script>

<template>
  <div class="p-4 max-w-md mx-auto">
    <h2 class="text-xl font-bold mb-4">Iniciar sesión</h2>
    <form @submit.prevent="login" class="space-y-4">
      <input v-model="username" type="text" placeholder="Usuario" class="w-full p-2 border" />
      <input v-model="password" type="password" placeholder="Contraseña" class="w-full p-2 border" />
      <button type="submit" class="w-full bg-blue-500 text-white p-2">Entrar</button>
      <p v-if="error" class="text-red-500">{{ error }}</p>
    </form>
  </div>
</template>