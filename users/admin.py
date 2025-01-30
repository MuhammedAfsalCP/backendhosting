from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_deleted",
        "is_staff",
        "is_active",
    )  # Fields to display
    list_filter = (
        "is_deleted",
        "is_staff",
        "is_active",
    )  # Filters on the right side of the admin page
    search_fields = ("username", "email")  # Searchable fields
    ordering = ("username",)  # Default ordering
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Additional Info", {"fields": ("is_deleted",)}),  # Include is_deleted here
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_deleted",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
