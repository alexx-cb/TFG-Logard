<script setup>
//PRINCIPAL DE PRODUCTOS --> LISTAR TODOS SEGUN EL ID DE CATEGORIA QUE SE LE PASE

// SE LLAMA A:
// DETAIL -- > DATOS DEL PRODUCTO Y EDITAR LOS DATOS DE ESE PRODUCTO
// ADMINPRODUCT -- > CREAR UN NUEVO PRODUCTO (FORMULARIO)

import { user } from '@/composables/useAuth';
import router from '@/router';
import {ref} from "vue";
import CreateProduct from "@/views/Products/CreateProduct.vue";

defineProps({
  categoryId:Number
})

const showForm = ref(false);


function showFormCreate() {
  showForm.value = true
}

</script>

<template>

  <h1>Componente Productos</h1>
  <p>{{categoryId}}</p>

  <div>


  </div>

  <div v-if="user.is_staff">

      <!-- Button to share the create form-->
      <button
        @click="showFormCreate()"
      >Add Product</button>

    <CreateProduct
    v-if="showForm"
    :category-id="categoryId"
  />
  </div>
</template>

<style scoped>

</style>