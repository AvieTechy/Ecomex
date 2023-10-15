from datetime import date
today = date.today()

from django.db import models

# Create your models here.

def get_collection_image_filepath(self, filename):
    return 'collections/' + '/collection_image'+ str(self.pk) +'.png'

def default_thumb_path():
    return 'default/'+'thumb_default.png'

class Collections(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=225)
    Thumbnail = models.ImageField(upload_to=get_collection_image_filepath, default=default_thumb_path)
    description = models.TextField(default="No description for this Collection!")
    start_date = models.CharField(default=today.strftime("%B %d, %Y"), max_length=255)
    objects = models.Manager()

    def __str__(self):
        return self.name

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    detail = models.TextField(max_length=225)
    price = models.FloatField()
    brand = models.CharField(max_length=200)
    collection = models.IntegerField(default=0)
    rate = models.IntegerField(max_length=6, default=0)
    Availability = models.BooleanField(default=True)
    Description = models.TextField(default='No Description for this Items')
    objects = models.Manager()


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=225)
    gender = models.CharField(max_length=225)
    products = models.ManyToManyField(Products)
    objects = models.Manager()


class Product_color(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.name

class Product_size(models.Model):
    id = models.AutoField(primary_key=True)
    name_size = models.CharField(max_length=200)

    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.name_size


def get_product_image_filepath(self, filename):
    return 'products/' + '/profile_image'+ str(self.pk) +'.png'

def get_default_product_image():
    return "default/default_product.png"

class Product_image(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.BooleanField(default=False)
    product_image = models.ImageField(upload_to=get_product_image_filepath)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    objects = models.Manager()

    def get_profile_image_filename(self):
        return str(self.product_image)
        # return str(self.product_image)[str(self.product_image).index(str(self.pk) + "/"):]



