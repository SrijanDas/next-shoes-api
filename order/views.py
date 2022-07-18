from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

import razorpay
from django.conf import settings
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, CancelledOrder
from .serializers import OrderSerializer, MyOrderSerializer

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

currency = "INR"
packaging_fees_per_item = 29


@api_view(['POST'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        packaging_fees = 0
        sub_total = 0
        try:
            for item in serializer.validated_data['items']:
                packaging_fees += packaging_fees_per_item
                sub_total += item.get('quantity') * item.get('product').price

            serializer.save(sub_total=sub_total, packaging_fees=packaging_fees)

            # Razorpay
            # Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            amount = (int(sub_total) + packaging_fees) * 100  #

            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                               currency=currency,
                                                               payment_capture=1))

            # order id of newly created order.
            razorpay_order_id = razorpay_order['id']

            # we need to pass these details to frontend.
            context = {"status": True,
                       'razorpay_order_id': razorpay_order_id,
                       'razorpay_amount': str(amount),
                       'currency': currency,
                       "order_details": serializer.data
                       }

            return Response(context, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error: ", e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    return Response({}, status=status.HTTP_400_BAD_REQUEST)


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
