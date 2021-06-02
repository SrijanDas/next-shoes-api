from django.contrib.auth.models import User
from django.db import models

from product.models import Product

ORDER_STATUS = [
    ('YTD', 'Yet to dispatch'),
    ('DIS', 'Dispatched'),
    ('SHP', 'Shipped'),
    ('CAN', 'Cancelled'),
]


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    order_status = models.CharField(max_length=3,
                                    choices=ORDER_STATUS,
                                    default="YTD")

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id


class CancelledOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    reason_for_cancellation = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return '%s' % self.order

