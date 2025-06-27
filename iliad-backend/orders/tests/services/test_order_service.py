from django.test import TestCase
from orders.services.order_service import OrderService
from orders.tests.factories import OrderFactory, ProductFactory
from datetime import datetime

class OrderServiceTest(TestCase):

    def setUp(self):
        self.order_service = OrderService()

        self.order1 = OrderFactory(
            customer_name="Alice Smith",
            description="First test order",
            date=datetime(2024, 6, 1, 10, 0),
        )
        self.order2 = OrderFactory(
            customer_name="Bob Johnson",
            description="Second test order",
            date=datetime(2024, 6, 15, 14, 30),
        )
        self.order3 = OrderFactory(
            customer_name="Charlie",
            description="Another order",
            date=datetime(2024, 7, 1, 9, 0),
        )

        self.product1 = ProductFactory(order=self.order1, name="Prod1", price=10)
        self.product2 = ProductFactory(order=self.order1, name="Prod2", price=20)

    # --- list_orders tests ---

    def test_list_orders_no_filters_returns_all(self):
        orders = self.order_service.list_orders()  # use instance
        self.assertEqual(orders.count(), 3)

    def test_list_orders_search_by_customer_name(self):
        filters = {"search": "Alice"}
        orders = self.order_service.list_orders(filters)
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders.first().customer_name, "Alice Smith")

    def test_list_orders_date_range(self):
        filters = {
            "date_start": "2024-06-10",
            "date_end": "2024-06-30"
        }
        orders = self.order_service.list_orders(filters)
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders.first().id, self.order2.id)

    # --- create_order tests ---

    def test_create_order_with_products(self):
        validated_data = {
            "customer_name": "New Customer",
            "description": "Test order",
            "date": datetime(2025, 1, 1, 10, 0),
            "products": [
                {"name": "Product A", "price": 10},
                {"name": "Product B", "price": 20}
            ],
        }
        order = self.order_service.create_order(validated_data)
        self.assertEqual(order.customer_name, "New Customer")
        self.assertEqual(order.products.count(), 2)

    # --- update_order tests ---

    def test_update_order_fields(self):
        validated_data = {
            "customer_name": "Updated Name",
            "products": [],
            "products_to_delete": [],
            "version": self.order1.version
        }
        updated_order = self.order_service.update_order(self.order1.id, validated_data)
        self.assertEqual(updated_order.customer_name, "Updated Name")

    def test_update_order_create_new_product(self):
        validated_data = {
            "products": [{"name": "New Product", "price": 30}],
            "products_to_delete": [],
            "version": self.order1.version
        }
        updated_order = self.order_service.update_order(self.order1.id, validated_data)
        self.assertTrue(updated_order.products.filter(name="New Product").exists())

    def test_update_order_update_existing_product(self):
        validated_data = {
            "products": [{"id": self.product1.id, "price": 99}],
            "products_to_delete": [],
            "version": self.order1.version
        }
        updated_order = self.order_service.update_order(self.order1.id, validated_data)
        updated_product = updated_order.products.get(id=self.product1.id)
        self.assertEqual(updated_product.price, 99)

    def test_update_order_delete_product(self):
        validated_data = {
            "products": [],
            "products_to_delete": [self.product2.id],
            "version": self.order1.version
        }
        updated_order = self.order_service.update_order(self.order1.id, validated_data)
        self.assertFalse(updated_order.products.filter(id=self.product2.id).exists())

    # --- delete_order tests ---

    def test_delete_order(self):
        order_to_delete = OrderFactory()
        self.order_service.delete_order(order_to_delete)
        with self.assertRaises(OrderFactory._meta.model.DoesNotExist):
            order_to_delete._meta.model.objects.get(id=order_to_delete.id)
