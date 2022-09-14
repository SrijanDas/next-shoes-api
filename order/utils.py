from product.models import Product
from .serializers import OrderSerializer


def readjust_product_quantity(order):
    serializer = OrderSerializer(order)
    for item in serializer.data.get('items'):
        product = Product.objects.get(id=item.get('product'))
        new_quantity = product.quantity - item.get('quantity')
        product.quantity = new_quantity if new_quantity > 0 else 0
        return product.save()
