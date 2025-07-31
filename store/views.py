from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from .models import Product  # Assuming you have a Product model defined
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

# Create your views here.

def store(request, category_slug=None):
    categories = None  # Initialize categories if needed
    products = None  # Initialize products if needed
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories)
        paginator = Paginator(products, 3)  # Show 6 products per page
        page = request.GET.get('page')  # Get the current page number from the request
        paged_products = paginator.get_page(page)  # Get the products for the current page
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')  # Fetch all products from the database
        paginator = Paginator(products, 3)  # Show 6 products per page
        page = request.GET.get('page')  # Get the current page number from the request
        paged_products = paginator.get_page(page)  # Get the products for the current page
        product_count = products.count()  # Get the count of products
    context = {
        'products': paged_products,
        'product_count': product_count, 
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=product).exists() 
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    
    context = {
        'product': product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)