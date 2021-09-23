from django.contrib import admin
from .models import User, Product, Basket, Review

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(Review)