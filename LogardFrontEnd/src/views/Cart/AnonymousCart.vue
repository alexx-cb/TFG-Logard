<script setup>
import { ref, onMounted } from "vue";
import { getLocalCartWithDetails, clearLocalCart } from "@/composables/useCart.js";
import UpdateAnonymousCart from "@/views/Cart/UpdateAnonymousCart.vue";
import "./Cart.vue";

const cartItems = ref([]);

async function loadCart() {
  cartItems.value = await getLocalCartWithDetails();
}

onMounted(loadCart);

function handleCartUpdate() {
  loadCart();
}

function clearCart() {
  if (confirm("¿Vaciar el carrito completamente?")) {
    clearLocalCart();
    loadCart();
  }
}
</script>

<template>
  <div class="cart-container">
    <div class="cart-header">
      <h2 class="cart-title">🛒Cart</h2>
      <button v-if="cartItems.length > 0" @click="clearCart" class="clear-cart-btn">
        🗑️ Clear Cart
      </button>
    </div>

    <div v-if="cartItems.length === 0" class="empty-cart">
      <div class="empty-cart-icon">🛒</div>
      <h3>Your cart is empty</h3>
      <p>Add some products to start!</p>
    </div>

    <div v-else class="cart-content">
      <div class="cart-items">
        <div v-for="item in cartItems" :key="`${item.product}-${item.size}`" class="cart-item">
          <div class="item-image">
            <img :src="`https://logard-backed.up.railway.app${item.product_info.image}`" class="product-placeholder" />
          </div>

          <div class="item-details">
            <h3 class="product-name">{{ item.product_info.name }}</h3>
            <div class="product-info">
              <span class="size-badge">Size: {{ item.size }}</span>
              <span
                class="price"
                :class="{ 'strikethrough': item.product_info.discount > 0 }"
              >
                €{{ item.product_info.price }}
              </span>
              <span
                v-if="item.product_info.discount > 0"
                class="discounted-price"
              >
                €{{ (item.product_info.price * (1 - item.product_info.discount / 100)).toFixed(2) }}
              </span>
            </div>
          </div>

          <UpdateAnonymousCart :item="item" @cart-updated="handleCartUpdate" />

          <div class="item-total">
            <div class="units">{{ item.units }} units</div>
              <div class="total-price">
                €{{ (item.product_info.price * (1 - item.product_info.discount / 100) * item.units).toFixed(2) }}
              </div>
          </div>
        </div>
      </div>

      <div class="cart-summary">
        <div class="summary-row">
          <span class="summary-label">Total products:</span>
          <span class="summary-value">{{ cartItems.reduce((sum, item) => sum + item.units, 0) }}</span>
        </div>
        <div class="summary-row total-row">
          <span class="summary-label">TOTAL:</span>
            <span class="summary-total">
              €{{
                cartItems.reduce(
                  (sum, item) =>
                    sum +
                    item.product_info.price *
                      (1 - item.product_info.discount / 100) *
                      item.units,
                  0
                ).toFixed(2)
              }}
            </span>
        </div>

        <router-link to="/login">
          <button class="checkout-btn">Login to purchase</button>
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

.price,
.discounted-price {
  color: #ffe600;
  font-size: 0.92rem;
}
.price.strikethrough {
  text-decoration: line-through;
  opacity: 0.7;
  margin-right: 8px;
}

.discounted-price {
  color: #ffe600;
  font-size: 0.92rem;
  font-weight: bold;
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
