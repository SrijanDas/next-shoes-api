from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from order.models import *
from .utils import send_order_confirmation_email


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


@receiver(post_save, sender=Order, dispatch_uid='order_payment_done')
def post_save_order(sender, instance, created, *args, **kwargs):
    if instance.payment_done:
        send_order_confirmation_email(order_instance=instance)

