from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path("register/", views.register_request, name="register"),
    path("updateInfo/", views.updateInfo, name="updateInfo"),
    path("reception/", views.reception, name="reception"),
    path("profile/", views.profile, name="profile"),
    path("gallery/", views.gallery, name="gallery"),
    path("order/", views.order, name="order"),
    path("review/", views.review, name="review"),
    path("success/", views.success, name="success"),
    path("filter/", views.filtererror, name="filtererror")
]