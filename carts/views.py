from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)  # Fetch the product by ID
    # Check if user is authenticated
    if current_user.is_authenticated:
    
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
            
    # try:
    #     cart = Cart.objects.get(cart_id=_cart_id(request)) # Get the cart
    # except Cart.DoesNotExist:
    #     cart = Cart.objects.create(cart_id=_cart_id(request)) # Create a new cart if it doesn't exist
    # cart.save()
    
        is_cart_item_exists = CartItem.objects.filter(product=product, user = current_user).exists()  # Check if the item is already in the cart
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user = current_user)  # This is a QuerySet

        # existing variations -> database
        # current variations -> product_variation
        # item_id -> database
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)


            if product_variation in existing_variation_list:
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # get a new single CartItem object before accessing variations
                item = CartItem.objects.create(product=product, quantity=1, user = current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, user = current_user)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    # if the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
        

def delete_from_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id) # Fetch the product by ID
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id) # Fetch the product by ID
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user = request.user, id=cart_item_id ) # Get the cart item
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # Get the cart
        cart_item = CartItem.objects.get(product=product, cart = cart, id = cart_item_id)
    cart_item.delete() # Remove the item from the cart
    return redirect('cart')
        
    
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user, is_active = True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # Get the cart
            cart_items = CartItem.objects.filter(cart=cart, is_active=True) # Get active items in the cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) # Calculate total price
            quantity += cart_item.quantity # Calculate total quantity
        tax = (2 * total)/ 100 # Calculate tax (2% of total)
        grand_total = total + tax # Calculate grand total
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,  
        'quantity': quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total': grand_total
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0                        
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100  # Calculate tax (2% of total)
        grand_total = total + tax  # Calculate grand total
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)