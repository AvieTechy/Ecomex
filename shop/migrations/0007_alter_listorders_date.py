# Generated by Django 4.1.3 on 2023-10-15 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20220907_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listorders',
            name='date',
            field=models.CharField(default='10/15/2023, 12:21:48', max_length=255),
        ),
    ]
