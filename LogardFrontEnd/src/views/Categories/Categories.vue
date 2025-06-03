<script setup>
import {getCategories, postCategories} from "@/composables/useCategories.js";
import {ref, onMounted, computed, watch} from "vue";
import {user} from "@/composables/useAuth.js";
import Products from "@/views/Products/Products.vue";
import UpdateDeleteCategories from "@/views/Categories/UpdateDeleteCategories.vue";

let categories = ref([])
let categoryName = ref('')
let isUserLoaded = ref(false)

onMounted(()=>{
  getAllCategories()
})

watch(user, (newUser) => {
  if (newUser) {
    isUserLoaded.value = true
  }
}, { immediate: true })

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
    categoryName.value =''
    await getAllCategories()
  }else{
    console.log("Error al crear la categoria")
  }

}

</script>

<template>
  <h1>Categorias</h1>

  <!-- Mostrar siempre las categorías -->
  <div v-for="category in categories" :key="category.id">
    <p>NOMBRE CATEGORIA:  {{ category.name }}</p>
    <Products :category-id="category.id" />

    <div v-if="isAdmin">
      <UpdateDeleteCategories
          :category-id="category.id"
          @category-updated="getAllCategories"
      />
    </div>
  </div>

  <!-- Mostrar contenido según rol -->
  <div v-if="isUserLoaded">
    <div v-if="isAdmin">
      <p>Eres admin</p>
      <h2>Crear nueva Categoria</h2>
      <form @submit.prevent="createNewCategory">
        <label for="name">Name: </label>
        <input type="text" id="name" v-model="categoryName" />
        <button type="submit">Create</button>
      </form>
    </div>
    <div v-else>
      <p>No eres admin</p>
    </div>
  </div>
  <div v-else>
    <p>Cargando usuario...</p>
  </div>
</template>


<style scoped>

</style>