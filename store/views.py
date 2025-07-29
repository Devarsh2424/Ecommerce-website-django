from django.http import Http404
from django.shortcuts import render, get_object_or_404

from category.models import Category
from .models import Product  # Assuming you have a Product model defined

# Create your views here.

def store(request, category_slug=None):
    categories = None  # Initialize categories if needed
    products = None  # Initialize products if needed
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories)
        product_count = products.count()
    else:
        products = Product.objects.all()  # Fetch all products from the database
        product_count = products.count()  # Get the count of products
    context = {
        'products': products,
        'product_count': product_count, 
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    
    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)