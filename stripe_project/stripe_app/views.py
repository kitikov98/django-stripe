from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from .models import Item
from .serializers import ItemSerializer
import stripe

class ItemView(APIView):
    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        return render(request, 'item.html', {'item': item})

class BuyView(APIView):
    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)

        stripe.api_key = 'sk_test_51OPPPdEaLvOkTk91fd6AfYfzmgTVuPFu31bwletF6o4gWTTAibxxmXsEHbntPE6cdRK3LyrZtmpf6uQSw1fUqbmf00CENRt9Lx'
        try:
            product = stripe.Product.create(name=item.name, description=item.description)
            price = stripe.Price.create(
                unit_amount=int(item.price * 100),  # Stripe работает с ценами в центах
                currency='usd',
                product=product.id,
            )
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price.id,
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='https://example.com/cancel',
            )
            return Response({'session_id': session.id})
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=400)

