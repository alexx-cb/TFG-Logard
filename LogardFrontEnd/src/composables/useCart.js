import api from "@/composables/axios/interceptor.js";

const LOCAL_CART_KEY = "local_cart";

export function getLocalCart() {
    const json = localStorage.getItem(LOCAL_CART_KEY);
    return json ? JSON.parse(json) : [];
}

export function saveLocalCart(cart) {
    localStorage.setItem(LOCAL_CART_KEY, JSON.stringify(cart));
}

export function clearLocalCart() {
    localStorage.removeItem(LOCAL_CART_KEY);
}

// ADD TO LOCALSTORAGE THE PRODUCT
export function addToLocalCart(productId, size, units = 1) {
    let cart = getLocalCart();
    const index = cart.findIndex(
        (item) => item.product === productId && item.size === size
    );
    if (index >= 0) {
        cart[index].units += units;
    } else {
        cart.push({ product: productId, size, units });
    }
    saveLocalCart(cart);
}

// GET PRODUCTS DETAILS BY ID
export async function fetchProductsInfo(productIds) {
    try {
        const response = await api.post("products/info/", { product_ids: productIds });
        return response.data;
    } catch (err) {
        console.error("Error fetching product info:", err);
        return [];
    }
}

// GET FULL CART WITH DETAILS
export async function getLocalCartWithDetails() {
    const localCart = getLocalCart();
    if (localCart.length === 0) return [];

    const productIds = [...new Set(localCart.map((i) => i.product))];
    const products = await fetchProductsInfo(productIds);

    const productMap = {};
    products.forEach((p) => (productMap[p.id] = p));

    return localCart.map((item) => ({
        ...item,
        product_info: productMap[item.product],
    }));
}

// ADD PRODUCT INTO DE DB
export async function addToUserCart(productId, size, units = 1) {
    try {
        const response = await api.post("cart/", {
            product: productId,
            size,
            units
        });
        return { success: true, data: response.data };
    } catch (err) {
        console.error("Error adding to user cart:", err);
        return { success: false, error: err?.response?.data || err?.message };
    }
}

// GET USERS CART
export async function getUserCart() {
    try {
        const response = await api.get("cart/");
        return { success: true, data: response.data };
    } catch (err) {
        console.error("Error fetching user cart:", err);
        return { success: false, error: err?.response?.data || err?.message };
    }
}

// UPDATE CART ITEM UNITS
export async function updateCartItem(itemId, units) {
    try {
        const response = await api.patch(`cart/update/${itemId}/`, { units });
        return { success: true, data: response.data };
    } catch (err) {
        console.error("Error updating cache item:", err);
        return { success: false, error: err?.response?.data || err?.message };
    }
}

// REMOVE SINGLE CART ITEM
export async function removeCartItem(itemId) {
    try {
        const response = await api.delete(`cart/update/${itemId}/`);
        return { success: true, data: response.data };
    } catch (err) {
        console.error("Error removing cart item:", err);
        return { success: false, error: err?.response?.data || err?.message };
    }
}

// CLEAR ALL CART ITEMS
export async function clearUserCart() {
    try {
        const response = await api.delete("cart/clear/");
        return { success: true, data: response.data };
    } catch (err) {
        console.error("Error clearing cart:", err);
        return { success: false, error: err?.response?.data || err?.message };
    }
}

// MERGE THE LOCALSTORAGE ONTO THE CART DB
export async function mergeLocalCartToUser() {
    const localCart = getLocalCart();
    if (localCart.length === 0) return { success: true };

    try {
        await api.post("cart/merge/", { items: localCart });
        clearLocalCart();
        return { success: true };
    } catch (err) {
        console.error("Error merging cart:", err);
        return { success: false, error: err?.response?.data || err?.message };
    }
}