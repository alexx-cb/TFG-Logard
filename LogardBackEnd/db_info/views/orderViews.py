from datetime import timezone, datetime

from django.db import transaction
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from db_info.Services.EmailService import EmailService
from db_info.models import Order, RowsOrder, Cart, Product
from db_info.payments.paypalService import PayPalService
from db_info.serializers.OrderSerializer import CreateOrderSerializer


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        data = serializer.validated_data
        cart_items = request.data.get('cart_items', [])

        total_with_discount = 0
        subtotal_without_discount = 0

        for item in cart_items:
            product_id = item['product']
            units = item['units']

            try:
                product = Product.objects.get(id=product_id)

                base_price_per_unit = product.price


                item_subtotal = base_price_per_unit * units
                subtotal_without_discount += item_subtotal

                # Aplicar descuento si existe
                if product.discount > 0:
                    discount_amount = (item_subtotal * product.discount) / 100
                    item_total_with_discount = item_subtotal - discount_amount
                else:
                    item_total_with_discount = item_subtotal

                total_with_discount += item_total_with_discount

            except Product.DoesNotExist:
                return Response({"message": "Product may not exists"})

        total = total_with_discount
        total_discount = subtotal_without_discount - total_with_discount

        currency = "EUR"

        with transaction.atomic():
            now = datetime.now(timezone.utc)
            order = Order.objects.create(
                address=data['address'],
                locality=data['locality'],
                province=data['province'],
                cost=total,
                status="Payment Pending",
                date=now.date(),
                time=now.time(),
                user=user,
            )
            for item in cart_items:
                RowsOrder.objects.create(
                    units=item['units'],
                    size=item['size'],
                    order=order,
                    product_id=item['product'],
                )

            paypal = PayPalService()

            # CHANGE IN PRODUCTION FOR REDIRECT TO MY APP NO TO LOCALHOST:8000
            return_url = request.build_absolute_uri(reverse('paypal-execute')) + f"?order_id={order.id}"
            cancel_url = request.build_absolute_uri(reverse('paypal-cancel')) + f"?order_id={order.id}"
            payment = paypal.create_payment(total, currency, return_url, cancel_url)

            for link in payment['links']:
                if link['rel'] == 'approval_url':
                    approval_url = link['href']
                    break
            else:
                raise Exception('No Approval URL found')

            order.status = 'Waiting PayPal payment'
            order.save()

            return Response({
                "approval_url": approval_url,
                "order_id": order.id,
                "subtotal": subtotal_without_discount,
                "total_discount": total_discount,
                "total": total
            })


class PaypalExecuteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        order_id = request.GET.get('order_id')

        if not all([payment_id, payer_id, order_id]):
            return Response({"error": "Missing required parameters"}, status=400)

        try:
            order = Order.objects.get(id=order_id, user=request.user)

            if order.status == 'Paid':
                return Response({"error": "Order already paid"}, status=400)

            paypal = PayPalService()
            payment = paypal.execute_payment(payment_id, payer_id)

            order.status = 'Paid'
            order.save()

            user = request.user
            rows = list(order.rowsorder_set.select_related('product').all())
            email_sent = EmailService.send_order_confirmation_email(order, user, rows)

            Cart.objects.filter(user=request.user).delete()

            return Response({
                "status": "success",
                "payment_id": payment_id,
                "order_id": order_id,
                "message": "Payment successful and cart cleared"
            })

        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
        except Exception as e:
            print(f"PayPal execution error: {str(e)}")
            return Response({"error": str(e)}, status=500)

class PayPalCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_id = request.GET.get('order_id')
        order = Order.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
        return Response({"status": "cancelled" , "order_id": order_id})