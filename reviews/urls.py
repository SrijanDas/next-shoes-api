from django.urls import path

from . import views

urlpatterns = [
    # path('get-reviews/<int:product_id>/', views.get_reviews),
    path('reviews/', views.get_reviews),

]