import api from "@/composables/axios/interceptor.js";

export async function getUserCart(){
    try {
        const response = await api.get('cart/')
        return {success:true, data:response}

    }catch (err){
        console.log("Error en la peticion get del carrito: "+err)
        return {sucess:false, error: err?.response?.value || err?.message}
    }
}