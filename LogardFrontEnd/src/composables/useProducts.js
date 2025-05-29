import api from "@/composables/axios.js";

export async function getProducts(){
    try {
        const response = await api.get('products')
        return {success: true, data: response}
    }catch (err){
        console.log("Error al hacer el get de los productos")
        return {success: false, error: err?.response?.data || err?.message}
    }
}

export async function postProduct(name, description, price, discount, image, category){
    try{
        const response = await api.post('products',
            {name, description, price, discount, image,category})
        console.log("Producto creado correctamente")
        return {success:true, data: response}
    }catch(err){
        console.log("Error al hacer el post del producto")
    }
}