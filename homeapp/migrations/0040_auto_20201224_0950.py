# Generated by Django 3.1.2 on 2020-12-24 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0039_orderitems_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='created',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]