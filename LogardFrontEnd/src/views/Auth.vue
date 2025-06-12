<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { login, register, logout, isAuthenticated } from '@/composables/useAuth.js'

const route = useRoute()
const router = useRouter()

const mode = computed(() => {
  if (isAuthenticated.value) return 'authenticated'
  if (route.path.endsWith('/register')) return 'register'
  return 'login'
})

const email = ref('')
const password = ref('')
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

watch(() => route.path, () => {})
</script>

<template>
  <div class="auth-container">
    <div v-if="mode === 'authenticated'" class="auth-box">
      <p>¡Bienvenido! Estás autenticado.</p>
      <button class="auth-btn" @click="logoutUser">Cerrar sesión</button>
    </div>

    <div v-else class="auth-box">
      <form v-if="mode === 'login'" @submit.prevent="loginUser" class="auth-form">
        <input v-model="email" placeholder="Email" type="email" required />
        <input v-model="password" placeholder="Contraseña" type="password" required />
        <button type="submit" class="auth-btn">Iniciar sesión</button>
        <button
          type="button"
          class="switch-btn"
          @click="() => router.push('/register')"
        >
          ¿No tienes cuenta? Regístrate
        </button>
      </form>

      <form v-else-if="mode === 'register'" @submit.prevent="registerUser" class="auth-form">
        <input v-model="name" placeholder="Nombre" required />
        <input v-model="surname" placeholder="Apellido" required />
        <input v-model="email" placeholder="Email" type="email" required />
        <input v-model="password" placeholder="Contraseña" type="password" required />
        <button type="submit" class="auth-btn">Registrarse</button>
        <button
          type="button"
          class="switch-btn"
          @click="() => router.push('/login')"
        >
          ¿Ya tienes cuenta? Inicia sesión
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  min-height: 100vh;
  background: #000;
  color: #ffe600;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Arial', sans-serif;
}

.auth-box {
  background: #181818;
  border-radius: 14px;
  box-shadow: 0 0 0 4px #ff0000, 0 0 16px 0 #ff0000 inset;
  padding: 38px 30px 30px 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 320px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.auth-form input {
  background: #222;
  color: #ffe600;
  border: 1px solid #ffe600;
  border-radius: 6px;
  padding: 10px 14px;
  font-size: 1rem;
  outline: none;
}

.auth-btn {
  background: #444;
  color: #ffe600;
  border: none;
  padding: 12px 0;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 8px;
}

.auth-btn:hover {
  background: #222;
}

.switch-btn {
  background: none;
  border: none;
  color: #ffe600;
  font-size: 1rem;
  margin-top: 18px;
  cursor: pointer;
  text-decoration: underline;
  align-self: center;
  transition: color 0.2s;
}

.switch-btn:hover {
  color: #fff700;
}

@media (max-width: 600px) {
  .auth-box {
    min-width: unset;
    width: 98vw;
    padding: 24px 4vw;
  }
}
</style>
