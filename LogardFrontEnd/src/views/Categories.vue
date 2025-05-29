<script setup>
import { getCategories } from "@/composables/useCategories";
import {ref, onMounted} from "vue";

let categories = ref([])

async function getAllCategories(){
  const response = await getCategories()
  console.log(response)

  if(response.success){
    categories.value = response.response
  }else{
    console.log("no ha llegado nada")
  }

}
onMounted(()=>{
  getAllCategories()
})




</script>

<template>
  <h1>Categorias</h1>
  <div>
    <p>{{categories}}</p>
  </div>

  <div>
    <form >

    </form>
  </div>
</template>

<style scoped>

</style>