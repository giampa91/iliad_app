from orders.models.product import Product

class ProductService:

    def create_products(self, order, products_data):
        for prod_data in products_data:
            prod_data = dict(prod_data)
            prod_data.pop('order', None)
            Product.objects.create(order=order, **prod_data)

    def delete_products(self, order, product_ids):
        if product_ids:
            Product.objects.filter(id__in=product_ids, order=order).delete()

    def update_or_create_products(self, order, products_data):
        for prod_data in products_data:
            prod_id = prod_data.get('id')
            prod_data = dict(prod_data)
            prod_data.pop('order', None)

            if prod_id:
                try:
                    product = Product.objects.get(id=prod_id, order=order)
                    for attr, value in prod_data.items():
                        setattr(product, attr, value)
                    product.save()
                except Product.DoesNotExist:
                    continue
            else:
                Product.objects.create(order=order, **prod_data)
