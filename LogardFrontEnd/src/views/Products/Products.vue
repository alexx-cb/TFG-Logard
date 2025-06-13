<script setup>
import { user } from '@/composables/useAuth';
import {computed, defineAsyncComponent, onMounted, ref} from "vue";
import { getProductsCategory} from "@/composables/useProducts.js";

const CreateProductAsync = defineAsyncComponent(() => import('@/views/Products/CreateProduct.vue'))
const props = defineProps({
  categoryId:Number
})

onMounted(()=>{
  getProductsCategoryView()
})

const showForm = ref(false);
const isAdmin = computed(()=>user.value?.is_staff)
const products = ref([])
const currentSlide = ref(0)

async function getProductsCategoryView(){
  try {
    const response = await getProductsCategory(props.categoryId)
    if (response.success){
      products.value = response.data.data
    }
  }catch (err){
   }
}

// Carrusel functions
const itemsPerPage = 3
const totalSlides = computed(() => Math.ceil(products.value.length / itemsPerPage))
const canGoPrev = computed(() => currentSlide.value > 0)
const canGoNext = computed(() => currentSlide.value < totalSlides.value - 1)

const visibleProducts = computed(() => {
  const start = currentSlide.value * itemsPerPage
  const end = start + itemsPerPage
  return products.value.slice(start, end)
})

function nextSlide() {
  if (canGoNext.value) {
    currentSlide.value++
  }
}

function prevSlide() {
  if (canGoPrev.value) {
    currentSlide.value--
  }
}

function toggleForm() {
  showForm.value = !showForm.value
}
</script>

<template>
  <div class="products-section">
    <!-- Products carousel -->
    <div class="carousel-container" v-if="products.length > 0">
      <button
        class="carousel-btn prev"
        @click="prevSlide"
        :disabled="!canGoPrev"
        v-show="products.length > itemsPerPage"
      >
        ←
      </button>

      <div class="products-grid">
        <router-link
          v-for="product in visibleProducts"
          :to="`/detail-product/${product.id}`"
          :key="product.id"
          class="product-card"
        >
          <div class="product-image-container">
            <img
              :src="`https://logard-backed.up.railway.app${product.image}`"
              :alt="product.name"
              class="product-image"
            />
          </div>
          <div class="product-info">
            <h3 class="product-name">{{ product.name }}</h3>
          </div>
        </router-link>
      </div>

      <button
        class="carousel-btn next"
        @click="nextSlide"
        :disabled="!canGoNext"
        v-show="products.length > itemsPerPage"
      >
        →
      </button>
    </div>

    <!-- Add new product form -->
    <div v-if="isAdmin" class="admin-add-section">
      <div class="add-product-form" :class="{ 'active': showForm }">
        <div class="form-header" @click="toggleForm">
          <span class="form-title">Add new Clothes</span>
          <button class="toggle-btn">→</button>
        </div>

        <div class="form-content" v-show="showForm">
          <component
            :is="CreateProductAsync"
            @update-product="getProductsCategoryView"
            :category-id="categoryId"
            @close-form="showForm = false"
          />
        </div>
      </div>
    </div>

    <!-- Carousel indicators -->
    <div class="carousel-indicators" v-if="products.length > itemsPerPage">
      <button
        v-for="slide in totalSlides"
        :key="slide"
        class="indicator"
        :class="{ active: currentSlide === slide - 1 }"
        @click="currentSlide = slide - 1"
      ></button>
    </div>
  </div>
</template>

<style scoped>
.products-section {
  margin-bottom: 40px;
}

.carousel-container {
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
  margin-bottom: 20px;
}

.carousel-btn {
  background: rgba(255, 215, 0, 0.8);
  border: none;
  color: #000;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 2;
}

.carousel-btn:hover:not(:disabled) {
  background: #FFD700;
  transform: scale(1.1);
}

.carousel-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  flex: 1;
  min-height: 300px;
}

.product-card {
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s ease;
}

.product-card:hover {
  transform: translateY(-10px);
}

.product-image-container {
  position: relative;
  background: none;
  border-radius: 15px;
  overflow: hidden;
  margin-bottom: 15px;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.product-info {
  text-align: left;
}

.product-name {
  color: #FFD700;
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 5px 0;
}

.admin-add-section {
  margin-top: 30px;
}

.add-product-form {
  background: rgba(64, 64, 64, 0.8);
  border-radius: 15px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.form-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  cursor: pointer;
  background: rgba(64, 64, 64, 0.9);
  transition: background 0.3s ease;
}

.form-header:hover {
  background: rgba(80, 80, 80, 0.9);
}

.form-title {
  color: #FFD700;
  font-weight: bold;
  font-size: 16px;
  margin-right: 30px;
}

.toggle-btn {
  background: #FFD700;
  border: none;
  color: #000;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-product-form.active .toggle-btn {
  transform: rotate(90deg);
}

.form-content {
  padding: 0 20px 20px;
}

.carousel-indicators {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

.indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: none;
  background: #333;
  cursor: pointer;
  transition: background 0.3s ease;
}

.indicator.active {
  background: #FFD700;
}

/* Responsive */
@media (max-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .form-fields {
    gap: 50px;
  }
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: 1fr;
  }

  .carousel-container {
    flex-direction: column;
  }

  .carousel-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    z-index: 3;
  }

  .carousel-btn.prev {
    left: 10px;
  }

  .carousel-btn.next {
    right: 10px;
  }

  .form-fields {
    display: none;
  }
}
</style>