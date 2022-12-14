from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as dj_logout, login as dj_login
from .forms import FilterArtForm, NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .forms import ArtistUpdateForm,CustomerUpdateForm,ArtUpdateForm,OrderUpdateForm,ReviewUpdateForm,ArtRatingForm,ArtistRatingForm
from .models import Artist,Customer,Art,Review,Order
from django.conf import settings
import razorpay
import datetime
country = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

#Home Page
def index(request):
    context={}
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Artist").exists():
            context = {"usertype":request.user.artist}
        else:
            context = {"usertype":request.user.customer}
    return render(request,'index.html',context)

#Logout Function

def logout(request):
    dj_logout(request)
    return redirect("login")
 
#Login Page 
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                dj_login(request, user)
                return redirect('updateInfo')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request,"login.html")

#Register Page
def register_request(request):
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
    return render(request,'register.html')

#Create Profile Page
@login_required(login_url='login')
def updateInfo(request):
    global country
    if request.user.groups.filter(name="Artist").exists():
        print(request.user.artist.country)
        if request.user.artist.country == "":
            if request.method == 'POST':
                form = ArtistUpdateForm(request.POST,request.FILES,instance=request.user.artist)
                if form.is_valid():
                    form.save()
                    return redirect('index')
            return render(request,'updateInfo.html',{'countries':country})
        else:
            return redirect('index')
    else:   
        if request.user.customer.country == "":
            if request.method == 'POST':
                form = CustomerUpdateForm(request.POST,request.FILES,instance=request.user.customer)
                if form.is_valid():
                    form.save()
                    return redirect('index')
            form = CustomerUpdateForm(instance=request.user.customer)
            return render(request,'updateInfo.html',{'countries':country})
        else:
            return redirect('index')

#Reception Page
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


#Profile Page
@login_required(login_url='login')
def profile(request):
    if request.user.groups.filter(name="Artist").exists():
        context = {'group':'Artist',
                   'countries':country,
                   'range':range(1,6)
                 }
        if request.method == 'POST':
            form = ArtistUpdateForm(request.POST,request.FILES,instance=request.user.artist)
            print(request.FILES)
            if form.is_valid():
                form.save()
                return redirect('profile')
    else:
        context = {'group':'Customer',
                   'countries':country,
                   'range':range(1,6)
                   }
        if request.method == 'POST':
            form = CustomerUpdateForm(request.POST,request.FILES,instance=request.user.customer)
            if form.is_valid():
                form.save()
                return redirect('profile')
    return render(request,'profile.html',context)

#Gallery Variables
count = 0 #GalleryCount
filterdict = {} #Filter Dictionary
#Gallery Page
@login_required(login_url='login')
def gallery(request):
    global count
    global filterdict
    context = {}
    filterdict={}
    first = Art.objects.filter(sold=False).values().first()
    if request.method=="POST":
        if 'filter' in request.POST:
            form = FilterArtForm(request.POST)
            if form.is_valid():
                f_rating = form.cleaned_data.get('rating')
                f_start_price = form.cleaned_data.get('price')
                f_type = form.cleaned_data.get('type')
                if f_rating is not None:
                    filterdict['rating__gte'] = f_rating 
                if f_start_price is not None:
                    filterdict['price__gte'] = f_start_price
                if f_type != '':
                    filterdict['type'] = f_type
                try:
                    first = Art.objects.filter(sold=False).filter(**filterdict).values()[count]  
                except:
                    return redirect('filtererror')    
        if 'move' in request.POST:
            if request.POST.get('move') == "next":
                count += 1
            elif request.POST.get('move') == "previous":
                count-=1
            if count < 0:
                count = Art.objects.filter(sold=False).filter(**filterdict).count()-1
            elif count >= Art.objects.filter(sold=False).filter(**filterdict).count():
                count = 0
            first = Art.objects.filter(sold=False).filter(**filterdict).values()[count]
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
            order.artId = Art.objects.filter(title=title,artist=artist,type=type,description=desc,image_url=url,lifetime=lifetime,payment=payment_type,rating=rating,sold=False).first()
            order.save()
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
            review.art = Art.objects.filter(title=title,artist=artist,type=type,description=desc,image_url=url,lifetime=lifetime,payment=payment_type,rating=rating,price=price,sold=False).first()
            review.save()
            return redirect('review')
    if request.user.groups.filter(name="Artist").exists():
        context['group']='Artist'
    else:
        context['group']='Customer'
    if first is None:
        return render(request,'galleryclosed.html',context)
    
    context['img_url']=first['image_url']
    context['artist']=Artist.objects.get(ArtistID=first['artist_id'])
    context['title']=first['title']
    context['description']=first['description']
    context['type']=first['type']
    context['price']=first['price']
    context['payment']=first['payment']
    context['lifetime']=first['lifetime']
    context['rating']=first['rating']
    context['range']=range(1,6)
    return render(request,'gallery.html',context)

#Order Page
@login_required(login_url='login')
def order(request):
    obj = Order.objects.last()
    payment={}
    if request.method == "POST":
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY,settings.RAZORPAY_SECRET))
        payment = client.order.create({"amount":obj.amount,"currency":"INR","payment_capture":"1"})
        orderObj = Order.objects.get(OrderID=obj.OrderID)
        orderObj.paid=True
        orderObj.save()
        Order.objects.filter(paid=False).delete()
        if obj.artId.payment == "Onetime Payment":
            artObj = Art.objects.get(ArtID=obj.artId.ArtID)
            artObj.sold=True
            artObj.save()
        return redirect('success')
    context = { 'payment':payment,
                'img_url':obj.artId.image_url,
                'artist':obj.artId.artist,
                'title':obj.artId.title,
                'price':obj.amount,
                'amount':obj.amount/100,
                'payment_type':obj.artId.payment,
                'lifetime':obj.artId.lifetime,
                'cname':obj.cname,
                'key':settings.RAZORPAY_KEY,
                'range':range(1,6)
                }
    if request.user.groups.filter(name="Artist").exists():
        context['group']='Artist'
    else:
        context['group']='Customer'    
    return render(request,'order.html',context)

#Review Page
@login_required(login_url='login')
def review(request):
    obj = Review.objects.last()
    if request.method == "POST":
        form = ReviewUpdateForm(request.POST,instance=obj)
        if form.is_valid():
            object=form.save(commit=False)
            object.showRev = True
            object.save()
            Review.objects.filter(showRev=False).delete()
            Artform = ArtRatingForm(instance=obj.art)
            artobj= Artform.save(commit=False)
            artobj.rating = round(Review.objects.filter(art=obj.art).aggregate(Avg('rating'))['rating__avg'],2)
            artobj.save()
            Artistform = ArtistRatingForm(instance=obj.art.artist)
            artistobj= Artistform.save(commit=False)
            artistobj.rating = round(Art.objects.filter(artist=obj.art.artist).aggregate(Avg('rating'))['rating__avg'],2)
            artistobj.save()
    comments = Review.objects.filter(art=obj.art,showRev=True)
    context = {
        'cname':obj.cname,
        'crole':obj.crole,
        'img_url':obj.art.image_url,
        'rating':obj.art.rating,
        'title':obj.art.title,
        'artist':obj.art.artist.name,
        'comments': comments,
        'range':range(1,6)
        }     
    return render(request,'review.html',context)

#Payment Success Page
@login_required(login_url='login')
def success(request):
    return render(request,'success.html')

#Filtererror Page
@login_required(login_url='login')
def filtererror(request):
    return render(request,'filtererror.html')

