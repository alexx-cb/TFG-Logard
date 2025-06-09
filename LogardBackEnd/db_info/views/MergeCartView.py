# views.py (añade esta clase)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from db_info.models import CartItem, Product, Cart


class MergeCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Recibe JSON:
        {
            "items": [
                {"product": 1, "units": 2, "size": "M"},
                {"product": 2, "units": 1, "size": "L"}
            ]
        }
        Agrega o suma las unidades a los items existentes en carrito usuario.
        """
        items = request.data.get('items', [])
        if not isinstance(items, list):
            return Response({"error": "items debe ser una lista"}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener carrito usuario o crear
        cart, _ = Cart.objects.get_or_create(user=request.user)

        for item in items:
            product_id = item.get('product')
            units = int(item.get('units', 1))
            size = item.get('size', 'M')

            # Validar existencia producto
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                continue

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                size=size,
                defaults={'units': units}
            )
            if not created:
                cart_item.units += units
                cart_item.save()

        return Response({"detail": "Carrito fusionado exitosamente"}, status=status.HTTP_200_OK)
