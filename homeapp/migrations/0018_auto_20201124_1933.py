# Generated by Django 3.1.2 on 2020-11-24 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0017_orderitems_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
    ]