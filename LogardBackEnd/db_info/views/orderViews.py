from datetime import timezone, datetime

from django.db import transaction
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from db_info.models import Order, RowsOrder
from db_info.payments.paypalService import PayPalService
from db_info.serializers.OrderSerializer import CreateOrderSerializer


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = request.user
        data= serializer.validated_data
        cart_items = request.data.get('cart_items',[])
        total = sum([item['total_price'] for item in cart_items])
        currency = "EUR"

        with transaction.atomic():
            now = datetime.now(timezone.utc)
            order = Order.objects.create(
                address=data['address'],
                locality=data['locality'],
                province=data['province'],
                cost=total,
                status="Payment Pending",
                date = now.date(),
                time=now.time(),
                user=user,
            )
            for item in cart_items:
                RowsOrder.objects.create(
                    units= item['units'],
                    size=item['size'],
                    order=order,
                    product_id=item['product'],
                )

            paypal = PayPalService()
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

            return Response({"approval_url": approval_url, "order_id": order.id})

class PaypalExecuteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        order_id = request.GET.get('order_id')

        paypal = PayPalService()
        payment = paypal.execute_payment(payment_id, payer_id)

        order = Order.objects.get(id=order_id)
        order.status = 'Paid'
        order.save()

        return Response({"status": "success" , "payment_id": payment_id, "order_id": order_id})

class PayPalCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_id = request.GET.get('order_id')
        order = Order.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
        return Response({"status": "cancelled" , "order_id": order_id})