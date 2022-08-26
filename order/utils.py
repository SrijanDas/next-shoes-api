from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
import datetime
from order.serializers import OrderPageSerializer
import os

__sender = settings.EMAIL_HOST_USER


def send_order_confirmation_email(order_instance):
    subject = "Your order has been successfully placed"
    user_name = f"{order_instance.user.first_name} {order_instance.user.last_name}".capitalize()
    order_confirm_date_string = datetime.datetime.strftime(order_instance.created_at, '%Y-%b-%d')
    sub_arr = order_confirm_date_string.split('-')
    order_confirm_date = f"{sub_arr[1]} {sub_arr[2]}, {sub_arr[0]}"
    order_link = f"http://localhost:3000/orders/{str(order_instance.id)}"
    if not settings.DEBUG:
        order_link = f"https://nfootwear.vercel.app/orders/{str(order_instance.id)}"

    # loading email templates
    # plaintext = ""
    # with open(str(settings.BASE_DIR) + "/templates/email/order_conf.txt") as f:
    #     plaintext = f.read()
    plaintext = get_template(str(settings.BASE_DIR) + '/templates/email/order_conf.txt')
    htmly = get_template(str(settings.BASE_DIR) + '/templates/email/order_conf.html')

    # serializing order instance
    serializer = OrderPageSerializer(order_instance)
    d = {
        'username': user_name,
        'order': serializer.data,
        'order_confirm_date': order_confirm_date,
        'order_link': order_link
    }

    text_content = plaintext.render(context=d)
    html_content = htmly.render(context=d)
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [order_instance.user.email, ]

    email = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.content_subtype = "html"
    email.send()
    return
