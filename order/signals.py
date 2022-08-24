from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from order.models import OrderItem, ReturnItem


@receiver(post_save, sender=ReturnItem)
def item_return_requested_handler(sender, instance, created, *args, **kwargs):
    if created:
        order_item = OrderItem.objects.get(id=instance.order_item_id)

        if not order_item.return_requested:
            order_item.return_requested = True
            order_item.save()

        if instance.approved and not order_item.returned:
            order_item.returned = True
            order_item.save()

        instance.save()

#
# def post_save_payment(sender, instance, created, *args, **kwargs):
#     print("payment_post_save method")
#     print(created)
#     if created and instance.status == "captured":
#         print("valid")
#         print(instance.razorpay_order_id)


# post_save.connect(order_item_return_requested_handler, sender=OrderItem)
