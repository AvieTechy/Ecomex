from django.urls import path

from product.views import (
    product_items, add_product, upload_product, dropzone_image, option_select, edit_product,
    collections, add_collection, upload_collection, upload_thumbnail_collection, collection_details
)

app_name = 'product'

urlpatterns = [
    #product

	path('', product_items, name="product_items"),
	path('add_product/', add_product, name="add_product"),
	path('upload_product/', upload_product, name="upload_product"),
    path('edit_product/<str:pro_id>', edit_product, name="edit_product"),
    path('items/', product_items, name="product_items"),

    path('dropzone_image/', dropzone_image, name="dropzone_image"),
    path('option_select/', option_select, name="option_select"),

    #collections
    path('collections/', collections, name="collections"),
	path('add_collection/', add_collection, name="add_collection"),
    path('upload_collection/', upload_collection, name="upload_collection"),
    path('upload_thumbnail_collection/', upload_thumbnail_collection, name="upload_thumbnail_collection"),
    path('collections/<str:coll_id>', collection_details, name="collection_details"),

]