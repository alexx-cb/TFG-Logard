<script setup>
//PRINCIPAL DE PRODUCTOS --> LISTAR TODOS SEGUN EL ID DE CATEGORIA QUE SE LE PASE

// SE LLAMA A:
// DETAIL -- > DATOS DEL PRODUCTO Y EDITAR LOS DATOS DE ESE PRODUCTO
// ADMINPRODUCT -- > CREAR UN NUEVO PRODUCTO (FORMULARIO)

import { user } from '@/composables/useAuth';
import {computed, ref} from "vue";
import CreateProduct from "@/views/Products/CreateProduct.vue";

defineProps({
  categoryId:Number
})

const showForm = ref(false);
const isAdmin = computed(()=>user.value?.is_staff)


function showFormCreate() {
  showForm.value = true
}

</script>

<template>

  <h1>Componente Productos</h1>
  <p>{{categoryId}}</p>

  <div>


  </div>

  <div v-if="isAdmin">

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