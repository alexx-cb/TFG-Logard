import api from "@/composables/axios/interceptor.js";
import publicApi from "@/composables/axios/publicApi.js";

export async function getProductsCategory(categoryId){
    try {
        const response = await publicApi.get(`products/category/${categoryId}`)
        return {success: true, data: response}
    }catch (err){
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
        return {success: true, data:response}
    }catch(err){
        return {success:false, data: err}
    }
}

export async function getProductDetails(id){
    try{
        const response = await api.get(`products/${id}/`)
        return {success:true, data: response}
    }catch(err){
        return {success:false, error: err?.response?.value || err?.message}
    }
}

export async function patchProduct(id, formData) {
    try {
        const response = await api.patch(`products/${id}/`, formData);
        return { success: true, data: response };
    } catch (err) {
        return { success: false, error: err?.response?.data || err?.message };
    }
}

export async function deleteProduct(id){
    try{
        const response = await  api.delete(`products/${id}/`)
        return {success: true, data: response}
    }catch (err){
    }
}