<script setup>
import { ref, onMounted } from "vue";
import { getLocalCartWithDetails } from "@/composables/useCart.js";

const cartItems = ref([]);

onMounted(async () => {
  cartItems.value = await getLocalCartWithDetails();
});
</script>

<template>
  <div>
    <h2>Carrito Anónimo</h2>
    <div v-if="cartItems.length === 0">El carrito está vacío</div>
    <ul>
      <li v-for="item in cartItems" :key="item.product + '-' + item.size">
        {{ item.product_info.name }} - Talla: {{ item.size }} - Unidades: {{ item.units }} -
        Precio: {{ item.product_info.price }} €
      </li>
    </ul>
  </div>
</template>
