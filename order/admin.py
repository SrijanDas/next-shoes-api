from django.contrib import admin

from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'id', "order_status", "total_amount", "created_at", "delivery_date", "payment_done", "razorpay_order_id")


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'return_requested', 'returned']


class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.get_fields() if field.name != "payment_data"]


class ReturnItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReturnItem._meta.get_fields()]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ReturnItem, ReturnItemAdmin)
admin.site.register(CancelledOrder)
admin.site.register(Payment, PaymentAdmin)
