# Generated by Django 3.1.2 on 2020-11-26 07:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0018_auto_20201124_1933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitems',
            name='date_added',
        ),
        migrations.AddField(
            model_name='orderitems',
            name='date',
            field=models.DateField(default=datetime.datetime.today, null=True),
        ),
    ]