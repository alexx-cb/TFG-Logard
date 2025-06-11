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
    <!-- Admin section for creating new category -->
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
    </div>
  </div>
</template>

<style scoped>
.categories-container {
  background-color: #000;
  color: #fff;
  min-height: 100vh;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

.filters-nav {
  display: flex;
  gap: 20px;
  margin-bottom: 40px;
  padding: 20px 0;
}

.filter-btn {
  background: transparent;
  border: none;
  color: #888;
  font-size: 16px;
  cursor: pointer;
  padding: 10px 0;
  transition: color 0.3s ease;
}

.filter-btn.active,
.filter-btn:hover {
  color: #FFD700;
  border-bottom: 2px solid #FFD700;
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
  padding: 30px 0;
  border-bottom: 1px solid #333;
}

.create-category-form {
  background: rgba(25, 25, 25, 0.9);
  border: 1px solid #444;
  border-radius: 15px;
  padding: 30px;
  max-width: 600px;
  margin: 0 auto;
}

.create-category-form h3 {
  color: #FFD700;
  margin-bottom: 20px;
  font-size: 24px;
  text-align: center;
}

.form-container {
  display: flex;
  justify-content: center;
}

.input-group {
  display: flex;
  align-items: center;
  background: #333;
  border-radius: 25px;
  padding: 8px;
  gap: 10px;
  min-width: 400px;
}

.form-input {
  background: transparent;
  border: none;
  color: #fff;
  padding: 12px 20px;
  font-size: 16px;
  outline: none;
  flex: 1;
}

.form-input::placeholder {
  color: #888;
}

.submit-btn {
  background: #FFD700;
  border: none;
  color: #000;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
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