# Generated by Django 4.0.5 on 2022-12-07 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_remove_review_customer_review_cname_review_crole_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='art',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
