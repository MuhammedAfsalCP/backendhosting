from django.contrib import admin

from .models import Products


# Register your models here.
class CustomProductsAdmin(admin.ModelAdmin):
    model = Products
    list_display = (
        "Name",
        "Category",
        "Stock",
        "is_deleted",
        "product_added",
    )  # Fields to display
    list_filter = (
        "is_deleted",
        "Category",
    )  # Filters on the right side of the admin page
    search_fields = ("Name", "Brand")  # Searchable fields
    fieldsets = (
        (None, {"fields": ("Name",)}),
        ("Products info", {"fields": ("Brand", "Price", "Image", "Stock", "Weight")}),
        ("Description", {"fields": ("Description",)}),
        # ('Important dates', {'fields': ('last_login', 'date_joined')}),
        (
            "Additional Info",
            {"fields": ("is_deleted", "Ingredient")},
        ),  # Include is_deleted here
    )


admin.site.register(Products, CustomProductsAdmin)
