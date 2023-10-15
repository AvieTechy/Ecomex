from django.shortcuts import render, redirect
from django.conf import settings

from product.models import Products, Product_color, Product_size, Product_image
from shop.models import Cart

DEBUG = False
def vertify_user(request):
    if(request.user.is_authenticated):
        return "ok"
    else: return "error"

def index(request):
    status = "home"
    cart_cnt = 0
    if vertify_user(request) == "ok":
        cart_cnt = Cart.objects.filter(user=request.user, status=True).count()
    context = {}
    context['debug_mode'] = settings.DEBUG
    context['debug'] = DEBUG
    context['status'] = status
    context['cart_cnt'] = cart_cnt
    return render(request, "index.html", context)

def error404(request):
    context = {}
    context['debug_mode'] = settings.DEBUG
    context['debug'] = DEBUG
    return render(request, "error404.html", context)

