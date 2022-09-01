import json
import razorpay
from django.conf import settings
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .models import Order, CancelledOrder, ReturnItem, Payment
from .serializers import *
import hmac
import hashlib
from .utils import send_order_confirmation_email, send_payment_success_email
import threading

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
                packaging_fees += packaging_fees_per_item * item.get('quantity')
                sub_total += item.get('quantity') * item.get('product').price

            total_amount = packaging_fees + sub_total

            # saving the order
            serializer.save(user=request.user,
                            sub_total=sub_total,
                            packaging_fees=packaging_fees,
                            total_amount=total_amount,
                            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error: ", e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def place_order(request):
    try:
        payment_method = request.data.get('paymentMethod')
        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id)

        if payment_method == 'online':
            # Razorpay

            # # Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            razorpay_amount = int(order.total_amount) * 100

            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=razorpay_amount,
                                                               currency=currency,
                                                               payment_capture=1))
            #
            # razorpay order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            # we need to pass these details to frontend.
            context = {"status": True,
                       "razorpay_details": {
                           'razorpay_order_id': razorpay_order_id,
                           'razorpay_amount': str(razorpay_amount),
                           'currency': currency,
                       }}

            # creating a payment and setting order payment method
            Payment.objects.create(order=order, razorpay_order_id=razorpay_order_id)
            order.payment_method = 'online'
            order.save()
            return Response(context)

        elif payment_method == 'cod':
            order.payment_method = 'cod'
            order.order_confirmed = True
            order.save()

            # creating thread for sending email
            thread = threading.Thread(target=send_order_confirmation_email, args=(order,))
            thread.start()

            return Response({'status': True})
        else:
            return Response({'status': False})

    except Exception as e:
        print(e)
        return Response({'status': False})


@api_view(['POST'])
def verify_payment(request):
    try:
        dig = hmac.new(key=bytes(settings.WEBHOOK_SECRET, 'utf-8'), msg=request.body,
                       digestmod=hashlib.sha256).hexdigest()

        payload = json.loads(request.body)['payload']
        razorpay_order_id = payload["payment"]["entity"]['order_id']

        entity = payload["payment"]["entity"]
        payment_obj = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        serializer = PaymentSerializer(payment_obj, entity)

        if serializer.is_valid() and request.headers['X-Razorpay-Signature'] == dig:
            # valid payment
            # saving payment data to database and setting order payment done
            serializer.save(payment_data=payload, transaction_id=entity['id'])
            order = Order.objects.get(id=payment_obj.order_id)
            order.payment_done = True

            # thread for sending payment success email
            thread1 = threading.Thread(target=send_payment_success_email, args=(serializer.data, order))
            thread1.start()

            if not order.order_confirmed and order.payment_method == 'online':
                order.order_confirmed = True

                # thread for sending order confirmation email
                thread2 = threading.Thread(target=send_order_confirmation_email, args=(order,))
                thread2.start()

            order.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_orders_for_user(self, user):
        try:
            orders = Order.objects.filter(user=user, order_confirmed=True).order_by("-delivery_date")
            return orders
        except Exception:
            raise Http404

    def get(self, request):
        orders = self.get_orders_for_user(request.user)
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
    order_id = request.data['itemId']
    reason = request.data['reason']
    order = Order.objects.get(pk=order_id)
    order.order_status = "CAN"
    order.save()
    cancelled_order = CancelledOrder()
    cancelled_order.order = order
    cancelled_order.reason_for_cancellation = reason
    cancelled_order.save()
    return Response("Order Cancelled")


@api_view(["POST"])
def return_item(request):
    try:
        item_id = request.data['itemId']
        reason = request.data['reason']

        ReturnItem.objects.create(
            order_item_id=item_id,
            reason=reason
        )
        # order_item = OrderItem.objects.get(id=item_id)
        # order_item.save(return_requested=True)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def cancel_return(request):
    try:
        item_id = request.data['itemId']
        order_item = OrderItem.objects.get(id=item_id)
        order_item.return_requested = False
        order_item.returned = False
        order_item.save()

        return_item_obj = ReturnItem.objects.get(order_item=order_item)
        return_item_obj.delete()

        return Response("cancelled return request", status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
