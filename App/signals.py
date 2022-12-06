from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Artist,Customer,Art

def Artist_Profile(sender,instance,created,**kwargs):
    if created:
        Artist.objects.create(user=instance,name=instance.username)
post_save.connect(Artist,sender=User)

def Customer_Profile(sender,instance,created,**kwargs):
    if created:
        Customer.objects.create(user=instance,name=instance.username)
post_save.connect(Customer,sender=User)
