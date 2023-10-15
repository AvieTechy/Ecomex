from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import include

from account.views import (
    register_view, login_view, logout_view, manage_view
)
from EcomexApp.views import (
    index, error404,
)

urlpatterns = [
	path('admin/', admin.site.urls),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('manage/', manage_view, name="manage"),

    path('', index, name="index"),
    path('error404/', error404, name="error404"),

    #snippets
    path('products/', include('product.urls', namespace='product')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('revenue/', include('revenue.urls', namespace='revenue')),

] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

