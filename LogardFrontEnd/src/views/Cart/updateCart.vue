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
  <div class="update-cart-container">
    <div class="quantity-controls">
      <button
        @click="removeOneUnit"
        :disabled="item.units <= 1 || isLoading"
        class="quantity-btn decrease"
        :class="{ disabled: item.units <= 1 }"
      >
        ➖
      </button>

      <span class="quantity-display">{{ item.units }}</span>

      <button
        @click="addOneUnit"
        :disabled="isLoading"
        class="quantity-btn increase"
      >
        ➕
      </button>
    </div>

    <button
      @click="removeItem"
      :disabled="isLoading"
      class="remove-btn"
      title="Eliminar producto del carrito"
    >
      <span v-if="isLoading" class="loading-spinner">⏳</span>
      <span v-else>🗑️</span>
    </button>
  </div>
</template>

<style scoped>
.update-cart-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: center;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #f8f9fa;
  padding: 8px 15px;
  border-radius: 25px;
  border: 2px solid #e9ecef;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.quantity-btn {
  width: 35px;
  height: 35px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.quantity-btn.decrease {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
}

.quantity-btn.decrease:hover:not(.disabled) {
  background: linear-gradient(135deg, #c0392b, #a93226);
  transform: scale(1.1);
}

.quantity-btn.increase {
  background: linear-gradient(135deg, #27ae60, #2ecc71);
  color: white;
}

.quantity-btn.increase:hover:not(:disabled) {
  background: linear-gradient(135deg, #2ecc71, #58d68d);
  transform: scale(1.1);
}

.quantity-btn.disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  opacity: 0.6;
}

.quantity-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.quantity-display {
  font-size: 1.2rem;
  font-weight: bold;
  color: #2c3e50;
  min-width: 30px;
  text-align: center;
  padding: 5px 10px;
  background: white;
  border-radius: 15px;
  border: 1px solid #ddd;
}

.remove-btn {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 6px rgba(0,0,0,0.1);
}

.remove-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #c0392b, #a93226);
  transform: scale(1.1) rotate(5deg);
}

.remove-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .update-cart-container {
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
  }

  .quantity-controls {
    flex: 1;
    justify-content: center;
    margin-right: 10px;
  }
}
</style>