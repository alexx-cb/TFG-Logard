import {ref} from "vue";
import api from "@/composables/axios/interceptor.js";

export const orderStatus = ref(null)
export const lastOrder = ref(null)

export async function createOrder({address, locality, province, cart_items}){
    try{
        const response = await api.post('order/create/', {address, locality, province, cart_items })

        lastOrder.value = response.data
        orderStatus.value = 'pending_payment'

        return { success: true, approval_url: response.data.approval_url, order_id: response.data.order_id}
    }catch(err){
        orderStatus.value = "Error"
        return {success:false, error: err.response?.data || err?.message}

    }

}

export async function  executePayPalPayment({paymentId, payerId, orderId}){
    try{

        const url = `paypal-execute/?paymentId=${paymentId}&PayerID=${payerId}&order_id=${orderId}`
        const response = await api.get(url)

        orderStatus.value= response.data.status
        lastOrder.value = response.data

        return {success:true, data: response.data}

    }catch (err){
        orderStatus.value = "error"
        return {success:false, error: err.response?.data || err?.message}
    }
}

export async function getUserOrders(){
    try{
        const response = await api.get('my-orders/')
        return {success:true, data: response.data}
    }catch(err){
        return { success: false, error: err?.response?.value || err?.message };
    }
}