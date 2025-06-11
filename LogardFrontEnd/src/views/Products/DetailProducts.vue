<script setup>
import {useRoute, useRouter} from "vue-router";
import {computed, onMounted, ref} from "vue";
import {deleteProduct, getProductDetails, patchProduct} from "@/composables/useProducts";
import {user} from "@/composables/useAuth.js";
import AddCart from "@/views/Cart/AddCart.vue";

const route = useRoute();
const router = useRouter();
const productId = Number(route.params.id);

const product = ref({});
const productOriginal = ref({});

const name = ref("");
const description = ref("");
const price = ref(0);
const discount = ref(0);
const image = ref(null);

const isEditing = {
  name: ref(false),
  description: ref(false),
  price: ref(false),
  discount: ref(false),
  image: ref(false)
};

onMounted(() => {
  getDetails();
});

const isAdmin = computed(() => user.value?.is_staff);

function imageContainer(event) {
  image.value = event.target.files[0];
}

function switchDisabled(refVar) {
  if (refVar && typeof refVar.value !== 'undefined') {
    refVar.value = !refVar.value;
  }
}

async function getDetails() {
  try {
    const response = await getProductDetails(productId);
    if (response.success) {
      const data = response.data.data;
      product.value = data;
      productOriginal.value = { ...data };

      name.value = data.name;
      description.value = data.description;
      price.value = data.price;
      discount.value = data.discount;
    }
  } catch (err) {
    console.log("Error en los detalles del producto: " + err);
  }
}

async function updateProduct() {
  const formData = new FormData();

  if (name.value && name.value !== productOriginal.value.name) {
    formData.append("name", name.value);
  }
  if (description.value && description.value !== productOriginal.value.description) {
    formData.append("description", description.value);
  }
  if (price.value && price.value !== productOriginal.value.price) {
    formData.append("price", price.value.toString());
  }
  if (discount.value !== productOriginal.value.discount) {
    formData.append("discount", discount.value.toString());
  }
  if (image.value) {
    formData.append("image", image.value);
  }

  if ([...formData.keys()].length === 0) {
    console.log("No hay cambios para actualizar.");
    return;
  }

  try {
    const response = await patchProduct(productId, formData);
    if (response.success) {
      await getDetails();

      Object.keys(isEditing).forEach(key => {
        isEditing[key].value = false;
      });
      image.value = null;
    }
  } catch (err) {
    console.log("Error al actualizar el producto", err);
  }
}

async function deleteProductView() {
  try {
    const response = await deleteProduct(productId);
    if (response.success) {
      alert("Producto eliminado correctamente");
      await router.push('/');
    }
  } catch (err) {
    console.log("Error en la vista: " + err);
  }
}
</script>


<template>
  <div class="product-detail">
    <div class="column left">
      <h1>{{ name }}</h1>
      <form @submit.prevent="updateProduct">
        <button type="button" class="edit-button" @click="switchDisabled(isEditing.name)">Edit Name</button>
        <div v-if="isEditing.name.value" class="edit-block">
          <input v-model="name" type="text" />
          <button type="submit" class="save-button">Guardar</button>
          <button type="button" class="cancel-button" @click="switchDisabled(isEditing.name)">Cancelar</button>
        </div>
      </form>

      <h2>Description</h2>
      <form @submit.prevent="updateProduct">
        <p>{{ description }}</p>
        <button type="button" class="edit-button" @click="switchDisabled(isEditing.description)">Edit Description</button>
        <div v-if="isEditing.description.value" class="edit-block">
          <input v-model="description" type="text" />
          <button type="submit" class="save-button">Guardar</button>
          <button type="button" class="cancel-button" @click="switchDisabled(isEditing.description)">Cancelar</button>
        </div>
      </form>
    </div>

    <div class="column center">
      <img :src="`http://localhost:8000${product.image}`" alt="product" v-if="product.image" />
      <div class="cart-container">
        <AddCart :product-id="productId" />
      </div>
    </div>

    <div class="column right">
      <form @submit.prevent="updateProduct">
        <div class="price">
          <span>{{ price }}€</span>
          <button type="button" class="edit-button" @click="switchDisabled(isEditing.price)">Edit Price</button>
        </div>
        <div v-if="isEditing.price.value" class="edit-block">
          <input v-model="price" type="number" />
          <button type="submit" class="save-button">Guardar</button>
          <button type="button" class="cancel-button" @click="switchDisabled(isEditing.price)">Cancelar</button>
        </div>
      </form>

      <div class="sizes">
        <p>S / M / L</p>
      </div>

      <form @submit.prevent="updateProduct" class="image-form">
        <button type="button" class="edit-button" @click="switchDisabled(isEditing.image)">Edit Image</button>
        <div v-if="isEditing.image.value" class="edit-block">
          <input
            type="file"
            accept="image/*"
            @change="imageContainer"
          />
          <button type="submit" class="save-button">Guardar</button>
          <button type="button" class="cancel-button" @click="switchDisabled(isEditing.image)">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.product-detail {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  background-color: #111;
  color: #ffd700;
  padding: 2rem;
  font-family: "Arial", sans-serif;
  min-height: 100vh;
}

.column {
  flex: 1;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.column.left,
.column.right {
  gap: 2rem;
}

.column.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

.column.center img {
  max-width: 100%;
  max-height: 600px;
  border-radius: 8px;
  box-shadow: 0 0 30px rgba(255, 0, 0, 0.5);
}

.edit-button,
.save-button,
.cancel-button {
  background-color: #888;
  color: #ffd700;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border: none;
  cursor: pointer;
  margin-top: 0.5rem;
  margin-right: 0.5rem;
}

.edit-button:hover,
.save-button:hover,
.cancel-button:hover {
  background-color: #aaa;
}

input[type="text"],
input[type="number"],
input[type="file"] {
  margin-top: 0.5rem;
  padding: 0.5rem;
  width: 100%;
  background-color: #222;
  color: #ffd700;
  border: none;
  border-radius: 4px;
}

.price {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.5rem;
}

.sizes p {
  font-size: 1.2rem;
}

.image-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.edit-block {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}
</style>