from django.test import TestCase
from orders.tests.factories import ProductFactory

class ProductFactoryTest(TestCase):

    def test_product_factory_creates_valid_product(self):
        product = ProductFactory()

        self.assertIsNotNone(product.id)
        self.assertTrue(product.name)
        self.assertIsNotNone(product.order)
        self.assertGreater(product.price, 0)
