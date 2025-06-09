<script setup>
import {getUserCart} from "@/composables/useCart.js";
import {onMounted, ref} from "vue";

const cart = ref([])

onMounted(()=>{
  getCart()
})

async function getCart(){
  try{
    const response = await getUserCart()
    if (response.success){
      cart.value = response.data
    }
  }catch(err){
    console.log("Error en la vista del carrito: "+err)
  }
}


</script>

<template>

  <p>ESTE ES TU CARRITO</p>
  <p>{{cart}}</p>


</template>

<style scoped>

</style>