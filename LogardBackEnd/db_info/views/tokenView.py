from datetime import timedelta

from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from LogardBackEnd import settings


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
        print("🔐 Login attempt started")
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh = response.data["refresh"]
            access = response.data["access"]

            print("✅ Tokens generated successfully")
            print(f"Access token preview: {access[:50]}...")
            print(f"Refresh token preview: {refresh[:50]}...")

            # Elimina los tokens del body para mayor seguridad
            response.data.pop("access", None)
            response.data.pop("refresh", None)

            # Opcional: agregar info del usuario
            response.data["message"] = "Login exitoso"

            # Configuración de cookies basada en settings
            jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
            access_lifetime = jwt_settings.get('ACCESS_TOKEN_LIFETIME', timedelta(minutes=15))
            refresh_lifetime = jwt_settings.get('REFRESH_TOKEN_LIFETIME', timedelta(days=1))

            # Convertir a segundos para max_age
            access_max_age = int(access_lifetime.total_seconds())
            refresh_max_age = int(refresh_lifetime.total_seconds())

            cookie_settings = {
                'httponly': True,
                'secure': False,  # True en producción con HTTPS
                'samesite': 'Lax',
                'path': '/'
            }

            # Establecer cookie del access token
            response.set_cookie(
                key="access_token",
                value=access,
                max_age=access_max_age,
                **cookie_settings
            )

            # Establecer cookie del refresh token
            response.set_cookie(
                key="refresh_token",
                value=refresh,
                max_age=refresh_max_age,
                **cookie_settings
            )

            print(f"🍪 Cookies set with max_age: access={access_max_age}s, refresh={refresh_max_age}s")
        else:
            print(f"❌ Login failed with status: {response.status_code}")
            print(f"Error data: {response.data}")

        return response


from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

User = get_user_model()  # Agrega esto al inicio del archivo


class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("=== REFRESH TOKEN DEBUG ===")
        print("COOKIES:", request.COOKIES)
        print("Headers Origin:", request.headers.get('Origin'))

        refresh_token_cookie = request.COOKIES.get('refresh_token')

        if not refresh_token_cookie:
            print("❌ No refresh token found")
            print("Available cookies:", list(request.COOKIES.keys()))
            return Response({"detail": "Refresh token no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print("🔄 Trying to refresh token...")
            # Crear el refresh token object
            refresh_token_obj = RefreshToken(refresh_token_cookie)

            # Generar nuevo access token
            new_access_token = str(refresh_token_obj.access_token)

            # Si ROTATE_REFRESH_TOKENS=True, genera nuevo refresh token
            if getattr(settings, 'SIMPLE_JWT', {}).get('ROTATE_REFRESH_TOKENS', False):
                # ✅ Obtener el objeto usuario completo
                user_id = refresh_token_obj.get('user_id')
                print(f"🔍 User ID from token: {user_id}")

                try:
                    user = User.objects.get(id=user_id)
                    print(f"✅ User found: {user}")
                except User.DoesNotExist:
                    print(f"❌ User with ID {user_id} not found")
                    return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_401_UNAUTHORIZED)

                # Invalidar el token anterior
                refresh_token_obj.blacklist()

                # Crear nuevo refresh token con el objeto usuario
                new_refresh_token = str(RefreshToken.for_user(user))
                print("✅ New refresh token generated")
            else:
                # Si no rotamos tokens, usar el mismo
                new_refresh_token = str(refresh_token_obj)
                print("✅ Using same refresh token (no rotation)")

        except (TokenError, InvalidToken) as e:
            print(f"❌ Token error: {e}")
            return Response({"detail": "Token inválido o expirado"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return Response({"detail": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = Response({"detail": "Access token actualizado con éxito"}, status=status.HTTP_200_OK)

        # Configuración de cookies
        cookie_settings = {
            'httponly': True,
            'secure': False,
            'samesite': 'Lax',
            'path': '/'
        }

        # Establecer cookies
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            max_age=900,  # 15 minutos
            **cookie_settings
        )

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            max_age=24 * 3600,  # 1 día
            **cookie_settings
        )

        print("✅ Cookies set successfully")
        return response