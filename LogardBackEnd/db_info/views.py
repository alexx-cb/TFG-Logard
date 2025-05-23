import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from jwt import ExpiredSignatureError, InvalidTokenError
from rest_framework import viewsets, status, generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Product, Order, User, CartItem, Cart, RowsOrder, Category
from .serializers import ProductSerializer, OrderSerializer, UserSerializer, CartItemSerializer, CartSerializer, \
    RowsOrderSerializer, CategorySerializer


# Create your views here.


class APIRootView(APIView):
    """Muestra las Rutas de la API en localhost:8000/api/"""
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            # "products": reverse('product-list-create', request=request),
            # "orders": reverse('order-list-create', request=request),
            # "cart-items": reverse('cartitem-list-create', request=request),

            "products": reverse('product-list', request=request),
            "products-details": reverse('product-details',kwargs={'pk':1}, request=request),
            "products-search": reverse('product-search',kwargs={'name':'camiseta'}, request=request),

            "categories": reverse('category-list', request=request),
            "category-detail": reverse('category-detail', kwargs={"pk": 1}, request=request),  # ejemplo pk
            "category-search": reverse('category-search', kwargs={"name": "ropa"}, request=request),

            "user-register": reverse('user-register', request=request),
            "me": reverse('user-detail', request=request),

            "token": reverse('token_obtain_pair', request=request),
            "token-refresh": reverse('token_refresh', request=request),
            "verify": reverse('verify-user', request=request),
        })

class CookieLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
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
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({"detail": "Refresh token no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
        except TokenError as e:
            return Response({"detail": "Token inválido o expirado"}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response()
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # cambia a True si usas HTTPS
            samesite="Lax",
            max_age=3600,
            path="/"
        )

        response.status_code = status.HTTP_200_OK
        response.data = {"detail": "Access token actualizado con éxito"}
        return response

# Crear usuarios
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

class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryByNameView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, name):
        categories = Category.objects.filter(name__icontains=name)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ProductListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductByNameView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, name):
        products = Product.objects.filter(name__icontains=name)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class RowsOrderViewSet(viewsets.ModelViewSet):
    queryset = RowsOrder.objects.all()
    serializer_class = RowsOrderSerializer
    permission_classes = [IsAuthenticated]

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer