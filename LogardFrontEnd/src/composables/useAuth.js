import axios from 'axios'
import { ref } from 'vue'
import api from "@/composables/axios/interceptor.js";

axios.defaults.baseURL = 'http://localhost:8000/api/'
axios.defaults.withCredentials = true;

export const isAuthenticated = ref(false)
export const user = ref(null)


export async function login(email, password) {
    try {
        const response = await api.post('/token/', {email,password});

        isAuthenticated.value = true;
        user.value = await getCurrentUser()
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
        const response = await api.post("/token/refresh-cookie/", {});
        if (response.status === 200) {
              // Ahora pedimos los datos del usuario con el nuevo access token
              const me = await api.get("/me/");
              user.value = me.data;
              console.log("Access token refrescado correctamente.");
              return true;
        }
        return false;
      } catch (e) {
            console.log("Error en refrescar el token:", e);
            return false;
      }
}

export async function initAuth() {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
        const response = await getCurrentUser();
        console.log(response)
        if (response.success) {
            user.value = response.data;
            isAuthenticated.value = true;
        }
    }
}