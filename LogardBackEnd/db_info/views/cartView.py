from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from db_info.models import Cart, Product, CartItem
from db_info.serializers.cartSerializer import CartSerializer, CartItemSerializer


class CartDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


    def post(self, request):
        product_id = request.data.get('product')
        size = request.data.get('size', 'M')
        units = request.data.get('units', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            defaults={'units': units}
        )
        if not created:
            cart_item.units += int(units)
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)


class UpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)

        units = request.data.get('units')
        if units is None:
            return Response({'error': 'Se requiere el campo "units"'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            units = int(units)
        except ValueError:
            return Response({'error': '"units" debe ser un número entero'}, status=status.HTTP_400_BAD_REQUEST)

        if units <= 0:
            cart_item.delete()
            return Response({'message': 'Item eliminado del carrito'}, status=status.HTTP_204_NO_CONTENT)

        cart_item.units = units
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)

        cart_item.delete()
        return Response({'message': 'Item eliminado del carrito'}, status=status.HTTP_204_NO_CONTENT)
