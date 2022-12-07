# Generated by Django 4.0.5 on 2022-12-07 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_remove_order_cart_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='customer',
        ),
        migrations.AddField(
            model_name='review',
            name='cname',
            field=models.TextField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='review',
            name='crole',
            field=models.TextField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='review',
            name='croleid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
