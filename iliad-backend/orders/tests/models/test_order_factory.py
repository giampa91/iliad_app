from django.test import TestCase
from orders.tests.factories import OrderFactory

class OrderFactoryTest(TestCase):

    def test_order_factory_creates_valid_order(self):
        order = OrderFactory()

        self.assertIsNotNone(order.id)
        self.assertTrue(order.customer_name)
        self.assertTrue(order.description)
        self.assertIsNotNone(order.date)
