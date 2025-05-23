import axios from "axios";

axios.defaults.baseURL = 'http://localhost:8000/api/'
axios.defaults.withCredentials = true;

const token = sessionStorage.getItem('token')
if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

export async function getCategories(){
    try {
        const response = await axios.get('categories/')
        return { success: true, res: response }
    } catch (err) {
        console.error("Error al obtener categorías:", err)
        return { success: false, error: err?.response?.data || err?.message }
    }
}

export async function postCategories(name){
    try {
        const response = await axios.post('categories/', { name })
        return { success: true, res: response }  // corregido 'success'
    } catch (err) {
        console.error("Error al crear categoría:", err)
        return { success: false, error: err?.response?.data || err?.message }
    }
}
