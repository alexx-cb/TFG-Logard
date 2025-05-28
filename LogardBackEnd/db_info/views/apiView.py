from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


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