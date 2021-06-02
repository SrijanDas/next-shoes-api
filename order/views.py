from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, CancelledOrder
from .serializers import OrderSerializer, MyOrderSerializer


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        try:
            paid_amount = sum(
                item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

            serializer.save(user=request.user, paid_amount=paid_amount)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def cancel_order(request):
    order_id = request.data['order_id']
    reason = request.data['reason']
    order = Order.objects.get(pk=order_id)
    order.order_status = "CAN"
    order.save()
    cancelled_order = CancelledOrder()
    cancelled_order.order = order
    cancelled_order.reason_for_cancellation = reason
    cancelled_order.save()
    return Response("Order Cancelled")