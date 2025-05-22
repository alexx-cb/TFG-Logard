<script setup>
import { ref } from 'vue'
import { login } from '@/composables/useAuth.js'
import router from "@/router/index.js";

const email = ref('')
const password = ref('')

async function loginUser() {
  try {
    await login(email.value, password.value)
    alert('Login exitoso')
    // Aquí puedes redirigir o hacer algo más
  } catch (error) {
    alert('Usuario o contraseña incorrectos')
  }
}
</script>

<template>
  <form @submit.prevent="loginUser">
    <input v-model="email" placeholder="Email" type="email" required />
    <input v-model="password" placeholder="Contraseña" type="password" required />
    <button type="submit">Iniciar sesión</button>
  </form>

</template>