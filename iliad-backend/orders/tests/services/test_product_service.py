from django.test import TestCase
from orders.models.product import Product
from orders.models.order import Order
from orders.services.product_service import ProductService
from orders.tests.factories import OrderFactory, ProductFactory

class ProductServiceTest(TestCase):

    def setUp(self):
        self.product_service = ProductService()
        self.order = OrderFactory()

    def test_create_products(self):
        products_data = [
            {"name": "Product 1", "price": 10},
            {"name": "Product 2", "price": 20}
        ]
        self.product_service.create_products(self.order, products_data)

        self.assertEqual(Product.objects.filter(order=self.order).count(), 2)
        names = list(Product.objects.filter(order=self.order).values_list('name', flat=True))
        self.assertIn("Product 1", names)
        self.assertIn("Product 2", names)

    def test_delete_products(self):
        product1 = ProductFactory(order=self.order)
        product2 = ProductFactory(order=self.order)
        product3 = ProductFactory(order=self.order)

        self.product_service.delete_products(self.order, [product1.id, product2.id])

        remaining = Product.objects.filter(order=self.order)
        self.assertEqual(remaining.count(), 1)
        self.assertEqual(remaining.first().id, product3.id)

    def test_update_or_create_products_update_existing(self):
        product = ProductFactory(order=self.order, name="Old Name", price=50)

        update_data = [
            {"id": product.id, "name": "Updated Name", "price": 99}
        ]

        self.product_service.update_or_create_products(self.order, update_data)

        product.refresh_from_db()
        self.assertEqual(product.name, "Updated Name")
        self.assertEqual(product.price, 99)

    def test_update_or_create_products_create_new(self):
        initial_count = Product.objects.count()

        new_data = [
            {"name": "New Product", "price": 25}
        ]

        self.product_service.update_or_create_products(self.order, new_data)

        self.assertEqual(Product.objects.count(), initial_count + 1)
        created = Product.objects.get(order=self.order, name="New Product")
        self.assertEqual(created.price, 25)

    def test_update_or_create_products_skip_invalid_id(self):
        invalid_id_data = [
            {"id": 999999, "name": "Nonexistent Product", "price": 100}
        ]

        self.product_service.update_or_create_products(self.order, invalid_id_data)

        # No new product should be created, and nothing should break
        self.assertEqual(Product.objects.count(), 0)
