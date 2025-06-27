from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from orders.models.order import Order
from orders.tests.factories import OrderFactory, ProductFactory
from datetime import datetime

class OrderViewSetTest(APITestCase):

    def setUp(self):
        # Create some orders and products
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
        self.product1 = ProductFactory(order=self.order1, name="Prod1", price=10)

    def test_list_orders(self):
        url = reverse('order-list')
        response = self.client.get(url, {'page': 1, 'page_size': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)

    def test_list_orders_with_search_filter(self):
        url = reverse('order-list')
        response = self.client.get(url, {'search': 'Alice', 'page': 1, 'page_size': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['customer_name'], "Alice Smith")

    def test_list_orders_with_date_range(self):
        url = reverse('order-list')
        response = self.client.get(url, {'date_start': '2024-06-10', 'date_end': '2024-06-30', 'page': 1, 'page_size': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.order2.id)

    def test_retrieve_order(self):
        url = reverse('order-detail', args=[self.order1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order1.id)
        self.assertEqual(response.data['customer_name'], self.order1.customer_name)

    def test_create_order(self):
        url = reverse('order-list')
        data = {
            "customer_name": "John Doe 9",
            "description": "Test order for mock data 6",
            "date": "2025-07-29T00:00:00Z",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['customer_name'], "John Doe 9")

    def test_update_order(self):
        url = reverse('order-detail', args=[self.order1.id])
        data = {
            "customer_name": "Updated Customer",
            "products": [
                {"name": "Product A", "price": 10.5},
                {"name": "Product B", "price": 20.0},
            ],
            "products_to_delete": [self.product1.id],
            "version": 0
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], "Updated Customer")

        products = response.data.get('products', [])
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0]['name'], "Product A")
        self.assertEqual(products[1]['name'], "Product B")


    def test_partial_update_order(self):
        url = reverse('order-detail', args=[self.order1.id])
        data = {"customer_name": "Partially Updated", "version": 0}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], "Partially Updated")

    def test_delete_order(self):
        url = reverse('order-detail', args=[self.order1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order1.id).exists())
