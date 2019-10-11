from django.contrib import admin
from .models import User # 추가

# Register your models here.

class UserAdmin(admin.ModelAdmin): # 추가
    list_display = ('email', )

admin.site.register(User, UserAdmin) # 추가