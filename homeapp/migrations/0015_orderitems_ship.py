# Generated by Django 3.1.2 on 2020-11-22 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0014_auto_20201122_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='ship',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
