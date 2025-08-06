from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from orders.models import OrderProduct
from store.forms import ReviewForm
from .models import Product, ReviewRating  # Assuming you have a Product model defined
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib import messages

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
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user = request.user, product_id = product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
    
    # Get the reviews for the product
    reviews = ReviewRating.objects.filter(product_id = product.id, status = True)
    
    context = {
        'product': product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
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


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')  # Get the URL of the page where the form was submitted
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id= request.user.id, product__id = product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank You! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject= form.cleaned_data['subject']
                data.rating= form.cleaned_data['rating']
                data.review= form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank You! Your review has been submitted.')
                return redirect(url)