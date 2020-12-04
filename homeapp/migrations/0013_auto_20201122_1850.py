# Generated by Django 3.1.2 on 2020-11-22 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0012_patron_cpassword'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=1, null=True)),
                ('price', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='homeapp.patron')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='homeapp.product')),
            ],
        ),
        migrations.RenameModel(
            old_name='Order',
            new_name='Orders',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
