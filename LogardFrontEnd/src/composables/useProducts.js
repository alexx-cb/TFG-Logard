import axios from 'axios'
import {ref, onMounted} from "vue";

export function useProducts(){
    const products = ref([])

    const loadProducts = async ()=>{
        const response = await axios.get('api/productos')
        products.value = response.data;
    }

    onMounted(loadProducts())
    return {products}
}