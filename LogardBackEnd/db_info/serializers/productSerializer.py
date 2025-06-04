import os
from rest_framework import serializers
from db_info.models import Product
from db_info.utils.validation_sql import validate_sql_injection


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_input(self, value):
        return validate_sql_injection(value)

    def create(self, validated_data):
        product = Product(**validated_data)
        product.save()
        return product

    def update(self, instance, validated_data):
        # Si hay una nueva imagen, eliminamos la anterior
        new_image = validated_data.get('image', None)
        if new_image and instance.image:
            if instance.image.name != new_image.name:  # Evitar borrar si es la misma
                if os.path.isfile(instance.image.path):
                    os.remove(instance.image.path)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance