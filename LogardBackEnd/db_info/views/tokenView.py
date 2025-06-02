from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class CookieLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie("access_token", path="/")
        response.delete_cookie("refresh_token", path="/")
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            pass
        response.status_code = status.HTTP_205_RESET_CONTENT
        return response

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh = response.data["refresh"]
            access = response.data["access"]

            # Elimina los tokens del body si quieres (opcional)
            response.data.pop("access", None)
            response.data.pop("refresh", None)

            # Setear cookies seguras
            response.set_cookie(
                key="access_token",
                value=access,
                httponly=True,
                secure=False,  # True si usas HTTPS
                samesite="Lax",  # o 'Strict' si lo prefieres más seguro
                max_age=3600,
                path="/"
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=7 * 24 * 3600,
                path="/"
            )

        return response

class CookieTokenRefreshView(APIView):
    def post(self, request):
        refresh_token_cookie = request.COOKIES.get('refresh_token')

        if not refresh_token_cookie:
            return Response({"detail": "Refresh token no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Crea una nueva instancia del refresh token a partir de la cookie
            refresh_token_obj = RefreshToken(refresh_token_cookie)

            # Rota el refresh token (solo si ROTATE_REFRESH_TOKENS=True)
            new_refresh_token = str(refresh_token_obj)
            new_access_token = str(refresh_token_obj.access_token)

        except TokenError:
            return Response({"detail": "Token inválido o expirado"}, status=status.HTTP_401_UNAUTHORIZED)

        # Crea la respuesta
        response = Response({"detail": "Access token actualizado con éxito"}, status=status.HTTP_200_OK)

        # Establece nuevo access token
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=3600,
            path="/"
        )

        # Establece nuevo refresh token (solo si rotación está activa)
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 3600,  # 7 días
            path="/"
        )

        return response