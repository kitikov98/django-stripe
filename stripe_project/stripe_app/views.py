from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
import stripe

from .models import Item

stripe.api_key = 'sk_test_51OPPPdEaLvOkTk91fd6AfYfzmgTVuPFu31bwletF6o4gWTTAibxxmXsEHbntPE6cdRK3LyrZtmpf6uQSw1fUqbmf00CENRt9Lx'

def get_buy_session(request, id):
    item = get_object_or_404(Item, id=id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                },
                'unit_amount_decimal': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('item', args=[id])),
        cancel_url=request.build_absolute_uri(reverse('item', args=[id])),
    )
    return JsonResponse({'session_id': session.id})

def get_item_page(request, id):
    item = get_object_or_404(Item, id=id)
    html = f"""
        <h1>{item.name}</h1>
        <p>{item.description}</p>
        <button onclick="redirectToCheckout({id})">Buy</button>
        <script src="https://js.stripe.com/v3/"></script>
        <script>
            function redirectToCheckout(itemId) {{
                fetch('/buy/'+itemId)
                    .then(function(response) {{
                        return response.json();
                    }})
                    .then(function(data) {{
                        var stripe = Stripe('your_stripe_publishable_key');
                        stripe.redirectToCheckout({{
                            sessionId: data.session_id
                        }});
                    }})
                    .catch(function(error) {{
                        console.error('Error:', error);
                    }});
            }}
        </script>
    """
    return HttpResponse(html)

