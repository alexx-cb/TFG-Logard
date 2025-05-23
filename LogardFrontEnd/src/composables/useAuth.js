import axios from 'axios'
import { ref } from 'vue'

axios.defaults.baseURL = 'http://localhost:8000/api/'
axios.defaults.withCredentials = true;

export const isAuthenticated = ref(false)

const token = sessionStorage.getItem('token')
if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

export async function login(email, password) {
    try {
        const response = await axios.post('/token/', {
            email,
            password
        }, {
            withCredentials: true
        });

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
    return axios.post('/cookie-logout/', {}, { withCredentials: true }).then(() => {
        isAuthenticated.value = false;
    });
}

// Obtener usuario actual
export async function getCurrentUser() {
    try {
        const response = await axios.get('me/', {withCredentials:true})
        isAuthenticated.value = true
        return { success: true, res: response.data}
    } catch (err) {
        isAuthenticated.value = false
        return { success: false, error: err?.response?.data || err?.message }
    }
}

// Intentar refrescar el token con cookies
async function tryRefreshToken() {
    try {
        await axios.post('/token/refresh-cookie/', {}, { withCredentials: true })
        return true
    } catch (e) {
        return false
    }
}