from django.urls import path, include

from . import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/', views.search),
    path('products/<slug:product_slug>/', views.ProductDetail.as_view()),
    # path('products/<slug:brand_slug>/', views.BrandDetail.as_view()),
    path('brand-list/', views.get_brand_list),
    path('products/get-price/<slug:slug>', views.get_price)
]
