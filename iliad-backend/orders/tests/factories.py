import factory
from orders.models.order import Order
from orders.models.product import Product


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer_name = factory.Faker("name")
    description = factory.Faker("sentence")

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    order = factory.SubFactory(OrderFactory)
    name = factory.Faker("word")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)