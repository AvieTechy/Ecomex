# Generated by Django 2.2.15 on 2022-09-07 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20220907_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info_order',
            name='email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='listorders',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Cart'),
        ),
        migrations.AlterField(
            model_name='listorders',
            name='date',
            field=models.CharField(default='09/07/2022, 12:15:09', max_length=255),
        ),
    ]
