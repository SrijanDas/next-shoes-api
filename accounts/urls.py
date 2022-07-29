from django.urls import path

from . import views

urlpatterns = [
    path('address/', views.AddressController.as_view()),

]
