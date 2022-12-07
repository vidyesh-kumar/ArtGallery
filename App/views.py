from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as dj_logout, login as dj_login
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import ArtistUpdateForm,CustomerUpdateForm,ArtUpdateForm,OrderUpdateForm,ReviewUpdateForm
from .models import Artist,Customer,Art,Review,Order
from django.conf import settings
import razorpay
import datetime

def index(request):
    return render(request,'index.html')

def logout(request):
    dj_logout(request)
    return redirect("index")
    
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                dj_login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request,"login.html",{"form":form})

def register_request(request):
    form  = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            if int(request.POST.get('group')) > 0:
                user = form.save()
                username = form.cleaned_data.get('username')
                user.groups.add(request.POST.get('group'))
                if user.groups.filter(name="Artist").exists():
                    ArtistUser = Artist(user=user,name=username)
                    ArtistUser.save()
                else:
                    CustomerUser = Customer(user=user,name = username)
                    CustomerUser.save()
                messages.success(request, "New account created: " + username)
                return redirect('login')
            else:
                messages.error(request, "Please Choose an Account Type")
    context = {'form':form}
    return render(request,'register.html',context)

@login_required(login_url='login')
def updateInfo(request):
    if request.user.groups.filter(name="Artist").exists():
        print(request.user.artist.country)
        if request.user.artist.country == "":
            if request.method == 'POST':
                form = ArtistUpdateForm(request.POST,instance=request.user.artist)
                if form.is_valid():
                    form.save()
                    return redirect('reception')
            form = ArtistUpdateForm(instance=request.user.artist)
            return render(request,'updateInfo.html',{'form':form})
        else:
            return redirect('reception')
    else:   
        if request.user.customer.country == "":
            if request.method == 'POST':
                form = CustomerUpdateForm(request.POST,instance=request.user.customer)
                if form.is_valid():
                    form.save()
                    return redirect('reception')
            form = CustomerUpdateForm(instance=request.user.customer)
            return render(request,'updateInfo.html',{'form':form})
        else:
            return redirect('reception')

@login_required(login_url='login')
def reception(request):
    if request.user.groups.filter(name="Artist").exists():
        context = {'group':'Artist'}
        if request.method == 'POST':
            form = ArtUpdateForm(request.POST,request.FILES)
            if form.is_valid():
                art=form.save(commit=False)
                art.artist = request.user.artist
                art.price = int(request.POST.get('price'))*1.2 #20% commission
                if request.POST.get('type') == 'Painting':
                    art.payment = "Onetime Payment"
                    art.lifetime = "Permanent"
                else:
                    art.payment ="Subscription Payment"
                    art.lifetime = "Limited"
                art.save()
    else:
        context = {'group':'Customer'}
    return render(request,'reception.html',context)


@login_required(login_url='login')
def profile(request):
    if request.user.groups.filter(name="Artist").exists():
        context = {'group':'Artist'}
        if request.method == 'POST':
            form = ArtistUpdateForm(request.POST,request.FILES,instance=request.user.artist)
            print(request.FILES)
            if form.is_valid():
                form.save()
                return redirect('profile')
    else:
        context = {'group':'Customer'}
        if request.method == 'POST':
            form = CustomerUpdateForm(request.POST,request.FILES,instance=request.user.customer)
            if form.is_valid():
                form.save()
                return redirect('profile')
    return render(request,'profile.html',context)

count = 0 #GalleryCount
cartcount = 0 #CartCount
@login_required(login_url='login')
def gallery(request):
    global count
    first = Art.objects.values().first()
    if request.method=="POST":
        if 'move' in request.POST:
            if request.POST.get('move') == "next":
                count += 1
            elif request.POST.get('move') == "previous":
                count-=1
            if count < 0:
                count = Art.objects.count()-1
            elif count >= Art.objects.count():
                count = 0
            first = Art.objects.values().all()[count]
        if 'order'in request.POST:
            form = OrderUpdateForm()
            price = request.POST.get('price')
            amount = float(price)*100
            title = request.POST.get('title')
            type = request.POST.get('type')
            url = request.POST.get('img_url')
            lifetime = request.POST.get('lifetime')
            payment_type= request.POST.get('payment')
            desc= request.POST.get('description')
            rating = request.POST.get('rating')
            artist=Artist.objects.filter(name=request.POST.get('artist')).first()
            order = form.save(commit=False)
            if request.user.groups.filter(name="Artist").exists():
                order.cname=request.user.artist.name
                order.crole="Artist"
                order.croleid=request.user.artist.ArtistID
            else:
                order.cname=request.user.customer.name
                order.crole="Customer"
                order.croleid=request.user.customer.CustomerID
            order.Odate = datetime.datetime.now()   
            order.amount = float(amount)
            order.artId = Art.objects.filter(title=title,artist=artist,type=type,description=desc,image_url=url,lifetime=lifetime,payment=payment_type,rating=rating).first()
            order.save()
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY,settings.RAZORPAY_SECRET))
            payment = client.order.create({"amount":float(amount),"currency":"INR","payment_capture":"1"})
            return redirect('order')
        if 'review' in request.POST:
            title = request.POST.get('title')
            type = request.POST.get('type')
            url = request.POST.get('img_url')
            lifetime = request.POST.get('lifetime')
            payment_type= request.POST.get('payment')
            desc= request.POST.get('description')
            rating = request.POST.get('rating')
            price = request.POST.get('price')
            artist=Artist.objects.filter(name=request.POST.get('artist')).first()
            form = ReviewUpdateForm()
            review = form.save(commit=False)
            if request.user.groups.filter(name="Artist").exists():
                review.cname=request.user.artist.name
                review.crole="Artist"
                review.croleid=request.user.artist.ArtistID
            else:
                review.cname=request.user.customer.name
                review.crole="Customer"
                review.croleid=request.user.customer.CustomerID
            review.date = datetime.datetime.now() 
            review.art = Art.objects.filter(title=title,artist=artist,type=type,description=desc,image_url=url,lifetime=lifetime,payment=payment_type,rating=rating,price=price).first()
            review.save()
            return redirect('review')
            
    if first is None:
        return render(request,'galleryclosed.html')
    context={'img_url':first['image_url'],
             'artist':Artist.objects.get(ArtistID=first['artist_id']),
             'title':first['title'],
             'description':first['description'],
             'type':first['type'],
             'price':first['price'],
             'payment':first['payment'],
             'lifetime':first['lifetime'],
             'rating':first['rating']
            }
    return render(request,'gallery.html',context)

@login_required(login_url='login')
def order(request):
    return render(request,'order.html')

def review(request):
    obj = Review.objects.last()
    context = {
        'cname':obj.cname,
        'crole':obj.crole,
        'img_url':obj.art.image_url,
        'rating':obj.rating,
        'title':obj.art.title,
        'artist':obj.art.artist.name
        }
    return render(request,'review.html',context)