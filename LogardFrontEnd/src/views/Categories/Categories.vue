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
  <div class="categories-container">
    <div v-if="isUserLoaded && isAdmin" class="create-category-section">
      <div class="create-category-form">
        <h3>New Category</h3>
        <form @submit.prevent="createNewCategory" class="form-container">
          <div class="input-group">
            <input
              type="text"
              id="name"
              v-model="categoryName"
              placeholder="Category name"
              class="form-input"
            />
            <button type="submit" class="submit-btn">
              <span>→</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Categories sections -->
    <div v-for="category in categories" :key="category.id" class="category-section">
      <div class="category-header">
        <h2 class="category-title">{{ category.name }}</h2>
      </div>

      <Products :category-id="category.id" />

      <div v-if="isAdmin" class="admin-controls">
        <UpdateDeleteCategories
          :category-id="category.id"
          @category-updated="getAllCategories"
        />
      </div>
      <hr class="divider" />
    </div>
  </div>
</template>

<style scoped>
.divider{
  border: none;
  border-bottom: 1px solid #ffd700;
  margin: 0;
  width: 100%;
  box-shadow: 0 1px 8px #111a;
}

.categories-container {
  background-color: #000;
  color: #fff;
  min-height: 100vh;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

.category-section {
  margin-bottom: 60px;
}

.category-header {
  margin-bottom: 30px;
}

.category-title {
  color: #FFD700;
  font-size: 32px;
  font-weight: bold;
  margin: 0;
  text-transform: capitalize;
}

.admin-controls {
  margin-top: 20px;
}

.create-category-section {
  margin-bottom: 50px;
}

.create-category-form {
  width: 30%;
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(25, 25, 25, 0.9);
  border: 1px solid #444;
  border-radius: 12px;
  padding: 10px 16px;
  font-family: 'Arial', sans-serif;
  color: #fff;
}

.create-category-form h3 {
  color: #FFD700;
  font-size: 16px;
  font-weight: bold;
  margin: 0;
  white-space: nowrap;
}

.form-container {
  flex: 1;
}

.input-group {
  display: flex;
  align-items: center;
  background: #333;
  border-radius: 25px;
  padding: 4px 8px;
  gap: 8px;
  width: 100%;
}

.form-input {
  background: transparent;
  border: none;
  color: #fff;
  padding: 8px 10px;
  font-size: 14px;
  outline: none;
  flex: 1;
}

.submit-btn {
  background: #FFD700;
  border: none;
  color: #000;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background: #FFA500;
}
/* Responsive */
@media (max-width: 768px) {
  .categories-container {
    padding: 10px;
  }

  .create-category-section {
    margin-bottom: 30px;
    padding: 20px 0;
  }

  .create-category-form {
    padding: 20px;
  }

  .input-group {
    min-width: 300px;
  }

  .category-title {
    font-size: 24px;
  }

  .filters-nav {
    flex-wrap: wrap;
    gap: 10px;
  }
}

@media (max-width: 480px) {
  .input-group {
    min-width: 250px;
  }

  .create-category-form h3 {
    font-size: 20px;
  }
}
</style>