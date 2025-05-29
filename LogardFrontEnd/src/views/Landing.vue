<script setup>

import {user} from "@/composables/useAuth.js";




</script>

<template>
  <h1>Hola</h1>
  <div>
    <p>{{ user ? JSON.stringify(user, null, 2) : 'No autenticado' }}</p>
  </div>
</template>
