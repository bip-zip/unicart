# Generated by Django 3.1.2 on 2020-11-11 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0007_auto_20201110_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sub_category',
        ),
        migrations.AddField(
            model_name='product',
            name='pslug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='homeapp.subcat'),
        ),
    ]
