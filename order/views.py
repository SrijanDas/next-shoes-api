import razorpay
from django.conf import settings
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, CancelledOrder
from .serializers import *

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

currency = "INR"
packaging_fees_per_item = 29


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        packaging_fees = 0
        sub_total = 0
        try:
            for item in serializer.validated_data['items']:
                packaging_fees += packaging_fees_per_item
                sub_total += item.get('quantity') * item.get('product').price

            # Razorpay
            total_amount = packaging_fees + sub_total
            # Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            razorpay_amount = int(total_amount) * 100

            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=razorpay_amount,
                                                               currency=currency,
                                                               payment_capture=1))

            # razorpay order id of newly created order.
            razorpay_order_id = razorpay_order['id']

            # saving the order
            serializer.save(user=request.user,
                            sub_total=sub_total,
                            packaging_fees=packaging_fees,
                            total_amount=total_amount,
                            razorpay_order_id=razorpay_order_id)

            # we need to pass these details to frontend.
            context = {"status": True,
                       "razorpay_details": {
                           'razorpay_order_id': razorpay_order_id,
                           'razorpay_amount': str(razorpay_amount),
                           'currency': currency,
                       },
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
        orders = Order.objects.filter(user=request.user).order_by("-delivery_date")
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)


@api_view(['GET'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
def get_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        serializer = OrderPageSerializer(order, many=False)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"Something went wrong!"})


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
