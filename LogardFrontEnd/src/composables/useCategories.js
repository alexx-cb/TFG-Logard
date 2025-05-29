import api from "@/composables/axios.js";


export async function getCategories(){
    try {
        const response = await api.get('categories/')
        return { success: true, data: response }
    } catch (err) {
        console.error("Error al obtener categorías:", err)
        return { success: false, error: err?.response?.data || err?.message }
    }
}

export async function postCategories(name){
    try {
        const response = await api.post('categories/', { name })
        return { success: true, data: response }
    } catch (err) {
        console.error("Error al crear categoría:", err)
        return { success: false, error: err?.response?.data || err?.message }
    }
}
