from django.db import models
from datetime import datetime

now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


from account.models import Account
from product.models import Products


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    items = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    color = models.CharField(default="", max_length=255)
    size = models.CharField(default="", max_length=255)
    status = models.BooleanField(default=True)
    objects = models.Manager()

class Info_Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    optinal = models.CharField(max_length=255, default="-")
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    objects = models.Manager()

class ListOrders(models.Model):
    id = models.AutoField(primary_key=True)
    info = models.ForeignKey(Info_Order, on_delete=models.CASCADE)
    note = models.CharField(max_length=255, default="-")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    date = models.CharField(max_length=255, default=date_time)
    subtotal = models.CharField(max_length=255)
    status_order = models.CharField(max_length=255, default="pending")
    objects = models.Manager()