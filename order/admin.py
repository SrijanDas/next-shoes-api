from django.contrib import admin

from .models import Order, OrderItem, CancelledOrder, Payment


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', "order_status", "total_amount", "created_at", "delivery_date", "payment_done", "razorpay_order_id")


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'returned']


class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.get_fields() if field.name != "payment_data"]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(CancelledOrder)
admin.site.register(Payment, PaymentAdmin)
