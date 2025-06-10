from decimal import Decimal
from rest_framework import serializers
from db_info.models import RowsOrder, Order


class RowsOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price',max_digits=10,decimal_places=2, read_only=True)
    product_discount = serializers.DecimalField(source='product.discount',max_digits=10,decimal_places=2, read_only=True)
    unit_price_with_discount = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = RowsOrder
        fields= ['id', 'units', 'size', 'product', 'product_name', 'product_price', 'product_discount',
                 'unit_price_with_discount', 'total_price']

    def get_unit_price_with_discount(self, obj):
        discount = obj.product_discount or Decimal('0.00')
        if discount > 0:
            return round(obj.product.price * (Decimal('1.00') - discount /Decimal('100.00')), 2)
        return obj.product.price

    def get_total_price(self, obj):
        unit_price = self.get_unit_price_with_discount(obj)
        return round(obj.product.price * unit_price, 2)


class OrderSerializer(serializers.ModelSerializer):
    items = RowsOrderSerializer(source='rowsorder_set', many=True, read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'address', 'locality', 'province', 'cost', 'status', 'date', 'time', 'user', 'user_email', 'items']

        read_only_fields=['date', 'time', 'user']


class CreateOrderSerializer(serializers.ModelSerializer):
    payment_method_id = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if not all([data.get('address'), data.get('locality'), data.get('province')]):
            raise serializers.ValidationError('All fields are required')
        return data

    class Meta:
        model = Order
        fields = ['address', 'locality', 'province', 'payment_method_id']