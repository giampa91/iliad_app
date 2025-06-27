from django.contrib import admin
from .models.order import Order
from .models.product import Product

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'date')
    search_fields = ('customer_name',)
    list_filter = ('date',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)