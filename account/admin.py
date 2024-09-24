from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "profile_img")}),
        ("Permissions", {"fields": ("is_active", "is_admin", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", )}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),
        }),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_admin")
    list_filter = ("is_admin", "is_active", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
