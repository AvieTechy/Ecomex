from django.urls import path

from shop.views import (
    shop_view, detail, add_order, my_cart, update_cart, checkout,
    send_order
    )

app_name = 'shop'

urlpatterns = [
    #shop
	path('', shop_view, name="shop_view"),
	path('detail/<str:pro_id>', detail, name="detail"),
	path('add_order', add_order, name="add_order"),
	path('my_cart', my_cart, name="my_cart"),
	path('update_cart', update_cart, name="update_cart"),
    path('checkout', checkout, name="checkout"),
    path('send_order', send_order, name="send_order"),
]