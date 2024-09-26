from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("products/<int:id>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("product-quantity-update/", views.product_quantity_update, name="product_quantity_update"),
]
