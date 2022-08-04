from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrdersList.as_view()),
    path('<int:order_id>/', views.get_order),
    path('checkout/', views.checkout),
    path('cancel-order/', views.cancel_order),
]