from django.contrib import admin
from .models import Product # 추가

# Register your models here.

class ProductAdmin(admin.ModelAdmin): # 추가 
    list_display = ('name', 'price')

admin.site.register(Product, ProductAdmin) # 추가