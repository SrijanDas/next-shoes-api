from django.db.models.signals import post_save

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
    # razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    dispatched_on = models.DateField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=10, null=True, blank=True)
    payment_done = models.BooleanField(default=False)
    order_confirmed = models.BooleanField(default=False)

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
    return_requested = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.order


class ReturnItem(models.Model):
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.order_item.id


class CancelledOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    reason_for_cancellation = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return '%s' % self.order


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    transaction_id = models.CharField(max_length=256, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=256, null=True, blank=True, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    method = models.CharField(max_length=25, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    currency = models.CharField(max_length=4, null=True, blank=True)
    payment_data = models.JSONField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

# def order_item_return_requested_handler(sender, instance, created, *args, **kwargs):
#     print("order_item_return_requested_handler")
#     print("instance", instance)
#     # print(update_fields)
#
# post_save.connect(order_item_return_requested_handler, sender=OrderItem)
