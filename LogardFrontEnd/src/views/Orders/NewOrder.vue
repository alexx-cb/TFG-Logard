<script setup>
import { onMounted, ref, computed } from "vue";
import { createOrder } from "@/composables/useOrders.js";
import { getUserCart } from "@/composables/useCart.js";

const address = ref('');
const locality = ref('');
const province = ref('');
const cart = ref({ items: [], total: 0 });
const approvalUrl = ref(null);
const errorMsg = ref('');

onMounted(() => {
  getCart();
});

async function getCart() {
  try {
    const response = await getUserCart();
    if (response.success) {
      cart.value = response.data;
    }
  } catch (err) {
    errorMsg.value = "Error al obtener el carrito: " + err;
  }
}

const total = computed(() => cart.value.total || 0);

async function submitOrder() {
  const response = await createOrder({
    address: address.value,
    locality: locality.value,
    province: province.value,
    cart_items: cart.value.items,
    payment_method_id: "paypal"
  });
  if (response.success) {
    approvalUrl.value = response.approval_url;
    window.location.href = approvalUrl.value;
  } else {
    errorMsg.value = "Error al crear el pedido: " + JSON.stringify(response.error);
  }
}
</script>

<template>
  <div class="checkout-container">
    <h2 class="checkout-title">Resumen del pedido</h2>
    <div v-if="cart.items.length === 0" class="empty-cart">
      <div class="empty-cart-icon">🛒</div>
      <h3>Your Cart is empty!</h3>
      <p>Add some products before you pay.</p>
    </div>
    <div v-else class="checkout-content">
      <ul class="checkout-items">
        <li v-for="item in cart.items" :key="item.id" class="checkout-item">
          <img :src="`https://logard-backed.up.railway.app${item.image}`" alt="" class="checkout-img" />
          <div class="checkout-details">
            <span class="checkout-product">{{ item.product_name }}</span>
            <span class="checkout-size">Size: {{ item.size }}</span>
            <span class="checkout-units">{{ item.units }} ud.</span>
          </div>
          <div class="checkout-prices">
            <span v-if="item.product_discount && item.product_discount !== '0.00'" class="original-price">
              <s>{{ item.product_price }}€</s>
            </span>
            <span v-if="item.product_discount && item.product_discount !== '0.00'" class="discounted-price">
              {{ item.price_with_discount }}€ c/u
            </span>
            <span v-else class="discounted-price">
              {{ item.product_price }}€ c/u
            </span>
            <span class="checkout-total">
              = <b>{{ item.total_price_with_discount ?? item.total_price }}€</b>
            </span>
          </div>
        </li>
      </ul>
      <div class="checkout-summary">
        <span class="summary-label">Total:</span>
        <span class="summary-total">{{ total }}€</span>
      </div>
      <form @submit.prevent="submitOrder" class="checkout-form">
        <input v-model="address" placeholder="Address" required />
        <input v-model="locality" placeholder="Locality" required />
        <input v-model="province" placeholder="Province" required />
        <button type="submit" class="checkout-btn">Pay with Paypal</button>
      </form>
      <div v-if="approvalUrl" class="paypal-redirect">
        <h3>Redirecting to PayPal...</h3>
        <a :href="approvalUrl" target="_blank">Click here if you didn't redirect</a>
      </div>
      <div v-if="errorMsg" class="checkout-error">
        {{ errorMsg }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.checkout-container {
  background: #000;
  color: #ffe600;
  min-height: 100vh;
  padding: 0;
  font-family: 'Arial', sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.checkout-title {
  font-size: 2rem;
  font-weight: bold;
  margin: 40px 0 24px 0;
  letter-spacing: 2px;
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

.checkout-content {
  width: 100%;
  max-width: 700px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 60px;
}

.checkout-items {
  list-style: none;
  padding: 0;
  margin: 0 0 20px 0;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.checkout-item {
  background: #181818;
  border-radius: 14px;
  box-shadow: 0 0 0 4px #ff0000, 0 0 16px 0 #ff0000 inset;
  padding: 18px 18px;
  display: flex;
  align-items: center;
  gap: 18px;
}

.checkout-img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 8px;
  background: #222;
}

.checkout-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.checkout-product {
  font-weight: bold;
  font-size: 1.05rem;
}

.checkout-size,
.checkout-units {
  font-size: 0.95rem;
}

.checkout-prices {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
  min-width: 120px;
}

.original-price {
  text-decoration: line-through;
  opacity: 0.7;
  color: #ffe600;
}

.discounted-price {
  color: #ffe600;
  font-size: 0.97rem;
  font-weight: bold;
}

a{
  color: #ffe600;
  font-size: 0.97rem;
}

.checkout-total {
  font-size: 1.05rem;
  font-weight: bold;
  color: #ffe600;
}

.checkout-summary {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  font-size: 1.2rem;
  margin-top: 12px;
}

.summary-label {
  font-weight: bold;
}

.summary-total {
  font-size: 1.35rem;
  font-weight: bold;
}

.checkout-form {
  display: flex;
  gap: 18px;
  margin-top: 18px;
  flex-wrap: wrap;
}

.checkout-form input {
  background: #222;
  color: #ffe600;
  border: 1px solid #ffe600;
  border-radius: 6px;
  padding: 8px 14px;
  font-size: 1rem;
  margin-bottom: 8px;
  outline: none;
  width: 180px;
}

.checkout-btn {
  background: #444;
  color: #ffe600;
  border: none;
  padding: 12px 36px;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.checkout-btn:hover {
  background: #222;
}

.paypal-redirect {
  margin-top: 24px;
  color: #ffe600;
  text-align: center;
}

.checkout-error {
  color: #ff3333;
  margin-top: 18px;
  font-weight: bold;
}

@media (max-width: 800px) {
  .checkout-content {
    max-width: 98vw;
    padding: 0 2vw;
  }
  .checkout-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  .checkout-form input {
    width: 100%;
  }
}
</style>
