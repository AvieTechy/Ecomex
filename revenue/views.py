from django.shortcuts import render, redirect
from django.template.defaulttags import register

from product.models import Product_image
from shop.models import ListOrders


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


def vertify_staff(request):
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        return "ok"
    else:
        return "error"


def revenue_view(request):
    status = "revenue"
    if vertify_staff(request) == "ok":
        images = {}
        revenues = ListOrders.objects.filter(status_order="accept").order_by('-date')
        alltotal = 0
        for revenue in revenues:
            alltotal += float(revenue.subtotal)
            images[revenue] = Product_image.objects.get(product_id=revenue.cart.items, key=True).product_image.url
        context = {'status':status, 'revenues':revenues,'images':images, 'alltotal':alltotal}

        return render(request, 'revenue_view.html', context)
    else:
        return redirect("error404")