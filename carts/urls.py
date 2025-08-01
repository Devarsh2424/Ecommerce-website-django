from django.urls import path
from carts import views
urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/<int:product_id>/<int:cart_item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    
    path('checkout/', views.checkout, name='checkout'),
]
