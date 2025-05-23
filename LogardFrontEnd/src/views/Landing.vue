<script setup>
import { onMounted, ref } from "vue";
import { getCurrentUser } from "@/composables/useAuth.js";

let usuario = ref(null)

async function getUser() {
  const response = await getCurrentUser()
  if (response.success) {
    usuario.value = response.res  // Aquí accedes directo al objeto usuario
  } else {
    console.error("No se pudo obtener el usuario", response.error)
    usuario.value = null
  }
}

onMounted(() => {
  getUser()
})
</script>

<template>
  <h1>Hola</h1>
  <div>
    <p>{{ usuario ? JSON.stringify(usuario, null, 2) : 'No autenticado' }}</p>
  </div>
</template>
