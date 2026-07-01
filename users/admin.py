from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "first_name", "last_name", "is_staff", "role"]
    search_fields = ["email"]
    fieldsets = UserAdmin.fieldsets + (("Custom fields", {"fields": ("role",)}),)


admin.site.register(CustomUser, CustomUserAdmin)
