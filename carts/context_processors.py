from carts.models import Cart,CartItem
from carts.views import _cart_id


def counter(request):
    cart_count = 0  # Initialize cart_count to zero
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart = cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0  # If no cart items exist, set count to zero
    return dict(cart_count = cart_count)  # Return the cart count in the context