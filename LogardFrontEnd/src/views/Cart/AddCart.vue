<script setup>
import { ref } from "vue";
import { addToLocalCart, addToUserCart } from "@/composables/useCart.js";
import { isAuthenticated } from "@/composables/useAuth.js";

const props = defineProps({
  productId: Number,
});

const size = ref("M");
const message = ref('')

async function addCart() {
  message.value = ''

  if (!props.productId) return;

  if (isAuthenticated.value) {
    const res = await addToUserCart(props.productId, size.value, 1);
    if (res.success){
      message.value = 'Product added to cart'
    }
    else{
      message.value = 'Error adding the product to the cart'
    }
  } else {
    addToLocalCart(props.productId, size.value, 1);
    message.value = 'Product added to cart'
  }
}
</script>

<template>
  <div class="add-cart-container">
    <form @submit.prevent="addCart" class="add-cart-form">
      <select v-model="size" class="cart-select">
        <option>S</option>
        <option>M</option>
        <option>L</option>
        <option>XL</option>
      </select>
      <input type="submit" value="Añadir al carrito" class="cart-button" />
    </form>

    <div v-if="message" class="message-box">
      {{ message }}
    </div>
  </div>
</template>

<style scoped>
.add-cart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

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

.message-box {
  background: #181818;
  border: 1px solid #ffd700;
  border-radius: 5px;
  padding: 0.75rem 1rem;
  color: #ffd700;
  text-align: center;
  font-size: 0.9rem;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.1);
  min-width: 200px;
}
</style>