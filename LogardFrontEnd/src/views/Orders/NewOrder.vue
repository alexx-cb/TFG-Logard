<script setup>
import { onMounted, ref, computed } from "vue";
import { createOrder } from "@/composables/useOrders.js";
import { getUserCart } from "@/composables/useCart.js";

const address = ref('');
const locality = ref('');
const province = ref('');
const cart = ref({ items: [], total: 0 }); // Inicializamos con la estructura correcta
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
    cart_items: cart.value.items
  });
  if (response.success) {
    approvalUrl.value = response.approval_url;
    window.location.href = approvalUrl.value;
  } else {
    errorMsg.value = "Error al crear el pedido: " + (response.error?.detail || response.error || "Desconocido");
  }
}
</script>

<template>
  <div>
    <h2>Resumen del pedido</h2>
    <ul>
      <li v-for="item in cart.items" :key="item.id">
        <img :src="item.image" alt="" style="width: 40px; vertical-align: middle; margin-right: 8px;">
        {{ item.product_name }} ({{ item.size }}) x {{ item.units }}
        <span v-if="item.product_discount && item.product_discount !== '0.00'">
          - <s>{{ item.product_price }}€</s> <b>{{ item.price_with_discount }}€</b> c/u
        </span>
        <span v-else>
          - {{ item.product_price }}€
        </span>
        = <b>{{ item.total_price_with_discount ?? item.total_price }}€</b>
      </li>
    </ul>
    <p><b>Total: {{ total }}€</b></p>

    <form @submit.prevent="submitOrder">
      <input v-model="address" placeholder="Dirección" required />
      <input v-model="locality" placeholder="Localidad" required />
      <input v-model="province" placeholder="Provincia" required />
      <button type="submit">Pagar con PayPal</button>
    </form>

    <div v-if="approvalUrl">
      <h3>Redirigiendo a PayPal...</h3>
      <a :href="approvalUrl" target="_blank">Haz clic aquí si no eres redirigido</a>
    </div>
    <div v-if="errorMsg" style="color: red;">
      {{ errorMsg }}
    </div>
  </div>
</template>
