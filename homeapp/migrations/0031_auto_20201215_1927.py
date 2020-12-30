# Generated by Django 3.1.2 on 2020-12-15 13:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0030_ads_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='pictures/advertise')),
                ('website1', models.URLField(blank=True, null=True)),
                ('created1_at', models.DateField(default=datetime.datetime.today, null=True)),
                ('image2', models.ImageField(blank=True, null=True, upload_to='pictures/advertise')),
                ('website2', models.URLField(blank=True, null=True)),
                ('created2_at', models.DateField(default=datetime.datetime.today, null=True)),
                ('image3', models.ImageField(blank=True, null=True, upload_to='pictures/advertise')),
                ('website3', models.URLField(blank=True, null=True)),
                ('created3_at', models.DateField(default=datetime.datetime.today, null=True)),
                ('image4', models.ImageField(blank=True, null=True, upload_to='pictures/advertise')),
                ('website4', models.URLField(blank=True, null=True)),
                ('created4_at', models.DateField(default=datetime.datetime.today, null=True)),
                ('image5', models.ImageField(blank=True, null=True, upload_to='pictures/advertise')),
                ('website5', models.URLField(blank=True, null=True)),
                ('created5_at', models.DateField(default=datetime.datetime.today, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Ads',
        ),
    ]