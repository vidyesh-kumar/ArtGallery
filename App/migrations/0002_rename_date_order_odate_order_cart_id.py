# Generated by Django 4.0.5 on 2022-12-06 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date',
            new_name='Odate',
        ),
        migrations.AddField(
            model_name='order',
            name='Cart_id',
            field=models.IntegerField(default=0),
        ),
    ]