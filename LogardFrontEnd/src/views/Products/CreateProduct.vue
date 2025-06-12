<script setup>
import { user } from '@/composables/useAuth';
import { computed, ref } from "vue";
import { postProduct } from "@/composables/useProducts.js";

const isAdmin = computed(() => user.value?.is_staff);

const name = ref('');
const description = ref('');
const price = ref('');
const discount = ref('');
const image = ref(null);

const props = defineProps({
  categoryId: Number
});
const emit = defineEmits(['update-product', 'close-form']);

function imageContainer(event) {
  image.value = event.target.files[0];
}

async function createProduct() {
  const formData = new FormData();

  formData.append('name', name.value);
  formData.append('description', description.value);
  formData.append('price', price.value);
  formData.append('discount', discount.value);
  formData.append('image', image.value);
  formData.append('category', props.categoryId);

  try {
    const response = await postProduct(formData);
    if (response.success) {
      emit('update-product');
      emit('close-form');
      console.log("producto creado con exito");
    } else {
      console.log("Error en la respuesta");
      console.log(response);
    }
  } catch (err) {
    console.log("Error al crear el producto: " + err);
  }
}

function closeForm() {
  emit('close-form');
}
</script>

<template>
  <div v-if="isAdmin" class="create-product-container">
    <div class="form-wrapper">
      <div class="form-header">
        <h3>Create New Product</h3>
        <button @click="closeForm" class="close-btn">×</button>
      </div>

      <form @submit.prevent="createProduct" class="product-form" novalidate>
        <div class="form-grid">
          <!-- Left column - Form inputs -->
          <div class="form-inputs">
            <div class="input-group">
              <label for="name">Name</label>
              <input
                type="text"
                id="name"
                v-model="name"
                placeholder="Product name"
                required
              />
            </div>

            <div class="input-group">
              <label for="description">Description</label>
              <textarea
                id="description"
                v-model="description"
                placeholder="Product description"
                rows="3"
              ></textarea>
            </div>

            <div class="input-row">
              <div class="input-group">
                <label for="price">Price (€)</label>
                <input
                  type="number"
                  id="price"
                  v-model="price"
                  placeholder="0.00"
                  step="0.01"
                  min="0"
                  required
                />
              </div>

              <div class="input-group">
                <label for="discount">Discount (%)</label>
                <input
                  type="number"
                  id="discount"
                  v-model="discount"
                  placeholder="0"
                  min="0"
                  max="100"
                />
              </div>
            </div>
          </div>

          <!-- Right column - Image upload -->
          <div class="image-section">
            <div class="image-upload-area">
              <input
                type="file"
                id="image"
                @change="imageContainer"
                accept="image/*"
                required
                class="styled-file-input"
              />
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" @click="closeForm" class="cancel-btn">
            Cancel
          </button>
          <button type="submit" class="submit-btn">
            Create Product
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.create-product-container {
  background: rgba(0, 0, 0, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 0;
  margin-top: 20px;
  border: 1px solid #333;
}

.form-wrapper {
  position: relative;
}

.form-header {
  width: 50%;
  display: flex;
  align-items: center;
  padding: 25px 30px 20px;
  border-bottom: 1px solid #333;
}

.form-header h3 {
  color: #FFD700;
  margin: 0;
  font-size: 20px;
  font-weight: bold;
  flex: 1;
}

.close-btn {
  background: none;
  border: none;
  color: #888;
  font-size: 24px;
  cursor: pointer;
  padding: 5px;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #FFD700;
}

.product-form {
  padding: 30px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 40px;
  margin-bottom: 30px;
}

.form-inputs {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  color: #FFD700;
  font-size: 14px;
  font-weight: 500;
}

.input-group input,
.input-group textarea {
  background: #222;
  border: 1px solid #444;
  border-radius: 8px;
  padding: 12px 15px;
  color: #fff;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.input-group input:focus,
.input-group textarea:focus {
  outline: none;
  border-color: #FFD700;
}

.input-group textarea {
  resize: vertical;
  min-height: 80px;
}

.input-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.image-section {
  display: flex;
  flex-direction: column;
}

.image-upload-area {
  flex: 1;
  margin-top: 20px;
}

.file-label {
  display: block;
  cursor: pointer;
  height: 100%;
  min-height: 250px;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  border: 2px dashed #444;
  border-radius: 12px;
  transition: all 0.3s ease;
  padding: 20px;
  text-align: center;
}

.upload-placeholder:hover {
  border-color: #FFD700;
  background: rgba(255, 215, 0, 0.05);
}

.upload-icon {
  font-size: 48px;
  margin-bottom: 15px;
  opacity: 0.7;
}

.upload-placeholder p {
  color: #FFD700;
  font-size: 16px;
  margin: 0 0 8px 0;
  font-weight: 500;
}

.upload-placeholder span {
  color: #888;
  font-size: 12px;
}

.styled-file-input {
  margin-top: 10px;
  background: #222;
  border: 1px solid #444;
  border-radius: 8px;
  padding: 10px 15px;
  color: #fff;
  font-size: 14px;
  width: 100%;
  cursor: pointer;
}

.styled-file-input:hover {
  border-color: #FFD700;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid #333;
}

.cancel-btn {
  background: transparent;
  border: 1px solid #666;
  color: #888;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  border-color: #888;
  color: #fff;
}

.submit-btn {
  background: #FFD700;
  border: none;
  color: #000;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  background: #FFA500;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .input-row {
    grid-template-columns: 1fr;
  }

  .product-form {
    padding: 20px;
  }

  .form-header {
    padding: 20px;
  }
}
</style>
