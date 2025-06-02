import api from "@/composables/axios/interceptor.js";
import publicApi from "@/composables/axios/publicApi.js";

export async function getProductsCategory(categoryId){
    try {
        const response = await publicApi.get(`products/category/${categoryId}`)
        return {success: true, data: response}
    }catch (err){
        console.log("Error al hacer el get de los productos")
        return {success: false, error: err?.response?.data || err?.message}
    }
}

export async function postProduct(formData){
    try{
        const response = await api.post('products/',
            formData,
            { headers: {
                'Content-Type': 'multipart/form-data'
                }
            }
        )
    }catch(err){
        console.log("Error al hacer el post del producto: " + err)
        return {success:false, data: err}
    }
}