<script setup>
import {useRoute, useRouter} from "vue-router";
import {computed, onMounted, ref} from "vue";
import {deleteProduct, getProductDetails, patchProduct} from "@/composables/useProducts";
import {user} from "@/composables/useAuth.js";
import Cart from "@/views/Cart.vue";

const route = useRoute();
const router = useRouter()
const productId = route.params.id;

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

const isAdmin = computed(()=>user.value?.is_staff)

function imageContainer(event) {
  image.value = event.target.files[0];
}

function switchDisabled(refVar) {
  if (refVar && typeof refVar.value !== 'undefined') {
    refVar.value = !refVar.value;
  } else {
    console.warn("switchDisabled recibió un valor inválido:", refVar);
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
  if (discount.value && discount.value !== productOriginal.value.discount) {
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
      console.log("Producto actualizado con éxito");
      await getDetails();

      isEditing.name.value = false;
      isEditing.description.value = false;
      isEditing.price.value = false;
      isEditing.discount.value = false;
      isEditing.image.value = false;
      image.value = null;
    }
  } catch (err) {
    console.log("Error al actualizar el producto", err);
  }
}

async function deleteProductView(){
  try{
    const response = await deleteProduct(productId)

    if (response.success){
      alert("Producto eliminado correctamente")
      await router.push('/')
    }
  }catch(err){
    console.log("Error en la vista: " +err)
  }
}
</script>

<template>
  <h1>PRODUCT DETAIL</h1>
  <p>{{product}}</p>

  <div v-if="isAdmin">
    <p>Pulsa <span @click="deleteProductView">Aqui</span> para eliminar el producto</p>

  </div>

  <!-- NAME -->
  <form @submit.prevent="updateProduct">
    <label for="name">Name:</label>
    <input type="text" v-model="name" :disabled="!isEditing.name.value" />

    <div v-if="isAdmin">
      <button type="button" @click="switchDisabled(isEditing.name)" v-if="!isEditing.name.value">Editar</button>
      <button type="button" @click="switchDisabled(isEditing.name)" v-else>Cancel</button>
      <input type="submit" value="Update Name" v-if="isEditing.name.value" />
    </div>

  </form>

  <!-- DESCRIPTION -->
  <form @submit.prevent="updateProduct">
    <label for="description">Description:</label>
    <input type="text" v-model="description" :disabled="!isEditing.description.value" />

    <div v-if="isAdmin">
      <button type="button" @click="switchDisabled(isEditing.description)" v-if="!isEditing.description.value">Editar</button>
      <button type="button" @click="switchDisabled(isEditing.description)" v-else>Cancel</button>
      <input type="submit" value="Update Description" v-if="isEditing.description.value" />
    </div>
  </form>

  <!-- PRICE -->
  <form @submit.prevent="updateProduct">
    <label for="price">Price:</label>
    <input type="number" v-model="price" :disabled="!isEditing.price.value" />

    <div v-if="isAdmin">
      <button type="button" @click="switchDisabled(isEditing.price)" v-if="!isEditing.price.value">Editar</button>
      <button type="button" @click="switchDisabled(isEditing.price)" v-else >Cancel</button>
      <input type="submit" value="Update Price" v-if="isEditing.price.value" />
    </div>
  </form>

  <!-- DISCOUNT -->
  <form @submit.prevent="updateProduct">
    <label for="discount">Discount:</label>
    <input type="number" v-model="discount" :disabled="!isEditing.discount.value" />

    <div v-if="isAdmin">
      <button type="button" @click="switchDisabled(isEditing.discount)" v-if="!isEditing.discount.value">Editar</button>
      <button type="button" @click="switchDisabled(isEditing.discount)" v-else>Cancel</button>
      <input type="submit" value="Update Discount" v-if="isEditing.discount.value" />
    </div>
  </form>

  <!-- IMAGE -->
  <form @submit.prevent="updateProduct">
    <label>Imagen:</label><br />
    <img :src="`http://localhost:8000${product.image}`" alt="Imagen del producto" style="max-width: 200px;" v-if="product.image" /><br />


    <div v-if="isAdmin">
      <input type="file" accept="image/*" @change="imageContainer" :disabled="!isEditing.image.value" />

      <button type="button" @click="switchDisabled(isEditing.image)" v-if="!isEditing.image.value">Editar Imagen</button>
      <button type="button" @click="switchDisabled(isEditing.image)" v-else>Cancel</button>
      <input type="submit" value="Update Image" v-if="isEditing.image.value" />
    </div>
  </form>
</template>