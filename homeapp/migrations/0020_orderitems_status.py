# Generated by Django 3.1.2 on 2020-11-26 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0019_auto_20201126_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
