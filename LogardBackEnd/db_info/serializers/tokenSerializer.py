from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from db_info.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        email = attrs.get('username')
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