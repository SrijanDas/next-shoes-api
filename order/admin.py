from django.contrib import admin

from .models import Order, OrderItem, CancelledOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', "order_status", "total_amount", "created_at", "delivery_date", "payment_done", "razorpay_order_id")


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderItem._meta.get_fields()]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(CancelledOrder)
