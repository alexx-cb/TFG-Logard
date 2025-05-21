import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000/api/'

export async function login(username, password){
    const response = await axios.post('token/', {username, password})
    const token = response.data.access
    localStorage.setItem('token', token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}