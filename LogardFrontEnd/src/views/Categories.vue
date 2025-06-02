<script setup>
import {getCategories, postCategories} from "@/composables/useCategories";
import {ref, onMounted, computed} from "vue";
import {user} from "@/composables/useAuth.js";
import Products from "@/views/Products/Products.vue";

let categories = ref([])
let categoryName = ref('')

onMounted(()=>{
  getAllCategories()
})

const isAdmin = computed(() => user.value?.is_staff === true)

async function getAllCategories(){
  const response = await getCategories()
  console.log(response)

  if(response.success){
    categories.value = response.data.data
  }else{
    console.log("no ha llegado nada")
  }

}

async function createNewCategory(){
  const response = await postCategories(categoryName.value)
  console.log(response)

  if (response.success){
    console.log("Categoria creada correctamente")
    await getAllCategories()
  }else{
    console.log("Error al crear la categoria")
  }

}

</script>

<template>
  <h1>Categorias</h1>
  <div>
    <div v-for="category in categories" :key="category.id">
      <p>{{ category.name }}</p>
      <Products
        :category-id="category.id"
      ></Products>


    </div>


    <div v-if="isAdmin">
      <p>Eres admin</p>
      <h2>Crear nueva Categoria</h2>
      <form @submit.prevent="createNewCategory">
        <label for="name">Name: </label>
        <input type="text" id="name" v-model="categoryName">

        <button type="submit">Create</button>

      </form>
    </div>
    <div v-else>
      <p>no eres admin</p>
    </div>
  </div>
</template>

<style scoped>

</style>