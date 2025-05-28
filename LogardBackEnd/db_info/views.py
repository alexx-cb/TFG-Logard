import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, CartItem, Cart, RowsOrder
from .serializers import ProductSerializer, OrderSerializer, CartItemSerializer, CartSerializer, \
    RowsOrderSerializer, CategorySerializer


# Create your views here.


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