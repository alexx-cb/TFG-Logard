from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from rest_framework.views import APIView


class EmailService(APIView):

    @staticmethod
    def send_order_confirmation_email(order, user, rows):
        subject = f"Confirmación de Pedido #{order.id} - LogardBrand"
        html_message = render_to_string('emails/orderConfirmation.html', {
            'order': order,
            'user': user,
            'products': rows
        })
        text_message = f"¡Gracias por tu compra en LogardBrand!\n\n..."

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
