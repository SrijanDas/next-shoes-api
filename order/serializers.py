from rest_framework import serializers

from .models import Order, OrderItem

from product.serializers import ProductSerializer
from accounts.serializers import AddressSerializer
from accounts.models import Address


class MyOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "total_amount", "delivery_date", "items", "order_status",)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order


class OrderPageSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)
    address = serializers.SerializerMethodField("get_address")

    class Meta:
        model = Order
        fields = ("id", "total_amount", "delivery_date", "items", "order_status", "address",)

    def get_address(self, order):
        address = Address.objects.get(id=order.address.id)
        serializer = AddressSerializer(address, many=False)
        return serializer.data
