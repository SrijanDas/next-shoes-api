from accounts.models import Account as User, Address
from django.db import models
from datetime import datetime, timedelta

from product.models import Product

ORDER_STATUS = [
    ('YTD', 'Yet to dispatch'),
    ('DIS', 'Dispatched'),
    ('SHP', 'Shipped'),
    ('CAN', 'Cancelled'),
]


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sub_total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    packaging_fees = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    order_status = models.CharField(max_length=3,
                                    choices=ORDER_STATUS,
                                    default="YTD")

    delivery_date = models.DateTimeField(null=True, blank=True)
    payment_done = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):  # new
        if not self.delivery_date:
            created_at = self.created_at
            if not self.created_at:
                created_at = datetime.now()
            self.delivery_date = created_at + timedelta(days=3)

        return super().save(*args, **kwargs)


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


# class Payment(models.Model):
#     razorpay_payment_id = models.CharField(max_length=100)
#     razorpay_order_id = models.CharField(max_length=100)
#     razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
#     currency = models.CharField(max_length=5)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '%s' % self.razorpay_order_id


