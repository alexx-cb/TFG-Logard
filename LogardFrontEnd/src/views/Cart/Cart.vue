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

        <router-link to="/new-order">
          <button class="checkout-btn">
            Proceder al Pago
          </button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cart-container {
  background: #000;
  color: #ffe600;
  min-height: 100vh;
  padding: 0;
  font-family: 'Arial', sans-serif;
  position: relative;
  display: flex;
  flex-direction: column;
}

.cart-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 32px 0 0 80px;
  gap: 32px;
}

.cart-title {
  font-size: 1.6rem;
  font-weight: bold;
  letter-spacing: 2px;
  margin: 0;
}

.clear-cart-btn {
  background: none;
  border: none;
  color: #ffe600;
  font-size: 1.1rem;
  cursor: pointer;
  font-weight: bold;
  margin-left: 40px;
  position: absolute;
  top: 24px;
  right: 40px;
  z-index: 10;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 1.2rem;
  color: #ffe600;
}

.empty-cart {
  text-align: center;
  margin-top: 120px;
  color: #ffe600;
}

.empty-cart-icon {
  font-size: 4rem;
  margin-bottom: 24px;
}

.cart-content {
  display: flex;
  flex-direction: column;
  min-height: 60vh;
  justify-content: space-between;
  padding: 60px 80px 0 80px;
  height: 100%;
  flex: 1 1 auto;
}

.cart-items {
  display: flex;
  gap: 64px;
  flex-wrap: wrap;
}

.cart-item {
  background: none;
  border: none;
  padding: 0;
  width: 260px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: relative;
}

.item-image {
  width: 220px;
  height: 220px;
  background: #1a1a1a;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  margin-bottom: 12px;
  box-shadow: 0 0 0 4px #ff0000, 0 0 16px 0 #ff0000 inset;
}

.product-placeholder {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.product-placeholder img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.item-details {
  margin-bottom: 8px;
}

.product-name {
  font-size: 1.05rem;
  font-weight: bold;
  margin: 0 0 2px 0;
  color: #ffe600;
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 0.95rem;
}

.size-badge {
  color: #ffe600;
  font-size: 0.92rem;
}

.price {
  color: #ffe600;
  font-size: 0.92rem;
}

.price.original-price,
.original-total {
  text-decoration: line-through;
  opacity: 0.7;
  margin-right: 8px;
  color: #ffe600;
}

.discounted-price,
.final-total {
  color: #ffe600;
  font-size: 0.92rem;
  font-weight: bold;
}

.discount-badge {
  background: #e74c3c;
  color: #ffe600;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  margin-top: 4px;
  display: inline-block;
}

.item-total {
  margin-top: 8px;
  font-size: 0.95rem;
  color: #ffe600;
}

.units {
  font-size: 0.9rem;
}

.total-price {
  font-size: 1.05rem;
  font-weight: bold;
}

.total-price.discounted {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.cart-summary {
  background: none;
  color: #ffe600;
  min-width: 320px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-top: 48px;
  margin-bottom: 36px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
  font-size: 1.1rem;
  margin-bottom: 18px;
}

.total-row .summary-label {
  font-weight: bold;
  font-size: 1.2rem;
}

.summary-total {
  font-size: 1.35rem;
  font-weight: bold;
}

.checkout-btn {
  background: #444;
  color: #ffe600;
  border: none;
  padding: 12px 36px;
  font-size: 1.2rem;
  font-weight: bold;
  border-radius: 4px;
  margin-top: 24px;
  cursor: pointer;
  transition: background 0.2s;
}

.checkout-btn:hover {
  background: #222;
}

@media (max-width: 900px) {
  .cart-content {
    flex-direction: column;
    align-items: center;
    padding: 30px 10px 0 10px;
  }
  .cart-items {
    flex-direction: column;
    gap: 32px;
  }
  .cart-summary {
    align-items: center;
    min-width: unset;
    width: 100%;
    margin-top: 40px;
  }
}
</style>