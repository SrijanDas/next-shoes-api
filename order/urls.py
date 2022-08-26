from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.OrdersList.as_view()),
    path('orders/<int:order_id>/', views.get_order),
    path('orders/checkout/', views.checkout),
    path('orders/place-order/', views.place_order),
    path('verify-payment/', views.verify_payment),
    path('cancel-order/', views.cancel_order),
    path('return-item/', views.return_item),
    path('cancel-return/', views.cancel_return),

]