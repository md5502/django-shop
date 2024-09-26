import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cart, CartItem, Product, Review

logger = logging.getLogger(__name__)


def home(request):
    products = Product.objects.all()
    return render(request, "shop/index.html", {"products": products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=product)

    return render(request, "shop/product_detail.html", {"product": product, "reviews": reviews})


def add_to_cart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            product_id = int(request.POST.get("product_id"))
            product_check = get_object_or_404(Product, id=product_id)
            user_cart, created = Cart.objects.get_or_create(created_by=request.user, status="A")
            if CartItem.objects.filter(cart=user_cart, product=product_check).exists():
                messages.warning(request, "You already have this product in your cart")
                return JsonResponse({"status": "success", "message": "You already have this product in your cart"})

            CartItem.objects.create(cart=user_cart, product=product_check, price=product_check.price, quantity=1)

            messages.success(request, "Product added successfully")
            return JsonResponse({"status": "success", "message": "Product added successfully"})

        messages.warning(request, "Login to continue")
        return JsonResponse({"status": "success", "message": "Login to continue"})

    return redirect("shop/add_to_cart")


@login_required(login_url="account:login")
def cart_view(request):
    user_cart = Cart.objects.get(created_by=request.user)

    # Calculate total price for each cart item and the entire cart
    cart_items = user_cart.cart_items.all()
    total_price = 0

    for item in cart_items:
        item.total = item.quantity * item.product.price  # Calculate total for each item
        total_price += item.total  # Add to cart total

    context = {
        "cart": user_cart,
        "cart_items": cart_items,
        "total_price": total_price,
    }

    return render(request, "shop/cart.html", context)


@login_required(login_url="account:login")
def product_quantity_update(request):
    if request.method == "POST":
        action = request.POST.get("action")
        product_id = request.POST.get("product_id")
        current_product_quantity = int(request.POST.get("current_product_quantity"))
        product = get_object_or_404(Product, id=product_id)
        p_quantity = product.quantity
        user_cart = Cart.objects.get(created_by=request.user)

        cart_item = CartItem.objects.filter(cart=user_cart, product=product).first()

        if not cart_item:
            messages.error(request, "Cart item not found.")
            return JsonResponse({"status": "success", "message": "cart item not found"}, status=404)

        if action == "increase":
            if current_product_quantity >= p_quantity:
                messages.warning(request, "Cannot add more than available stock.")
                return JsonResponse({"status": "success", "message": "Cannot add more than available stock"})

            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Quantity increased.")
            return JsonResponse({"status": "success", "message": "Quantity increased"})

        if action == "decrease":
            if current_product_quantity <= 1:
                cart_item.delete()
                messages.success(request, "Item removed from cart.")
                return JsonResponse({"status": "success", "message": "Item removed from cart"})
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, "Quantity decreased.")
            return JsonResponse({"status": "success", "message": "Quantity decreased"})

    messages.error(request, "Invalid request.")
    return JsonResponse({"status": "success", "message": "Invalid request"}, status=400)


@login_required(login_url="account:login")
def checkout_view(request):
    return "asd"
