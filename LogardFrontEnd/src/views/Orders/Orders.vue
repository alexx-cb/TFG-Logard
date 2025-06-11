<script setup>
import {onMounted, ref} from "vue";
import {getUserOrders} from "@/composables/useOrders.js";

const orders = ref('')

onMounted(()=>{
  getOrders()
})

async function getOrders(){
  try{
    const response = await getUserOrders()
    orders.value= response.data
  }catch (err){
    console.log("Error en la vista: "+err)
  }
}

</script>

<template>
  <h1>Orders</h1>

  {{orders}}

</template>

<style scoped>

</style>