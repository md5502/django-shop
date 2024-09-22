from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import BaseUser


@admin.register(BaseUser)
class UserAdmin(admin.ModelAdmin):

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "is_active", "is_admin", "is_superuser")
    list_filter = ("is_active", "is_admin", "is_superuser")
    search_fields = ("email",)
    filter_horizontal = ("groups", "user_permissions")
