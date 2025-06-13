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

// Computed para calcular el precio final con descuento
const finalPrice = computed(() => {
  if (discount.value > 0) {
    return (price.value * (1 - discount.value / 100)).toFixed(2);
  }
  return price.value;
});

// Computed para verificar si hay descuento
const hasDiscount = computed(() => discount.value > 0);

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
  }
}

async function deleteProductView() {
  if (confirm("¿Estás seguro de que quieres eliminar este producto?")) {
    try {
      const response = await deleteProduct(productId);
      if (response.success) {
        await router.push('/');
      }
    } catch (err) {
    }
  }
}
</script>

<template>
  <div class="product-detail">
    <div class="column left">
      <h1>{{ name }}</h1>
      <form @submit.prevent="updateProduct" v-if="isAdmin">
        <button type="button" class="action-button edit-button" @click="switchDisabled(isEditing.name)">
          Edit Name
        </button>
        <div v-if="isEditing.name.value" class="edit-block">
          <input v-model="name" type="text" />
          <div class="button-group">
            <button type="submit" class="action-button save-button">Guardar</button>
            <button type="button" class="action-button cancel-button" @click="switchDisabled(isEditing.name)">Cancelar</button>
          </div>
        </div>
      </form>

      <form @submit.prevent="updateProduct" v-if="isAdmin">
        <p>{{ description }}</p>
        <button type="button" class="action-button edit-button" @click="switchDisabled(isEditing.description)">
          Edit Description
        </button>
        <div v-if="isEditing.description.value" class="edit-block">
          <textarea v-model="description" rows="4"></textarea>
          <div class="button-group">
            <button type="submit" class="action-button save-button">Guardar</button>
            <button type="button" class="action-button cancel-button" @click="switchDisabled(isEditing.description)">Cancelar</button>
          </div>
        </div>
      </form>
      <p v-if="!isAdmin">{{ description }}</p>
    </div>

    <div class="column center">
      <img :src="`https://logard-backed.up.railway.app${product.image}`" alt="product" v-if="product.image" />
      <div class="cart-container">
        <AddCart :product-id="productId" />
      </div>
    </div>

    <div class="column right">
      <!-- Botón de eliminar en la parte superior derecha -->
      <div class="delete-container" v-if="isAdmin">
        <button @click="deleteProductView" class="action-button delete-button">
          🗑️ Eliminar Producto
        </button>
      </div>

      <form @submit.prevent="updateProduct" v-if="isAdmin">
        <div class="price-section">
          <!-- Precio con descuento -->
          <div class="price" v-if="hasDiscount">
            <span class="price-original">{{ price }}€</span>
            <span class="price-final">{{ finalPrice }}€</span>
          </div>
          <!-- Precio sin descuento -->
          <div class="price" v-else>
            <span>{{ price }}€</span>
          </div>
          <button type="button" class="action-button edit-button" @click="switchDisabled(isEditing.price)">
            Edit Price
          </button>
        </div>
        <div v-if="isEditing.price.value" class="edit-block">
          <input v-model="price" type="number" step="0.01" />
          <div class="button-group">
            <button type="submit" class="action-button save-button">Guardar</button>
            <button type="button" class="action-button cancel-button" @click="switchDisabled(isEditing.price)">Cancelar</button>
          </div>
        </div>
      </form>

      <!-- Sección de descuento para admin -->
      <form @submit.prevent="updateProduct" v-if="isAdmin">
        <div class="discount-section">
          <div class="discount-info" v-if="hasDiscount">
            <span class="discount-badge">-{{ discount }}%</span>
          </div>
          <button type="button" class="action-button edit-button" @click="switchDisabled(isEditing.discount)">
            Edit Discount
          </button>
        </div>
        <div v-if="isEditing.discount.value" class="edit-block">
          <input v-model="discount" type="number" step="1" min="0" max="100" />
          <div class="button-group">
            <button type="submit" class="action-button save-button">Guardar</button>
            <button type="button" class="action-button cancel-button" @click="switchDisabled(isEditing.discount)">Cancelar</button>
          </div>
        </div>
      </form>

      <!-- Precios para usuarios no admin -->
      <div class="price-section" v-if="!isAdmin">
        <div class="price" v-if="hasDiscount">
          <span class="price-original">{{ price }}€</span>
          <span class="price-final">{{ finalPrice }}€</span>
        </div>
        <div class="price" v-else>
          <span>{{ price }}€</span>
        </div>
        <div class="discount-info" v-if="hasDiscount">
          <span class="discount-badge">-{{ discount }}%</span>
        </div>
      </div>

      <form @submit.prevent="updateProduct" class="image-form" v-if="isAdmin">
        <button type="button" class="action-button edit-button" @click="switchDisabled(isEditing.image)">
          Edit Image
        </button>
        <div v-if="isEditing.image.value" class="edit-block">
          <input
            type="file"
            accept="image/*"
            @change="imageContainer"
          />
          <div class="button-group">
            <button type="submit" class="action-button save-button">Guardar</button>
            <button type="button" class="action-button cancel-button" @click="switchDisabled(isEditing.image)">Cancelar</button>
          </div>
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
  min-height: 85vh;
}

.column {
  flex: 1;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.column.left,
.column.right {
  gap: 2rem;
}

.column.center {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 2rem;
}

.column.center img {
  max-width: 100%;
  max-height: 600px;
  border-radius: 8px;
  box-shadow: 0 0 30px rgba(255, 0, 0, 0.5);
}

/* Contenedor del botón eliminar */
.delete-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.action-button {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: #111;
  font-weight: bold;
  font-size: 0.9rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.action-button:hover {
  background: linear-gradient(135deg, #ffed4e, #ffd700);
  transform: translateY(-2px);
}

.action-button:active {
  transform: translateY(0);
}

/* Variaciones específicas para diferentes tipos de botones */
.delete-button {
  background: linear-gradient(135deg, #ff4444, #ff6666);
}

.delete-button:hover {
  background: linear-gradient(135deg, #ff6666, #ff4444);
}

.cancel-button {
  background: linear-gradient(135deg, #666, #888);
}

.cancel-button:hover {
  background: linear-gradient(135deg, #888, #666);
}

/* Estilos para inputs */
input[type="text"],
input[type="number"],
input[type="file"],
textarea {
  margin-top: 0.5rem;
  padding: 0.75rem;
  width: 100%;
  background-color: #222;
  color: #ffd700;
  border: 2px solid #333;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input[type="text"]:focus,
input[type="number"]:focus,
input[type="file"]:focus,
textarea:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

/* Estilos para precios */
.price-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.price {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.price-original {
  text-decoration: line-through;
  color: #888;
  font-size: 1.2rem;
}

.price-final {
  color: #ff4444;
  font-weight: bold;
  font-size: 1.8rem;
}

/* Estilos para descuento */
.discount-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.discount-info {
  display: flex;
  justify-content: center;
  margin-top: 0.5rem;
}

.discount-badge {
  background: linear-gradient(135deg, #ff4444, #ff6666);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 8px rgba(255, 68, 68, 0.3);
}

.sizes p {
  font-size: 1.2rem;
}

.image-form {
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.edit-block {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.button-group {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.button-group .action-button {
  flex: 1;
  min-width: 120px;
}

/* Responsive design */
@media (max-width: 768px) {
  .product-detail {
    flex-direction: column;
    gap: 2rem;
  }

  .column {
    padding: 0.5rem;
  }

  .price {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .delete-container {
    justify-content: center;
  }

  .button-group .action-button {
    min-width: 100px;
  }

  .price-final {
    font-size: 1.5rem;
  }

  .price-original {
    font-size: 1rem;
  }
}
</style>