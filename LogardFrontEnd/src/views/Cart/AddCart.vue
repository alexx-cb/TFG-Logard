<script setup>
import { ref } from "vue";
import { addToLocalCart, addToUserCart } from "@/composables/useCart.js";
import { isAuthenticated } from "@/composables/useAuth.js";

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
  <form @submit.prevent="addCart" class="add-cart-form">
    <select v-model="size" class="cart-select">
      <option>S</option>
      <option>M</option>
      <option>L</option>
      <option>XL</option>
    </select>
    <input type="submit" value="Añadir al carrito" class="cart-button" />
  </form>
</template>

<style scoped>
.add-cart-form {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.cart-select {
  background-color: #222;
  color: #ffd700;
  border: none;
  padding: 0.5rem 1rem;
  font-weight: bold;
  border-radius: 5px;
}

.cart-button {
  background-color: #444;
  color: #ffd700;
  border: none;
  padding: 0.5rem 1.2rem;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
}

.cart-button:hover {
  background-color: #666;
}
</style>
