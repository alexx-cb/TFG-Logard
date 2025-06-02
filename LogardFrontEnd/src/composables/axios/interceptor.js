import axios from "axios";
import {tryRefreshToken} from "../useAuth.js"

const api = axios.create({
    baseURL : "http://localhost:8000/api/",
    withCredentials: true
})

api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest =error.config

        if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url.includes('/token/refresh-cookie/')){
                originalRequest._retry = true;

                const refreshed = await tryRefreshToken();

                if (refreshed) {
                    return api(originalRequest);
                }
            }

        return Promise.reject(error)
    }
)

const publicApi = axios.create({
    baseURL: 'https://localhost:8000/api/',
    withCredentials: false
})


export default api