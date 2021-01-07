# Generated by Django 3.1.2 on 2021-01-06 10:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0004_auto_20210104_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 6, 15, 50, 59, 276943), null=True),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=200, null=True)),
                ('date', models.DateField(default=datetime.datetime(2021, 1, 6, 15, 50, 59, 276943), null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='homeapp.patron')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='homeapp.product')),
            ],
        ),
    ]