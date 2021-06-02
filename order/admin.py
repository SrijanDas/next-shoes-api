from django.contrib import admin

from .models import Order, OrderItem, CancelledOrder

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', "order_status")


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(CancelledOrder)
