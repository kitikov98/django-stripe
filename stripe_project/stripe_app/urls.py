from django.urls import path
from .views import ItemView, BuyView

urlpatterns = [
    path('item/<int:item_id>/', ItemView.as_view(), name='item'),
    path('buy/<int:item_id>/', BuyView.as_view(), name='buy'),
]