<script setup>
import { onMounted, ref } from "vue";
import { getUserOrders } from "@/composables/useOrders.js";

const orders = ref([]);

onMounted(() => {
  getOrders();
});

async function getOrders() {
  try {
    const response = await getUserOrders();
    orders.value = response.data;
  } catch (err) {
    console.log("Error en la vista: " + err);
  }
}
</script>

<template>
  <div class="orders-container">
    <h1 class="orders-title">Mis Pedidos</h1>
    <div v-if="orders.length === 0" class="empty-orders">
      <div class="empty-orders-icon">📦</div>
      <h3>No hay pedidos aún</h3>
      <p>Cuando realices un pedido aparecerá aquí.</p>
    </div>
    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-header">
          <span class="order-id">#{{ order.id }}</span>
          <span class="order-date">{{ order.date }}</span>
        </div>
        <div class="order-user">
          <span class="user-label">Usuario:</span>
          <span class="user-email">{{ order.user_email }}</span>
        </div>
        <div class="order-address">
          <span class="address-label">Dirección:</span> {{ order.address }},
          <span class="locality-label">Localidad:</span> {{ order.locality }}
        </div>
        <div class="order-items">
          <div
            v-for="item in order.items"
            :key="item.id"
            class="order-item"
          >
            <span class="product-name">{{ item.product_name }}</span>
            <span class="product-units">{{ item.units }} ud.</span>
            <span class="product-size">Talla: {{ item.size }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.orders-container {
  background: #000;
  color: #ffe600;
  min-height: 100vh;
  padding: 0;
  font-family: 'Arial', sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.orders-title {
  font-size: 2rem;
  font-weight: bold;
  margin: 40px 0 24px 0;
  letter-spacing: 2px;
}

.empty-orders {
  text-align: center;
  margin-top: 120px;
  color: #ffe600;
}

.empty-orders-icon {
  font-size: 4rem;
  margin-bottom: 24px;
}

.orders-list {
  width: 100%;
  max-width: 700px;
  display: flex;
  flex-direction: column;
  gap: 36px;
  margin-bottom: 60px;
}

.order-card {
  background: #181818;
  border-radius: 14px;
  box-shadow: 0 0 0 4px #ff0000, 0 0 16px 0 #ff0000 inset;
  padding: 32px 28px 18px 28px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  position: relative;
}

.order-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 18px;
  margin-bottom: 8px;
}

.order-id {
  font-size: 1.1rem;
  font-weight: bold;
  background: #ffe600;
  color: #181818;
  border-radius: 8px;
  padding: 2px 12px;
  margin-right: 12px;
}

.order-date {
  font-size: 1rem;
  color: #ffe600;
  opacity: 0.8;
}

.order-user, .order-address {
  font-size: 1rem;
  margin-bottom: 2px;
}

.user-label, .address-label, .locality-label {
  font-weight: bold;
  color: #ffe600;
  margin-right: 4px;
}

.user-email {
  font-size: 0.95rem;
  color: #ffe600;
  opacity: 0.8;
  margin-left: 8px;
}

.order-items {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.order-item {
  background: #222;
  color: #ffe600;
  border-radius: 8px;
  padding: 10px 18px;
  display: flex;
  align-items: center;
  gap: 24px;
  font-size: 1rem;
  font-weight: 500;
}

.product-name {
  font-weight: bold;
  font-size: 1.05rem;
}

.product-units, .product-size {
  font-size: 0.98rem;
}

@media (max-width: 800px) {
  .orders-list {
    max-width: 98vw;
    padding: 0 2vw;
  }
  .order-card {
    padding: 22px 8px 10px 8px;
  }
}
</style>