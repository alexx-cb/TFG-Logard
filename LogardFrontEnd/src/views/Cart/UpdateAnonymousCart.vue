<script setup>
import { updateLocalCart, removeFromLocalCart } from "@/composables/useCart.js";
const props = defineProps(["item"]);
const emit = defineEmits(["cart-updated"]);

function increaseQuantity() {
  updateLocalCart(props.item.product, props.item.size, props.item.units + 1);
  emit("cart-updated");
}

function decreaseQuantity() {
  if (props.item.units > 1) {
    updateLocalCart(props.item.product, props.item.size, props.item.units - 1);
    emit("cart-updated");
  }
}

function removeItem() {
  removeFromLocalCart(props.item.product, props.item.size);
  emit("cart-updated");
}
</script>

<template>
  <div class="item-actions">
    <button @click="decreaseQuantity">-</button>
    <span>{{ props.item.units }}</span>
    <button @click="increaseQuantity">+</button>
    <button class="remove" @click="removeItem">Remove</button>
  </div>
</template>

<style scoped>
.item-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}

.item-actions button {
  background: none;
  border: none;
  color: #ffe600;
  font-size: 1.25rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.15s;
}

.item-actions button:not(.remove) {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  padding: 0;
  text-align: center;
}

.remove {
  width: auto;
  min-width: 80px;
  height: 32px;
  border-radius: 6px;
  padding: 0 18px;
  font-size: 1rem;
  background: none;
  color: #ffe600;
  transition: background 0.15s, color 0.15s;
}

.item-actions button:hover,
.remove:hover {
  background: #ffe600;
  color: #000;
}
</style>