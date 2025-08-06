from django.urls import path
from orders import views

urlpatterns = [
    path('place_order/', views.place_order, name="place_order"),
    # path('payments/', views , name=),
    path('order_complete/', views.order_complete, name='order_complete'),
]
