from .models import Cart, CartItem


def count_item_in_cart(request):
    counter = 0

    if request.user.is_authenticated:
        user_cart = Cart.objects.filter(created_by=request.user, status="A")[0]
        cart_items = CartItem.objects.filter(cart=user_cart)

        for cart_item in cart_items:
            counter += cart_item.quantity


    return {"count_item_in_cart": counter}
