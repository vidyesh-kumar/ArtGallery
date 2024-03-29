from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Artist,Customer,Art,Order,Review

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ArtistUpdateForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name','country','email','address','phone',"profile_pic"]

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','country','email','address','phone','profile_pic']

class ArtUpdateForm(forms.ModelForm):
    class Meta:
        model = Art
        fields = ['title','price','description','type','image_url']

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['Odate','amount','cname','croleid','crole','artId']
    
class ReviewUpdateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','comment']

class ArtRatingForm(forms.ModelForm):
    class Meta:
        model = Art
        fields = ['rating']
class ArtistRatingForm(forms.ModelForm):
    class Meta:
        model = Art
        fields = ['rating']
    

class FilterArtForm(forms.Form):
    type = forms.CharField(required=False)
    rating = forms.FloatField(required=False)
    price = forms.FloatField(required=False)
