from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from db_info.models import Cart, Product, CartItem
from db_info.serializers.cartSerializer import CartSerializer, CartItemSerializer


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product')
        size = request.data.get('size', 'M')
        units = int(request.data.get('units', 1))

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
            cart_item.units += units
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)

        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)

        cart_item.delete()
        return Response({'message': 'Item eliminado del carrito'}, status=status.HTTP_204_NO_CONTENT)


class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """
        Elimina todos los items del carrito del usuario autenticado
        """
        try:
            cart = Cart.objects.get(user=request.user)
            # Eliminar todos los items del carrito
            deleted_count = cart.items.all().delete()[0]

            return Response({
                'message': f'Carrito vaciado exitosamente. Se eliminaron {deleted_count} items.',
                'items_deleted': deleted_count
            }, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            # Si no existe carrito, crear uno vacío
            Cart.objects.create(user=request.user)
            return Response({
                'message': 'No había items en el carrito',
                'items_deleted': 0
            }, status=status.HTTP_200_OK)
