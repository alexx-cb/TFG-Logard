from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import generate_verification_token

from .models import Product, Cart, Order, RowsOrder, CartItem, Category, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()

        token = generate_verification_token(user)

        verification_link = f"http://localhost:5173/verify?token={token}"

        send_mail(
            'Verifica tu cuenta',
            f'Por favor verifica tu cuenta haciendo clic en el siguiente enlace:\n\n{verification_link}',
            'no-reply@tu-dominio.com',
            [user.email],
            fail_silently=False,
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

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

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Añade info extra al token si quieres
        token['email'] = user.email
        token['role'] = user.role
        return token

    def validate(self, attrs):
        email = attrs.get('username')  # porque espera username por defecto
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('No existe el usuario')

        if not check_password(password, user.password):
            raise serializers.ValidationError('Contraseña incorrecta')

        # Opcional: verificar que usuario esté confirmado
        if not user.confirmed:
            raise serializers.ValidationError('Usuario no confirmado')

        # Manualmente genera tokens
        data = super().get_token(user)
        refresh = data
        access = data.access_token

        return {
            'refresh': str(refresh),
            'access': str(access),
        }