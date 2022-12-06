# Generated by Django 4.0.5 on 2022-10-25 10:03

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_alter_artist_country_alter_customer_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]
