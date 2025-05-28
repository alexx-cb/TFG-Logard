# Crear usuarios
import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from db_info.models import User
from db_info.serializers.userSerializer import UserSerializer


class UserRegisterView(APIView):
    """ Metodo Post Para Crear Usuarios"""
    permission_classes = [AllowAny]


    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Obtener o actualizar usuario autentificado
class CurrentUserView(APIView):
    """Metodo GET y UPDATE para el usuario actual"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyUserView(APIView):
    """Metodo para Obetener el token de la verificacion del usuario
    Return: JSON response con un mensaje que comprueba si es correcto o no
    """
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "Token no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
        except jwt.ExpiredSignatureError:
            return Response({"detail": "Token expirado"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"detail": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            return Response({"detail": "Usuario ya está verificado"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        return Response({"detail": "Usuario verificado correctamente"}, status=status.HTTP_200_OK)