import axios from "axios";

const publicApi = axios.create({
    baseURL: 'https://logard-backed.up.railway.app/api/',
    withCredentials: false
})

export default publicApi