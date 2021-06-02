from django.urls import path, include

from . import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/', views.search),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('category-list/', views.get_category_list),
    path('seller-list/', views.get_seller_list),
    path('seller/<slug:seller_slug>/', views.SellerDetail.as_view()),
    path('seller/products/<slug:seller_slug>/', views.SellerProducts.as_view()),

]
