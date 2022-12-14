from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

#Artist Model
class Artist(models.Model):
    ArtistID = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,blank=True)
    country = models.CharField(max_length=100,blank=True,null=False)
    email=models.EmailField(max_length=100,blank=True)
    profile_pic = models.ImageField(default='Profile/avatar.png',upload_to='Profile')
    address = models.TextField(max_length=300,blank=True)
    phone = PhoneNumberField(blank=True,null=True)
    rating = models.FloatField(default=0)
    def __str__(self):
        return self.name

class Customer(models.Model):
    CustomerID = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,blank=True)
    country = models.CharField(max_length=100,blank=True,null=False)
    email=models.EmailField(max_length=100,blank=True)
    profile_pic = models.ImageField(default='Profile/avatar.png',upload_to='Profile')
    address = models.TextField(max_length=300,blank=True)
    phone = PhoneNumberField(blank=True,null=True)
    def __str__(self):
        return self.name

class Art(models.Model):
    ArtID = models.AutoField(primary_key=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True)
    description = models.TextField(max_length=300)
    image_url = models.ImageField(upload_to='Art',default='Art/default.jpeg')
    type=models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    price = models.FloatField()
    payment=models.TextField()
    lifetime = models.TextField()
    rating = models.FloatField(default=0)
    sold = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    Odate = models.DateField()
    amount = models.FloatField()
    cname = models.TextField(max_length=100,default="")
    crole = models.TextField(max_length=100,default="")
    croleid = models.IntegerField(default=0)
    artId = models.ForeignKey(Art,on_delete=models.PROTECT)
    paid = models.BooleanField(default=False)
    def __str__(self):
        return self.artId.title
    
class Review(models.Model):
    ReviewID = models.AutoField(primary_key=True)
    date = models.DateField()
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=300,default="")
    cname = models.TextField(max_length=100,default="")
    crole = models.TextField(max_length=100,default="")
    croleid = models.IntegerField(default=0)
    showRev = models.BooleanField(default=False)
    art = models.ForeignKey(Art,on_delete=models.PROTECT)
    def __str__(self):
        return self.art.title
    