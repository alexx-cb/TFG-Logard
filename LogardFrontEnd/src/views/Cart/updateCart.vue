<script setup>
import { ref } from 'vue';
import api from "@/composables/axios/interceptor.js";

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['cart-updated']);

const isLoading = ref(false);
const message = ref('');

async function updateItemUnits(itemId, newUnits) {
  message.value = '';
  isLoading.value = true;
  try {
    const response = await api.patch(`cart/update/${itemId}/`, { units: newUnits });
    if (response.status === 200) {
      emit('cart-updated');
    }
  } catch (err) {
    message.value = "Error updating the units of the product"
  } finally {
    isLoading.value = false;
  }
}

async function addOneUnit() {
  const newUnits = props.item.units + 1;
  await updateItemUnits(props.item.id, newUnits);
}

async function removeOneUnit() {
  if (props.item.units > 1) {
    const newUnits = props.item.units - 1;
    await updateItemUnits(props.item.id, newUnits);
  }
}

async function removeItem() {
  if (confirm(`Are you sure you want to delete the product "${props.item.product_name}" (${props.item.size}) form the cart?`)) {
    message.value = '';
    isLoading.value = true;
    try {
      const response = await api.delete(`cart/update/${props.item.id}/`);
      if (response.status === 204) {
        emit('cart-updated');
      }
    } catch (err) {
      message.value = "Error deleting the product"
    } finally {
      isLoading.value = false;
    }
  }
}
</script>

<template>
  <div class="item-actions-container">
    <div class="item-actions">
      <button @click="removeOneUnit" :disabled="item.units <= 1 || isLoading" class="quantity-btn">-</button>
      <span class="quantity-display">{{ item.units }}</span>
      <button @click="addOneUnit" :disabled="isLoading" class="quantity-btn">+</button>
      <button @click="removeItem" :disabled="isLoading" class="remove">
        <span v-if="isLoading">⏳</span>
        <span v-else>Remove</span>
      </button>
    </div>

    <div v-if="message" class="message-box">
      {{ message }}
    </div>
  </div>
</template>

<style scoped>
.item-actions-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}

.quantity-btn {
  background: none;
  border: none;
  color: #ffe600;
  font-size: 1.25rem;
  font-weight: bold;
  cursor: pointer;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  transition: background 0.15s;
  text-align: center;
}

.quantity-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-btn:hover:not(:disabled) {
  background: #ffe600;
  color: #000;
}

.quantity-display {
  font-size: 1.1rem;
  font-weight: bold;
  color: #ffe600;
  min-width: 30px;
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
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.remove:hover:not(:disabled) {
  background: #ffe600;
  color: #000;
}

.remove:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.message-box {
  background: #181818;
  border: 1px solid #ffe600;
  border-radius: 6px;
  padding: 8px 12px;
  color: #ffe600;
  text-align: center;
  font-size: 0.85rem;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(255, 230, 0, 0.1);
  max-width: 250px;
}
</style>