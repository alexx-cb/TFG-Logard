from django.conf import settings
from rest_framework import serializers
from sib_api_v3_sdk import SendSmtpEmail, Configuration, ApiClient, TransactionalEmailsApi

from db_info.models import User
from db_info.utils.verification_token import generate_verification_token


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

        verification_link = f"https://logard.es/verify?token={token}"
        configuration = Configuration()
        configuration.api_key['api-key'] = settings.API_KEY_BREVO
        api_client = ApiClient(configuration)
        email_api = TransactionalEmailsApi(api_client)

        # Crear el email
        email = SendSmtpEmail(
            to=[{"email": user.email}],
            sender={"name": "Logard Brand", "email": settings.EMAIL_SENDER},
            subject="Verifica tu cuenta",
            html_content=f"""
                    <p>Hola {user.name},</p>
                    <p>Gracias por registrarte. Por favor verifica tu cuenta haciendo clic en el siguiente enlace:</p>
                    <p><a href="{verification_link}">Verificar cuenta</a></p>
                    <p>Si no creaste esta cuenta, ignora este mensaje.</p>
                """
        )

        # Enviar el email
        try:
            email_api.send_transac_email(email)
        except Exception as e:
            pass
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance