import axios from 'axios'
import { ref } from 'vue'
import api from "@/composables/axios.js";

axios.defaults.baseURL = 'http://localhost:8000/api/'
axios.defaults.withCredentials = true;

export const isAuthenticated = ref(false)


export async function login(email, password) {
    try {
        const response = await api.post('/token/', {email,password});

        isAuthenticated.value = true;
        return { success: true, res:response };
    } catch (error) {
        return {
            success: false,
            error: {
                message: error.response?.data || error.message,
                status: error.response?.status || null
            }
        };
    }
}

export async function register(name, surname, email, password) {
    try {
        await axios.post('user/', { name, surname, email, password })
        return { success: true }
    } catch (error) {
        return { success: false, error: error.response?.data || error?.message }
    }
}


export function logout() {
    return api.post('/cookie-logout/', {}).then(() => {
        isAuthenticated.value = false;
    });
}

// Obtener usuario actual
export async function getCurrentUser() {
    try {
        const response = await api.get('me/')
        isAuthenticated.value = true
        return { success: true, res: response.data}
    } catch (err) {
        isAuthenticated.value = false
        return { success: false, error: err?.response?.data || err?.message }
    }
}

// Intentar refrescar el token con cookies
export async function tryRefreshToken() {
    try {
        await api.post('/token/refresh-cookie/', {})
        return true
    } catch (e) {
        console.log("Error en refrescar el token:", e)
        return false
    }
}