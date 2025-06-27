from django.shortcuts import get_object_or_404
from orders.models.order import Order
from orders.models.product import Product
from orders.services.product_service import ProductService
from django.db import transaction
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from datetime import datetime
from rest_framework.exceptions import ValidationError


class OrderService:
    product_service = ProductService()

    def list_orders(self, filters=None):
        queryset = Order.objects.all()

        if filters:
            search = filters.get("search")
            date_start = filters.get("date_start")
            date_end = filters.get("date_end")

            if search:
                queryset = queryset.filter(
                    Q(customer_name__icontains=search) | Q(description__icontains=search)
                )

            if date_start:
                try:
                    parsed_start = datetime.strptime(date_start, "%Y-%m-%d")
                    queryset = queryset.filter(date__date__gte=parsed_start)
                except ValueError:
                    pass

            if date_end:
                try:
                    parsed_end = datetime.strptime(date_end, "%Y-%m-%d")
                    queryset = queryset.filter(date__date__lte=parsed_end)
                except ValueError:
                    pass

        return queryset

    def get_order(self, order_id):
        return get_object_or_404(Order, id=order_id)

    def create_order(self, validated_data):
        products_data = validated_data.pop('products', [])
        order = Order.objects.create(**validated_data)
        self.product_service.create_products(order, products_data)
        return order

    @transaction.atomic
    def update_order(self, order_id: int, validated_data: dict) -> Order:
        expected_version = validated_data.pop("version", None)
                
        if expected_version is None:
            raise ValidationError("Missing version for optimistic locking.")

        products_data = validated_data.pop('products', [])
        products_to_delete = validated_data.pop('products_to_delete', [])

        # fetch the order with the expected version
        order = Order.objects.filter(id=order_id, version=expected_version).first()
        if not order:
            raise ValidationError("Order has been modified by another user. Please refresh and try again.")

        # Update
        for attr, value in validated_data.items():
            setattr(order, attr, value)

        # Increment version
        order.version += 1

        # Save order
        order.save()

        # Update or create products
        for product_data in products_data:
            product_id = product_data.get('id', None)

            if product_id:
                try:
                    product = Product.objects.get(id=product_id, order=order)
                    for attr, value in product_data.items():
                        setattr(product, attr, value)
                    product.save()
                except Product.DoesNotExist:
                    pass
            else:
                Product.objects.create(order=order, **product_data)

        if products_to_delete:
            Product.objects.filter(id__in=products_to_delete, order=order).delete()

        return order

    def delete_order(self, order):
        order.delete()
