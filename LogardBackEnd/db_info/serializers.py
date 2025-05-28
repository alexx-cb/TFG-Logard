from rest_framework import serializers
from .models import Product, Cart, Order, RowsOrder, CartItem


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class RowsOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RowsOrder
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
