# Generated by Django 4.0.5 on 2022-12-07 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_remove_order_artist_remove_order_customer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='Cart_id',
        ),
    ]
