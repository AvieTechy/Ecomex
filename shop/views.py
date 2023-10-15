from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from product.models import Products, Product_color, Product_size, Product_image, Collections
from django.template.defaulttags import register

from shop.models import Cart, ListOrders, Info_Order


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


def vertify_user(request):
    if (request.user.is_authenticated):
        return "ok"
    else:
        return "error"


def shop_view(request):
    status = "shop"
    cart_cnt = 0
    if vertify_user(request) == "ok":
        cart_cnt = Cart.objects.filter(user=request.user, status=True).count()
    context, colors, sizes, images = {}, {}, {}, {}
    products = []
    if (Products.objects.all().count() != 0):
        products = Products.objects.all()
        for product in products:
            colors[product] = Product_color.objects.filter(product_id=product)
            sizes[product] = Product_size.objects.filter(product_id=product)
            for i in Product_image.objects.filter(product_id=product):
                print(i.key)
            print(Product_image.objects.filter(product_id=product).count())
            image = Product_image.objects.get(product_id=product, key=True)

            images[product] = image.product_image.url
    context = {'status': status, 'colors': colors, 'sizes': sizes, 'images': images, 'products': products,
               'cart_cnt': cart_cnt}
    print(cart_cnt)
    return render(request, 'shop.html', context)


def detail(request, pro_id):
    status = "shop"
    cart_cnt = 0
    if vertify_user(request) == "ok":
        cart_cnt = Cart.objects.filter(user=request.user, status=True).count()

    ID = pro_id
    thumbs = {}
    urls = {}
    rate_rel = {}
    orate_rel = {}
    product = Products.objects.get(id=pro_id)
    images = Product_image.objects.filter(product_id=product)
    colors = Product_color.objects.filter(product_id=product)
    sizes = Product_size.objects.filter(product_id=product)
    related = Products.objects.filter(collection=product.collection)
    for rel in related:
        image = Product_image.objects.get(product_id=rel, key=True)
        thumbs[rel] = image
        urls[rel] = image.product_image.url
        rate_rel[rel] = [1] * rel.rate
        orate_rel[rel] = [1] * (5 - rel.rate)
    rate = [1] * product.rate
    orate = [1] * (5 - product.rate)

    print(related)
    print("rel")
    context = {'status': status, 'ID': ID, 'product': product, 'images': images, 'rate': rate,
               'orate': orate, 'colors': colors, 'sizes': sizes, 'related': related, 'thumbs': thumbs,
               'urls': urls, 'rate_rel': rate_rel, 'orate_rel': orate_rel, 'cart_cnt': cart_cnt}

    return render(request, "detail.html", context)


def add_order(request):
    status = "shop"
    cart_cnt = 0
    if vertify_user(request) == "ok":
        pro_id = request.POST.get('pro_id')
        qty = request.POST.get('qty')
        color_choice = request.POST.get('color_choice')
        size = request.POST.get('size')

        product = Products.objects.get(id=pro_id)
        if Cart.objects.filter(user=request.user, items=product, color=color_choice, size=size,
                               status=True).count() == 0:
            cart = Cart(user=request.user, items=product, color=color_choice, size=size, status=True)
            cart.save()
        cart = Cart.objects.get(user=request.user, items=product, color=color_choice, size=size, status=True)
        cart.quantity = qty
        cart.save()
        cart_cnt = Cart.objects.filter(user=request.user, status=True).count()
        context = {'status': status, 'cart_cnt': cart_cnt}
        messages.success(request, 'Added in your cart!')
        return redirect("shop:detail", pro_id)
    else:
        messages.warning(request, 'Please Login First!')
        return redirect("login")


def my_cart(request):
    status = "shop"
    cart_cnt = 0
    if vertify_user(request) == "ok":
        orders = []
        thumbs = {}
        total = {}
        subtotal = 0

        orders = Cart.objects.filter(user=request.user, status=True)
        cart_pend = Cart.objects.filter(user=request.user, status=False)
        pends = []
        cnt = {}
        para = 0
        for cart_p in cart_pend:
            if ListOrders.objects.filter(cart=cart_p).count() == 1:
                ord = ListOrders.objects.get(cart=cart_p)
                pends.append(ord)
                para += 1
                cnt[ord] = para

        for order in orders:
            thumb = Product_image.objects.get(product_id=order.items, key=True)
            thumbs[order] = thumb.product_image.url
            total[order] = order.items.price * order.quantity
            subtotal += total[order]

        cart_cnt = Cart.objects.filter(user=request.user, status=True).count()
        context = {'cart_cnt': cart_cnt, 'status': status, 'orders': orders, 'thumbs': thumbs,
                   'total': total, 'subtotal': subtotal, 'pends': pends, 'cnt':cnt}
        return render(request, "my_cart.html", context)
    else:
        messages.warning(request, 'Please Login First!')
        return redirect("login")


def update_cart(request):
    status = "shop"
    cart_cnt = 0
    if vertify_user(request) == "ok":
        print("vao")
        print(request.POST)
        if request.POST:
            try:
                items = Cart.objects.filter(user=request.user, status=True)
                for item in items:
                    qty = 0
                    if str(item.id) in request.POST:
                        qty = request.POST[str(item.id)]
                    print(qty)
                    if qty == 0 or qty == '0':
                        Cart.objects.get(id=item.id).delete()
                    else:
                        item.quantity = qty
                        item.save()
                messages.success(request, 'Updated Your Cart!')

                return redirect("shop:my_cart")
            except:
                messages.error(request, 'There was an error while updating your cart. Please try again!')
                return redirect("shop:my_cart")

    else:
        messages.warning(request, 'Please Login First!')
        return redirect("login", {'cart_cnt': cart_cnt})


def checkout(request):
    status = "shop"
    cart_cnt = 0
    total = {}
    subtotal = 0

    if vertify_user(request) == "ok":
        cart_cnt = Cart.objects.filter(user=request.user, status=True).count()

        if cart_cnt == 0:

            messages.info(request, "Nothing is in your cart at the moment. Pick some from this list!")
            return redirect("shop:shop_view")
        else:
            orders = Cart.objects.filter(user=request.user, status=True)
            for order in orders:
                total[order] = order.items.price * order.quantity
                subtotal += total[order]
            context = {'orders': orders, 'total': total, 'subtotal': subtotal, 'cart_cnt': cart_cnt,
                       'status': status}
            return render(request, 'checkout.html', context)

    else:
        messages.warning(request, 'Please Login First!')
        return redirect("login", {'cart_cnt': cart_cnt})


def send_order(request):
    status = "shop"
    cart_cnt = 0
    if vertify_user(request) == "ok":
        if request.POST:
            # require
            name = request.POST['cus_name']
            email = request.user.email
            phone = request.POST['phone']
            city = request.POST['city']
            country = request.POST['country']
            street = request.POST['street']
            postcode = request.POST['postcode']

            optinal = "-"
            note = "-"
            if request.POST['optinal'] != '':
                optinal = request.POST.get('optinal')
            if request.POST['note'] != '':
                note = request.POST.get('note')

            print(name, email, phone, postcode, city, country, street, optinal, note)
            try:
                carts = Cart.objects.filter(user=request.user, status=True)
                for cart in carts:
                    subtotal = cart.items.price * cart.quantity
                    cart.status = False
                    if Info_Order.objects.filter(user=request.user, name=name, email=email, phone=phone,
                                                 optinal=optinal, city=city, country=country, street=street,
                                                 postcode=postcode).count() == 0:
                        print("vao")
                        info = Info_Order(user=request.user, name=name, email=email, phone=phone, optinal=optinal,
                                          city=city, country=country, street=street, postcode=postcode)
                        info.save()

                    info = Info_Order.objects.get(user=request.user, name=name, email=email, phone=phone,
                                                  optinal=optinal, city=city,
                                                  country=country, street=street, postcode=postcode)
                    print(info)
                    print("success info")
                    list_orders = ListOrders(info=info, note=note, cart=cart, subtotal=subtotal)
                    list_orders.save()
                    print(list_orders)
                    print("success list_orders")
                    # info.save()
                    cart.save()
                messages.success(request, 'Your order is pending!')
                return redirect("shop:my_cart")
            except:
                messages.error(request, 'Failed in Sending your checkout!')
                return redirect("shop:checkout")

    else:
        messages.warning(request, 'Please Login First!')
        return redirect("login", {'cart_cnt': cart_cnt})

