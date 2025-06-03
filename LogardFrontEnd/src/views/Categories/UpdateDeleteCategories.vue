<script setup>

import {deleteCategory, updateCategory} from "@/composables/useCategories.js";
import {ref} from "vue";

const props = defineProps({
    categoryId: Number
})
const emit = defineEmits(['category-updated'])

const name = ref('')


async function updateCategories(){
    try{
        const response = await updateCategory(props.categoryId, name.value)
        if (response.success){
            alert("actualizada con exito")
            emit('category-updated')
        }
    }catch (err){
        console.log(err)
    }
}

async function deleteCategories(){
    try{
        const response = await deleteCategory(props.categoryId)
        if (response.success){
          emit('category-updated')
          alert("categoria eliminada correctamente")
        }
    }catch (err){
        console.log("Error al eliminar: " +err)
    }
}
</script>

<template>
  <h1>Update Delete Categories</h1>
  <p>{{categoryId}}</p>

  <div>
    <h4>Actualizar</h4>
    <form @submit.prevent="updateCategories">
      <label for="name">Name: </label>
      <input type="text" v-model="name" id="name"/>
      <input type="submit" value="Update"/>
    </form>
  </div>

  <div>
    <h4 @click="deleteCategories">Pulsa aqui para 'Eliminar'</h4>
  </div>



</template>

<style scoped>

</style>