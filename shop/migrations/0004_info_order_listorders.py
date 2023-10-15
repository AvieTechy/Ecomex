# Generated by Django 2.2.15 on 2022-09-06 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0003_cart_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info_Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('optinal', models.CharField(default='-', max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ListOrders',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('note', models.CharField(default='-', max_length=255)),
                ('date', models.CharField(default='09/07/2022, 01:36:01', max_length=255)),
                ('subtotal', models.CharField(max_length=255)),
                ('status_order', models.CharField(default='pending', max_length=255)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Cart')),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Info_Order')),
            ],
        ),
    ]
