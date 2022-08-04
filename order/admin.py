from django.contrib import admin

from .models import Order, OrderItem, CancelledOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', "order_status", "total_amount", "created_at", "delivery_date", "payment_done", "razorpay_order_id")

# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ()


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(CancelledOrder)

