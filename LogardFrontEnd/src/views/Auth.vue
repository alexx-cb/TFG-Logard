<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { login, register, logout, isAuthenticated } from '@/composables/useAuth.js'

const route = useRoute()
const router = useRouter()

// Modos controlados por estado de autenticación y ruta
const mode = computed(() => {
  if (isAuthenticated.value) return 'authenticated'
  if (route.path.endsWith('/register')) return 'register'
  return 'login'
})

// Campos login
const email = ref('')
const password = ref('')

// Campos registro
const name = ref('')
const surname = ref('')

async function loginUser() {
  const res = await login(email.value, password.value)

  if (res.success) {
    email.value = ''
    password.value = ''
    alert('Login exitoso')
    await router.push('/')
  } else {
    const status = res?.error?.status
    if (status === 401) {
      alert("Credenciales incorrectas o no has autenticado tu correo")
    } else {
      alert("Ha ocurrido un error al iniciar sesión")
    }
  }
}

async function registerUser() {
  const res = await register(name.value, surname.value, email.value, password.value)

  if (res?.success === false) {
    alert('Error al registrar usuario.')
    return
  }

  alert('Usuario registrado correctamente.')
  name.value = ''
  surname.value = ''
  email.value = ''
  password.value = ''
  await router.push('/login')
}

async function logoutUser() {
  await logout()
  alert('Sesión cerrada')
  await router.push('/')
}

//escucha cambios de ruta para que el modo se actualice
watch(() =>
    route.path, () => {
})
</script>

<template>
  <div>
    <div v-if="mode === 'authenticated'">
      <p>¡Bienvenido! Estás autenticado.</p>
      <button @click="logoutUser">Cerrar sesión</button>
    </div>

    <div v-else>
      <button
        v-if="mode === 'login'"
        @click="() => router.push('/register')"
        style="margin-bottom: 1rem;"
      >
        ¿No tienes cuenta? Regístrate
      </button>
      <button
        v-else
        @click="() => router.push('/login')"
        style="margin-bottom: 1rem;"
      >
        ¿Ya tienes cuenta? Inicia sesión
      </button>

      <form v-if="mode === 'login'" @submit.prevent="loginUser">
        <input v-model="email" placeholder="Email" type="email" required />
        <input v-model="password" placeholder="Contraseña" type="password" required />
        <button type="submit">Iniciar sesión</button>
      </form>

      <form v-else-if="mode === 'register'" @submit.prevent="registerUser">
        <input v-model="name" placeholder="Nombre" required />
        <input v-model="surname" placeholder="Apellido" required />
        <input v-model="email" placeholder="Email" type="email" required />
        <input v-model="password" placeholder="Contraseña" type="password" required />
        <button type="submit">Registrarse</button>
      </form>
    </div>
  </div>
</template>
