import axios from 'axios'
import { ref } from 'vue'
import api from "@/composables/axios.js";

axios.defaults.baseURL = 'http://localhost:8000/api/'
axios.defaults.withCredentials = true;

export const isAuthenticated = ref(false)
export const user = ref(null)


export async function login(email, password) {
    try {
        const response = await api.post('/token/', {email,password});

        isAuthenticated.value = true;
        user.value = await getCurrentUser()
        console.log(user.value)
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
        user.value = null
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
        user.value = null
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

export async function initAuth() {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
        const res = await getCurrentUser();
        if (res.success) {
            user.value = res.res;
            isAuthenticated.value = true;
        }
    }
}