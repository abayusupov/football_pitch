from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_owner', 'is_staff', 'date_joined')
    list_filter = ('is_owner', 'is_staff')

CustomUserAdmin.fieldsets += ("Qo'shimcha ma'lumotlar", {'fields': ('is_owner',)}),
admin.site.register(CustomUser, CustomUserAdmin)