from rest_framework import serializers
from db_info.models import CartItem, Cart
from decimal import Decimal


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_discount = serializers.DecimalField(source='product.discount', max_digits=5, decimal_places=2, read_only=True)
    price_with_discount = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    total_price_with_discount = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_name', 'size', 'units', 'product_price', 'product_discount',
            'price_with_discount', 'total_price', 'total_price_with_discount'
        ]

    def get_price_with_discount(self, obj):
        discount = obj.product.discount or Decimal('0.00')
        if discount == 0:
            return None
        return round(obj.product.price * (Decimal('1.00') - discount / Decimal('100.00')), 2)

    def get_total_price(self, obj):
        return round(obj.units * obj.product.price, 2)

    def get_total_price_with_discount(self, obj):
        discount = obj.product.discount or Decimal('0.00')
        if discount == 0:
            return None
        discounted_price = obj.product.price * (Decimal('1.00') - discount / Decimal('100.00'))
        return round(obj.units * discounted_price, 2)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if rep.get('product_discount') in [None, '0.00', 0, 0.0, '0']:
            rep.pop('price_with_discount', None)
            rep.pop('total_price_with_discount', None)
        return rep


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total']

    def get_total(self, obj):
        total = Decimal('0.00')
        for item in obj.items.all():
            discount = item.product.discount or Decimal('0.00')
            if discount > 0:
                discounted_price = item.product.price * (Decimal('1.00') - discount / Decimal('100.00'))
            else:
                discounted_price = item.product.price
            total += item.units * discounted_price
        return round(total, 2)
