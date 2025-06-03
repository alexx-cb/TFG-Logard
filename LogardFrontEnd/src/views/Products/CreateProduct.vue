<script setup>
// COMPONENTE PARA CREAR NUEVOS PRODUCTOS(FORMULARIO)

import { user } from '@/composables/useAuth';
import {computed, ref} from "vue";
import {postProduct} from "@/composables/useProducts.js";

const isAdmin = computed(()=> user.value?.is_staff)

const name = ref('')
const description = ref('')
const price = ref('')
const discount = ref('')
const image = ref(null)

const props = defineProps({
  categoryId: Number
})
const emit = defineEmits(['update-product'])

function imageContainer(event) {
  image.value = event.target.files[0]
}

async function createProduct(){
  const formData = new FormData()

  formData.append('name', name.value)
  formData.append('description', description.value)
  formData.append('price', price.value)
  formData.append('discount', discount.value)
  formData.append('image', image.value)
  formData.append('category', props.categoryId)


  try{
    const response = await postProduct(formData)
    if (response.success){
      emit('update-product')
      console.log("producto creado con exito")
    }else{
      console.log("Error en la respuesta")
      console.log(response)
    }
  }catch(err){
    console.log("Error al crear el producto: " + err)
  }
}

</script>

<template>

  <div v-if="isAdmin">
    <h1>Crear Productos</h1>

    {{categoryId}}

    <form @submit.prevent="createProduct(categoryId)">
      <label for="name">Name: </label>
      <input type="text" id="name" v-model="name"/>

      <label for="description">Description: </label>
      <input type="text" id="description" v-model="description"/>

      <label for="price">Price: </label>
      <input type="number" id="price" v-model="price">

      <label for="discount">Discount: </label>
      <input type="number" id="discount" v-model="discount"/>

      <label for="image">Image:</label>
      <input type="file" id="image" @change="imageContainer" />

      <input type="hidden" value={{categoryId}}  />

      <input type="submit" value="Create"/>
    </form>

  </div>

</template>

<style scoped>

</style>