# Generated by Django 3.1.2 on 2020-11-22 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0013_auto_20201122_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]
