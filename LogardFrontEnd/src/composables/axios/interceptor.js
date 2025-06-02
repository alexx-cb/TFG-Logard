import axios from "axios";
import {isAuthenticated, tryRefreshToken, user} from "../useAuth.js"

const api = axios.create({
    baseURL : "http://localhost:8000/api/",
    withCredentials: true
})

api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url.includes('/token/refresh-cookie/')) {
            originalRequest._retry = true;

            const refreshed = await tryRefreshToken();

            if (refreshed) {
                return api(originalRequest);
            } else {
                user.value = null;
                isAuthenticated.value = false;

                return Promise.reject(error);
            }
        }

        return Promise.reject(error);
    }
)

export default api