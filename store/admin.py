from django.contrib import admin
from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'category', 'price', 'stock', 'is_available', 'updated_at')
    
admin.site.register(Product, ProductAdmin)