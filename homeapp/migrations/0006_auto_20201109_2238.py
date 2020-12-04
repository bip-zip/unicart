# Generated by Django 3.1.2 on 2020-11-09 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0005_subcat_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcat',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/subcat'),
        ),
        migrations.AddField(
            model_name='subcat',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/subcat'),
        ),
        migrations.AlterField(
            model_name='subcat',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/subcat'),
        ),
    ]
