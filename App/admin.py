from django.contrib import admin

from .models import Artist,Customer,Art,Order,Review
# Register your models here.

admin.site.register(Artist)
admin.site.register(Customer)
admin.site.register(Art)
admin.site.register(Order)
admin.site.register(Review)
