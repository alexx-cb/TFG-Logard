<script setup>
import { deleteCategory, updateCategory } from "@/composables/useCategories.js";
import { ref } from "vue";

const props = defineProps({
  categoryId: Number
});
const emit = defineEmits(['category-updated']);

const name = ref('');

async function updateCategories() {
  try {
    const response = await updateCategory(props.categoryId, name.value);
    if (response.success) {
      alert("actualizada con exito");
      name.value = ''
      emit('category-updated');
    }
  } catch (err) {
    console.log(err);
  }
}

async function deleteCategories() {
  try {
    const response = await deleteCategory(props.categoryId);
    if (response.success) {
      emit('category-updated');
      alert("categoria eliminada correctamente");
    }
  } catch (err) {
    console.log("Error al eliminar: " + err);
  }
}
</script>

<template>
  <div class="category-row">
    <span class="category-id">Update Category</span>
    <form @submit.prevent="updateCategories" class="update-form">
      <input type="text" v-model="name" placeholder="Nuevo nombre" />
      <button type="submit">Actualizar</button>
    </form>
    <span class="category-id">Delete Category</span>
    <button @click="deleteCategories" class="delete-btn">
      Eliminar
    </button>
  </div>
</template>

<style scoped>
.category-row {
  width: 55%;
  display: flex;
  align-items: center;
  gap: 18px;
  color: #ffe600;
  padding: 16px 22px;
  border-radius: 10px;
  margin: 12px 0;
  font-family: 'Arial', sans-serif;
}

.category-id {
  font-weight: bold;
  margin-right: 12px;
}

.update-form {
  display: flex;
  align-items: center;
  gap: 8px;
}

.update-form input {
  background: #222;
  color: #ffe600;
  border: 1px solid #ffe600;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 1rem;
  outline: none;
}

.update-form button,
.delete-btn {
  background: #444;
  color: #ffe600;
  border: none;
  padding: 7px 18px;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.update-form button:hover,
.delete-btn:hover {
  background: #222;
  color: #ffe600;
}
</style>