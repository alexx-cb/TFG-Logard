<script setup>
//PRINCIPAL DE PRODUCTOS --> LISTAR TODOS SEGUN EL ID DE CATEGORIA QUE SE LE PASE

// SE LLAMA A:
// DETAIL -- > DATOS DEL PRODUCTO Y EDITAR LOS DATOS DE ESE PRODUCTO
// ADMINPRODUCT -- > CREAR UN NUEVO PRODUCTO (FORMULARIO)

import { user } from '@/composables/useAuth';
import {computed, defineAsyncComponent, onMounted, ref} from "vue";;
import { getProductsCategory} from "@/composables/useProducts.js";


const CreateProductAsync = defineAsyncComponent(() => import('@/views/Products/CreateProduct.vue'))
const props = defineProps({
  categoryId:Number
})

onMounted(()=>{
  getProductsCategoryView()
})

const showForm = ref(false);
const isAdmin = computed(()=>user.value?.is_staff)

const products = ref([])

async function getProductsCategoryView(){
  try {
    const response = await getProductsCategory(props.categoryId)
    if (response.success){
      products.value = response.data.data
    }else{
      console.log("Error en la vista: "+ response)
    }

  }catch (err){
    console.log("Error en el get de productos: " + err)

  }
}

</script>

<template>

  <h1>Componente Productos</h1>
  <p>{{categoryId}}</p>

  <div v-for="product in products" :key="product.id">
    <p>{{ product.name }}</p>
    <img :src="`http://localhost:8000${product.image}`" :alt="product.name" />
  </div>

  <div v-if="isAdmin">
    <button @click="showForm = true">Add Product</button>
    <component :is="showForm ? CreateProductAsync : null" @update-product="getProductsCategoryView" :category-id="categoryId" />
  </div>
</template>

<style scoped>

</style>