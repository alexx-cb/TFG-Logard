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

async function updateItemUnits(itemId, newUnits) {
  isLoading.value = true;
  try {
    const response = await api.patch(`cart/update/${itemId}/`, { units: newUnits });
    if (response.status === 200) {
      emit('cart-updated');
    }
  } catch (err) {
    console.error("Error actualizando unidades:", err);
    alert("Error al actualizar las unidades. Inténtalo de nuevo.");
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
  if (confirm(`¿Estás seguro de que quieres eliminar "${props.item.product_name}" (${props.item.size}) del carrito?`)) {
    isLoading.value = true;
    try {
      const response = await api.delete(`cart/update/${props.item.id}/`);
      if (response.status === 204) {
        emit('cart-updated');
      }
    } catch (err) {
      console.error("Error eliminando item:", err);
      alert("Error al eliminar el producto. Inténtalo de nuevo.");
    } finally {
      isLoading.value = false;
    }
  }
}
</script>

<template>
  <div class="item-actions">
    <button @click="removeOneUnit" :disabled="item.units <= 1 || isLoading" class="quantity-btn">-</button>
    <span class="quantity-display">{{ item.units }}</span>
    <button @click="addOneUnit" :disabled="isLoading" class="quantity-btn">+</button>
    <button @click="removeItem" :disabled="isLoading" class="remove">
      <span v-if="isLoading">⏳</span>
      <span v-else>Remove</span>
    </button>
  </div>
</template>

<style scoped>
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

</style>