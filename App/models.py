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
    about = models.TextField(max_length=300,blank=True)
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
    about = models.TextField(max_length=300,blank=True)
    phone = PhoneNumberField(blank=True,null=True)
    def __str__(self):
        return self.name

class Art(models.Model):
    ArtID = models.AutoField(primary_key=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    price = models.FloatField()
    title = models.CharField(max_length=100,blank=True)
    description = models.TextField(max_length=300)
    image_url = models.ImageField(upload_to='Art',default='Art/default.jpeg')
    type=models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title
    
class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    date = models.DateField()
    Quantity = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    def __str__(self):
        return self.OrderID
    
class Review(models.Model):
    ReviewID = models.AutoField(primary_key=True)
    date = models.DateField()
    rating = models.FloatField()
    comment = models.TextField(max_length=300)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    def __str__(self):
        return self.ReviewID
    