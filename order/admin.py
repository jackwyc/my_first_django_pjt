from django.contrib import admin
from .models import Order # 추가

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')

admin.site.register(Order, OrderAdmin)