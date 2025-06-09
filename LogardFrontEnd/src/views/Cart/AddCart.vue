<script setup>
import { ref } from "vue";
import { addToLocalCart, addToUserCart } from "@/composables/useCart.js";
import {isAuthenticated} from "@/composables/useAuth.js";

const props = defineProps({
  productId: Number,
});

const size = ref("M");

async function addCart() {
  if (!props.productId) return;

  if (isAuthenticated.value) {
    const res = await addToUserCart(props.productId, size.value, 1);
    if (res.success) alert("Producto añadido al carrito (backend)");
    else alert("Error al añadir producto: " + res.error);

  } else {
    addToLocalCart(props.productId, size.value, 1);
    alert("Producto añadido al carrito (localStorage)");
  }
}
</script>

<template>
  <form @submit.prevent="addCart">
    <select v-model="size">
      <option>S</option>
      <option>M</option>
      <option>L</option>
      <option>XL</option>
    </select>
    <input type="submit" value="Add To Cart" />
  </form>
</template>
