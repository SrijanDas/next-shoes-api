from django.urls import path

from . import views

urlpatterns = [
    path('checkout/', views.checkout),
    path('all/', views.OrdersList.as_view()),
    path('cancel-order/', views.cancel_order),
]