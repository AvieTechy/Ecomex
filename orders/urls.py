from django.urls import path

from orders.views import (
orders_view, order_processing
   )

app_name = 'orders'

urlpatterns = [
    #product
    path('', orders_view, name="orders_view"),
    path('order_processing/', order_processing, name="order_processing"),
]