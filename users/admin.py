from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("id", "username", "email", "first_name", "last_name", "contact", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "middle_name", "last_name", "username", "contact", "address", "gender")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name", "username", "contact", "address", "gender"),
        }),
    )
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)
