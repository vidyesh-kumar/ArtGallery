# Generated by Django 4.0.5 on 2022-12-11 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_order_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='art',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]