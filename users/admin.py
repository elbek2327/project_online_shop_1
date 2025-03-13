

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
