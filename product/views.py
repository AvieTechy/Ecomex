import json


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from product.models import Products, Product_image, Product_color, Product_size, Collections

from django.template.defaulttags import register


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


def vertify_staff(request):
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        return "ok"
    else:
        return "error"


    # Collections
def collections(request):
    cart_cnt = 0
    if vertify_staff(request) == "ok":
        status = "products"
    else:
        status = "collection"
    coll_cnt = Collections.objects.all().count()
    colls = []
    if coll_cnt != 0:
        colls = Collections.objects.all().order_by('-id')

    return render(request, "staffs/collections.html", {'status': status, 'coll_cnt': coll_cnt, 'colls': colls, 'cart_cnt': cart_cnt})

def collection_details(request, coll_id):
    status = "products"
    if vertify_staff(request) == "error":
        return redirect("error404")

    coll = Collections.objects.get(id=coll_id)
    product_list = Products.objects.filter(collection=coll_id)
    return render(request, "staffs/collection_detail.html", {'status': status, 'coll': coll, 'product_list':product_list})


def add_collection(request):
    status = "products"
    if vertify_staff(request) == "error":
        return redirect("error404")

    return render(request, "staffs/add_collection.html",{"status": status})

def upload_collection(request):
    if vertify_staff(request) == "error":
        return redirect("error404")

    status = "products"
    if request.method == "POST":

        title = request.POST.get('title')
        description = request.POST.get('description')
        print(title)
        print(description)
        try:
            coll = Collections(name=title)
            coll.save()
            print("oke")
            if description != "":
                coll.description = description
            coll.save()
            print("success coll")
            ID = coll.id
            print(ID)
            result = "perfect"
            message = "Your profile has been updated"

            context = {"result": result, "message": message, "ID": ID, }
            return HttpResponse(
                json.dumps(context),
                content_type="application/json"
            )
        except:
            result = "failed"
            message = "the process is failed!"
            ID = "0"
            context = {"result": result, "message": message, "ID": ID, }

            return HttpResponse(
                json.dumps(context),
                content_type="application/json"
            )
    return redirect("collections")

def upload_thumbnail_collection(request):
    if vertify_staff(request) == "error":
        return redirect("error404")

    result = "result"
    message = "message"
    if request.method == "POST":
        id = request.POST.get('pid')
        coll = Collections.objects.get(id=id)
        try:
            thumb_img = ""
            print(request.FILES)
            for image in request.FILES:
                thumb_img = request.FILES[image]

            if thumb_img != "":
                coll.Thumbnail = thumb_img
                coll.save()
                print("success thumb")
            return HttpResponse({}, content_type="application/json")
        except:
            return HttpResponse('failed')


    # products
def product_items(request):
    status = "products"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        products = []
        colors = {}
        sizes = {}
        images = {}
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
        print(products, colors, sizes)
        return render(request, 'staffs/product_items.html',
                      {'status': status, 'products': products, 'colors': colors, 'sizes': sizes, 'images': images})
    else:
        return redirect("error404")


def add_product(request):
    status = "products"
    if vertify_staff(request) == "error":
        return redirect("error404")

    colls = []
    if (Collections.objects.all().count() != 0):
        colls = Collections.objects.all()
    return render(request, 'staffs/add.html', {'status': status, 'colls': colls})

def edit_product(request, pro_id):
    status = "products"
    if vertify_staff(request) == "error":
        return redirect("error404")

    product = Products.objects.get(id = pro_id)
    collection = Collections.objects.get(id = product.collection)
    coll_id = collection.id
    coll_name = collection.name
    colls = Collections.objects.all()
    images = Product_image.objects.filter(product_id = product)
    return render(request, "staffs/edit_items.html", {'status': status, 'product': product, 'images': images,
                                                      'coll_id': coll_id, 'coll_name': coll_name,'colls': colls})

def upload_product(request):
    status = "products"
    if request.method == "POST":

        title = request.POST.get('title')
        category = request.POST.get('category')
        gender = request.POST.get('gender')
        collection = request.POST.get('collection')
        brand = request.POST.get('brand')
        detail = request.POST.get('detail')
        description = request.POST.get('description')
        price = request.POST.get('prices')

        try:
            product = Products(name=title, detail=detail, price=price, Description=description, collection=collection, brand=brand)
            product.save()

            ID = product.id
            result = "perfect"
            message = "Your profile has been updated"

            context = {"result": result, "message": message, "ID": ID, }
            return HttpResponse(
                json.dumps(context),
                content_type="application/json"
            )
        except:
            result = "failed"
            message = "the process is failed!"
            ID = "0"
            context = {"result": result, "message": message, "ID": ID, }

            return HttpResponse(
                json.dumps(context),
                content_type="application/json"
            )
    return render(request, 'staffs/add.html', {'status': status})

def dropzone_image(request):
    result = "result"
    message = "message"
    if request.method == "POST":
        id = request.POST.get('pid')
        product = Products.objects.get(id=id)
        try:
            print(request.FILES)

            for image in request.FILES:
                product_img = Product_image(product_image=request.FILES[image], product_id=product)
                print(product_img.key)
                product_img.save()

            for p in Product_image.objects.filter(product_id=product):
                p.key = True
                p.save()
                break

            return HttpResponse({}, content_type="application/json")
        except:
            return HttpResponse('failed')

    return HttpResponse(
        json.dumps({"result": result, "message": message}),
        content_type="application/json"
    )


def option_select(request):
    result = "result"
    message = "message"

    if request.POST:
        id = request.POST.get('pid')
        unit = request.POST.get('unit')

        colors = request.POST.getlist('colors[]')
        sizes = request.POST.getlist('sizes[]')
        size_shoes = request.POST.getlist('size_shoes[]')

        print(colors)
        print(size_shoes)
        print(sizes)
        print(id)
        product = Products.objects.get(id=id)
        try:
            print("vao")
            if colors != []:
                print("vao colors")
                for color in colors:
                    print(color)
                    print(product)
                    Product_color.objects.create(name=color, product_id=product)
                    print("save")
            print("success color")
            if size_shoes != []:
                print("vao size shoes")
                for size in size_shoes:
                    product_size = Product_size(name=str(size + unit), product_id=product)
                    product_size.save()
            elif sizes != []:
                print("vao size")
                for size in sizes:
                    product_size = Product_size(name_size=size, product_id=product)
                    product_size.save()
            print("success size")
        except:
            return HttpResponse('failed1')

        return redirect("product:add_product")

    return HttpResponse(
        json.dumps({"result": result, "message": message}),
        content_type="application/json"
    )
