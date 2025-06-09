from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from db_info.models import Product
from db_info.utils.PermissionClass import IsAdminOrReadOnly
from db_info.serializers.productSerializer import ProductSerializer


class ProductListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

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


class ProductListCategoryView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        products = Product.objects.filter(category=pk)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailsView(APIView):
    permission_classes = [IsAdminOrReadOnly]

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
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductByNameView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, name):
        products = Product.objects.filter(name__icontains=name)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def product_info_list(request):
    """
    Recibe una lista de IDs de producto en JSON:
    { "product_ids": [1, 2, 3] }
    Devuelve lista con info de esos productos.
    """
    product_ids = request.data.get('product_ids', [])
    if not isinstance(product_ids, list) or not all(isinstance(i, int) for i in product_ids):
        return Response({"error": "Se espera una lista de IDs de producto (enteros)."}, status=status.HTTP_400_BAD_REQUEST)

    products = Product.objects.filter(id__in=product_ids)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
