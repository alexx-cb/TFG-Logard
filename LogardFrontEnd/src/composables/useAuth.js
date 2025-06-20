import axios from 'axios'
import { ref } from 'vue'
import api from "@/composables/axios/interceptor.js";
import {mergeLocalCartToUser} from "@/composables/useCart.js";

axios.defaults.baseURL = 'https://logard-backed.up.railway.app/api/'
axios.defaults.withCredentials = true;

export const isAuthenticated = ref(false)
export const user = ref(null)


export async function login(email, password) {
    try {
        const response = await api.post('/token/', {email,password});

        isAuthenticated.value = true;
        user.value = await getCurrentUser()

        const mergeResult = await mergeLocalCartToUser();
        if (!mergeResult.success) {
            console.warn("Carrito local no pudo fusionarse:", mergeResult.error);
        }

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
        user.value = response.data
        return { success: true, data: response.data}
    } catch (err) {
        isAuthenticated.value = false
        user.value = null
        return { success: false, error: err?.response?.data || err?.message }
    }
}

// Intentar refrescar el token con cookies
export async function tryRefreshToken() {
    try {
        const response = await axios.post('https://logard-backed.up.railway.app/api/token/refresh-cookie/', {})
        return response.status === 200
    } catch (err) {
        return false
    }
}

export async function initAuth() {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
        const response = await getCurrentUser();
        if (response.success) {
            user.value = response.data;
            isAuthenticated.value = true;
        }
    }
}