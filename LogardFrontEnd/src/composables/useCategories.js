import api from "@/composables/axios/interceptor.js";
import publicApi from "@/composables/axios/publicApi.js";


export async function getCategories(){
    try {
        const response = await publicApi.get('categories/')
        return { success: true, data: response }
    } catch (err) {
        return { success: false, error: err?.response?.data || err?.message }
    }
}

export async function postCategories(name){
    try {
        const response = await api.post('categories/', { name })
        return { success: true, data: response }
    } catch (err) {
        return { success: false, error: err?.response?.data || err?.message }
    }
}

export async function updateCategory(id, name){
    try{
        const response = await api.patch(`categories/${id}/`, { name })
        return {success: true, data:response}
    }catch (err){
        return {success: false, error: err?.response?.value || err?.message}
    }
}

export async function deleteCategory(id){
    try{
        const response =await api.delete(`categories/${id}/`)
        return {success:true, data:response}
    }catch(err){
        return {success: false, error: err?.response?.value || err?.message}
    }
}