<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import {executePayPalPayment} from "@/composables/useOrders.js";

const route = useRoute();
const router = useRouter();

const status = ref(null);
const errorMsg = ref("");
const loading = ref(true);

onMounted(async () => {
  const paymentId = route.query.paymentId;
  const payerId = route.query.PayerID;
  const orderId = route.query.order_id;

  if (paymentId && payerId && orderId) {
    const result = await executePayPalPayment({ paymentId, payerId, orderId });
    loading.value = false;
    if (result.success) {
      status.value = result.data.status === "Pagado" ? "success" : result.data.status;
    } else {
      status.value = "error";
      errorMsg.value = result.error?.detail || result.error || "No se pudo confirmar el pago.";
    }
  } else {
    loading.value = false;
    status.value = "error";
    errorMsg.value = "Faltan parámetros en la URL de PayPal.";
  }
});
</script>
<template>
  <div class="paypal-callback">
    <h2>Procesando pago con PayPal...</h2>
    <div v-if="loading">Por favor, espera mientras confirmamos tu pago.</div>
    <div v-if="status === 'success'" class="success">
      <h3>¡Pago realizado con éxito!</h3>
      <p>Tu pedido ha sido confirmado. Revisa tu correo electrónico para más detalles.</p>
      <router-link to="/">Volver a la tienda</router-link>
    </div>
    <div v-if="status === 'cancelled'" class="cancelled">
      <h3>Pago cancelado</h3>
      <p>El pago no se ha completado. Puedes intentarlo de nuevo desde tu carrito.</p>
      <router-link to="/cart">Volver al carrito</router-link>
    </div>
    <div v-if="status === 'error'" class="error">
      <h3>Ocurrió un error</h3>
      <p>{{ errorMsg }}</p>
      <router-link to="/">Volver a la tienda</router-link>
    </div>
  </div>
</template>

<style scoped>
</style>
