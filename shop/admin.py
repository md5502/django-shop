from django.contrib import admin

from .models import Cart, CartItem, Category, Order, OrderLine, Product, Review, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent_category", "slug")
    search_fields = ("name", "slug")
    list_filter = ("parent_category", "tags")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "price", "discount_type", "discount_value")
    search_fields = ("name", "sku")
    list_filter = ("categories", "tags", "discount_type")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "rating")
    search_fields = ("user__username", "product__name")
    list_filter = ("rating",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("created_by", "status")
    search_fields = ("created_by__username",)
    list_filter = ("status",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "price", "quantity")
    search_fields = ("cart__created_by__username", "product__name")
    list_filter = ("cart", "product")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "price", "quantity")
    search_fields = ("order__user__username", "product__name")
    list_filter = ("order", "product")
