<script setup>
import { getUserCart } from "@/composables/useCart.js";
import { onMounted, ref } from "vue";
import UpdateCart from "@/views/Cart/updateCart.vue";
import api from "@/composables/axios/interceptor.js";

const cart = ref([]);
const isLoading = ref(false);

onMounted(() => {
  getCart();
});

async function getCart() {
  isLoading.value = true;
  try {
    const response = await getUserCart();
    if (response.success) {
      cart.value = response.data;
    }
  } catch (err) {
    console.log("Error en la vista del carrito: " + err);
  } finally {
    isLoading.value = false;
  }
}

async function clearCompleteCart() {
  if (confirm("¿Estás seguro de que quieres vaciar todo el carrito?")) {
    try {
      const response = await api.delete("cart/clear/");
      if (response.status === 200) {
        await getCart();
      }
    } catch (err) {
      console.error("Error vaciando el carrito:", err);
      alert("Error al vaciar el carrito. Inténtalo de nuevo.");
    }
  }
}

function onCartUpdated() {
  getCart();
}
</script>

<template>
  <div class="cart-container">
    <div class="cart-header">
      <h2 class="cart-title">🛒 TU CARRITO DE COMPRAS</h2>
      <button
        v-if="cart.items && cart.items.length > 0"
        @click="clearCompleteCart"
        class="clear-cart-btn"
      >
        🗑️ Vaciar Carrito
      </button>
    </div>

    <div v-if="isLoading" class="loading">
      <p>Cargando carrito...</p>
    </div>

    <div v-else-if="!cart.items || cart.items.length === 0" class="empty-cart">
      <div class="empty-cart-icon">🛒</div>
      <h3>Tu carrito está vacío</h3>
      <p>¡Agrega algunos productos para comenzar!</p>
    </div>

    <div v-else class="cart-content">
      <div class="cart-items">
        <div
          v-for="item in cart.items"
          :key="`${item.id}-${item.size}`"
          class="cart-item"
        >
          <div class="item-image">
            <div class="product-placeholder">
              <img :src="`http://localhost:8000${item.image}`">
            </div>
          </div>

          <div class="item-details">
            <h3 class="product-name">{{ item.product_name }}</h3>
            <div class="product-info">
              <span class="size-badge">Talla: {{ item.size }}</span>
              <span
                class="price"
                :class="{ 'original-price': item.price_with_discount }"
              >
                €{{ item.product_price }}
              </span>
              <span v-if="item.price_with_discount" class="discounted-price">
                €{{ item.price_with_discount }}
              </span>
            </div>
            <div v-if="item.product_discount > 0" class="discount">
              <span class="discount-badge">-{{ item.product_discount }}%</span>
            </div>
          </div>

          <div class="item-actions">
            <UpdateCart
              :item="item"
              @cart-updated="onCartUpdated"
            />
          </div>

          <div class="item-total">
            <div class="units">{{ item.units }} unidades</div>
            <div v-if="item.total_price_with_discount" class="total-price discounted">
              <span class="original-total">€{{ item.total_price }}</span>
              <span class="final-total">€{{ item.total_price_with_discount }}</span>
            </div>
            <div v-else class="total-price">€{{ item.total_price }}</div>
          </div>
        </div>
      </div>

      <div class="cart-summary">
        <div class="summary-row">
          <span class="summary-label">Total de artículos:</span>
          <span class="summary-value">{{ cart.items.reduce((sum, item) => sum + item.units, 0) }}</span>
        </div>
        <div class="summary-row total-row">
          <span class="summary-label">TOTAL:</span>
          <span class="summary-total">€{{ cart.total }}</span>
        </div>
        <button class="checkout-btn">
          Proceder al Pago
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cart-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 3px solid #e1e5e9;
}

.cart-title {
  color: #2c3e50;
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
}

.clear-cart-btn {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.clear-cart-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 1.2rem;
  color: #7f8c8d;
}

.empty-cart {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-radius: 15px;
  margin: 20px 0;
}

.empty-cart-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-cart h3 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 1.5rem;
}

.empty-cart p {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.cart-content {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 30px;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cart-item {
  display: grid;
  grid-template-columns: 80px 1fr auto auto;
  gap: 20px;
  padding: 25px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.08);
  border: 1px solid #e1e5e9;
  transition: all 0.3s ease;
  align-items: center;
}

.cart-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.item-image {
  height: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-placeholder {
  width: 150px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  border-radius: 15px;
}

.product-placeholder img{
  width: 100%;
  height: auto;
  border-radius: 15px;
}

.item-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.product-name {
  font-size: 1.3rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0;
}

.product-info {
  display: flex;
  gap: 15px;
  align-items: center;
}

.size-badge {
  background: linear-gradient(135deg, #9b59b6, #8e44ad);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
}

.price {
  font-size: 1.1rem;
  font-weight: bold;
  color: #27ae60;
}

.price.original-price {
  color: #7f8c8d;
  text-decoration: line-through;
}

.discounted-price {
  font-size: 1.2rem;
  font-weight: bold;
  color: #27ae60;
}

.discount-badge {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

.item-total {
  text-align: right;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.units {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.total-price {
  font-size: 1.3rem;
  font-weight: bold;
  color: #2c3e50;
}

.total-price.discounted {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.original-total {
  font-size: 1rem;
  color: #7f8c8d;
  text-decoration: line-through;
}

.final-total {
  font-size: 1.3rem;
  color: #27ae60;
  font-weight: bold;
}

.cart-summary {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.08);
  border: 1px solid #e1e5e9;
  height: fit-content;
  position: sticky;
  top: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #ecf0f1;
}

.summary-row.total-row {
  border-bottom: none;
  border-top: 2px solid #3498db;
  margin-top: 15px;
  padding-top: 20px;
  font-size: 1.2rem;
}

.summary-label {
  color: #7f8c8d;
  font-weight: 500;
}

.summary-value {
  color: #2c3e50;
  font-weight: bold;
}

.summary-total {
  color: #e74c3c;
  font-weight: bold;
  font-size: 1.4rem;
}

.checkout-btn {
  width: 100%;
  background: linear-gradient(135deg, #27ae60, #2ecc71);
  color: white;
  border: none;
  padding: 15px;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.checkout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

@media (max-width: 768px) {
  .cart-content {
    grid-template-columns: 1fr;
  }

  .cart-item {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 15px;
  }

  .cart-header {
    flex-direction: column;
    gap: 15px;
  }
}
</style>