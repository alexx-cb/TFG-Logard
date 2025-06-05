<script setup>

import {addToCart} from "@/composables/useCart.js";
import {ref} from "vue";

const props = defineProps({
  productId:Number,
})

const size = ref('')

async function addCart(){
  try{
    const response = await addToCart(props.productId, size.value)

    if(response.success){
      alert("Producto añadido al carrito correctamente")
      console.log(response.data.data)
    }

  }catch(err){
    console.log("Error añadiendo el producto: " +err)
  }
}
</script>

<template>



  <div>
    <form @submit.prevent="addCart">
      <input type="hidden" :value="productId" />

      <select v-model="size">
        <option>S</option>
        <option>M</option>
        <option>L</option>
        <option>XL</option>

      </select>

      <input type="submit" value="Add To Cart"/>
    </form>


  </div>
</template>

<style scoped>

</style>