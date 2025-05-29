<script setup>
// COMPONENTE PARA CREAR NUEVOS PRODUCTOS(FORMULARIO)

import { user } from '@/composables/useAuth';

defineProps({
  categoryId: Number
})
</script>

<template>

  <div>
    <h1>Crear Productos</h1>

    {{categoryId}}

  </div>

</template>

<style scoped>

</style>