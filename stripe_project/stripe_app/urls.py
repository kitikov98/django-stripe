from django.urls import path

from .views import get_buy_session, get_item_page

urlpatterns = [
    path('buy/<int:id>/', get_buy_session, name='buy'),
    path('item/<int:id>/', get_item_page, name='item'),
]

