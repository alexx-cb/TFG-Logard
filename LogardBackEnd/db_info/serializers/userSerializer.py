from django.core.mail import send_mail
from rest_framework import serializers

from db_info.models import User
from db_info.utils import generate_verification_token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'email', 'password', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
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