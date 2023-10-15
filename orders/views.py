from django.contrib import messages
from django.core.mail import message
from django.shortcuts import render, redirect

# Create your views here.
from django.template.defaulttags import register

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

def orders_view(request):
    status = "orders"
    if vertify_staff(request) == "ok":
        orders = ListOrders.objects.filter(status_order="pending").order_by('-date')
        context = {'orders':orders, 'status':status}
        return render(request, "orders_view.html", context)
    else:
        return redirect("error404")

def order_processing(request):
    status = "orders"
    if vertify_staff(request) == "ok":
        if request.POST:
            ID = request.POST.get('id')
            option = request.POST.get('options')
            try:
                order = ListOrders.objects.get(id=ID)
                order.status_order = option
                order.save()
                messages.success(request, 'Approved the order with ID: #' + ID + '!')
                return redirect("orders:orders_view")

            except:
                messages.error(request, 'Failed in processing the order with ID: #'+ID+'!')
                return redirect("orders:orders_view")
    else:
        return redirect("error404")