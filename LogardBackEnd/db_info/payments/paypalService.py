import paypalrestsdk
from django.conf import settings


class PayPalService:
    def __init__(self):
        paypalrestsdk.configure({
            "mode":settings.PAYPAL_MODE,
            "client_id":settings.PAYPAL_CLIENT_ID,
            "client_secret":settings.PAYPAL_CLIENT_SECRET,
        })

    def create_payment(self, total, currency, return_url, cancel_url):
        payment = paypalrestsdk.Payment({
            "intent":"sale",
            "payer":{"payment_method":"paypal"},
            "redirect_urls":{
                "return_url":return_url,
                "cancel_url":cancel_url
            },
            "transactions":[{
                "amount":{
                    "total":f"{total:.2f}",
                    "currency":currency,
                },
                "description":"Buy in Logard"
            }]
        })
        if payment.create():
            return payment
        else:
            raise Exception(payment.error)

    def execute_payment(self, payment_id, payer_id):
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id":payer_id}):
            return payment
        else:
            raise Exception(payment.error)