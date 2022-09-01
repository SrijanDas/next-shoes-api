from rest_framework import serializers

from .models import Order, OrderItem, Payment

from product.serializers import ProductSerializer
from accounts.serializers import AddressSerializer
from accounts.models import Address
from reviews.models import Review
from reviews.serializers import ReviewSerializer


class MyOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    review = serializers.SerializerMethodField("get_review")

    class Meta:
        model = OrderItem
        fields = ("id", "product", "price", "quantity", "review", "return_requested", "returned")

    def get_review(self, order_item):
        try:
            review = Review.objects.get(order_item=order_item)
            return ReviewSerializer(review).data
        except Exception:
            return False


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
        fields = ("id", "total_amount", 'packaging_fees', 'sub_total', "delivery_date", "items", "order_status", "address", "dispatched_on", "created_at")

    def get_address(self, order):
        address = Address.objects.get(id=order.address.id)
        serializer = AddressSerializer(address, many=False)
        return serializer.data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("transaction_id", "amount", "method", "currency", "order", "date_added")

    def create(self, validated_data):
        validated_data['amount'] = validated_data['amount'] / 100
        payment = Payment.objects.create(**validated_data)
        return payment

    def update(self, instance, validated_data):
        instance.amount = validated_data['amount'] / 100
        instance.transaction_id = validated_data.get('transaction_id', instance.transaction_id)
        instance.method = validated_data.get('method', instance.method)
        instance.status = validated_data.get('status', instance.status)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.payment_data = validated_data.get('payment_data', instance.payment_data)
        instance.save()
        return instance

