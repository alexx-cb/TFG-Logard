<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const message = ref('Processing your order...')
const orderId = route.query.order_id
const orderData = ref(null)

onMounted(async () => {
  if (!orderId) {
    message.value = 'Not found the Order ID.'
    return
  }

  try {
    const response = await axios.get(`/api/orders/${orderId}`)
    orderData.value = response.data
    message.value = 'Your payment has been processed successfully!'
  } catch (error) {
    message.value = 'Your payment has been processed successfully!'
  }
})

function volverAlInicio() {
  router.push('/')
}
</script>

<template>
  <div class="verification-container">
    <div class="verification-box">
      <h2>Successful Payment</h2>
      <p>{{ message }}</p>
      <div v-if="orderData" class="order-details">
        <p><strong>Order Number:</strong> {{ orderData.id }}</p>
        <p><strong>Total Pay:</strong> €{{ orderData.cost }}</p>
      </div>
      <button @click="volverAlInicio" class="verification-button">
        Back to Home
      </button>
    </div>
  </div>
</template>

<style scoped>
.verification-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #000;
  color: #fff;
  width: 100vw;
  height: 100vh;
  font-family: 'Arial', sans-serif;
}

.verification-box {
  background-color: rgba(25, 25, 25, 0.95);
  border: 1px solid #333;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 0 10px #000;
  max-width: 400px;
  width: 90%;
}

.verification-box h2 {
  color: #00FF99;
  margin-bottom: 20px;
  font-size: 24px;
}

.verification-box p {
  margin-bottom: 10px;
  font-size: 16px;
}

.verification-button {
  background-color: #FFD700;
  border: none;
  padding: 10px 20px;
  color: #000;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 20px;
}

.verification-button:hover {
  background-color: #FFA500;
}

.order-details {
  margin-top: 15px;
  font-size: 14px;
  text-align: left;
}
</style>
