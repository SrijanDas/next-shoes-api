from django.urls import path

from . import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search', views.search),
    path('products/<slug:product_slug>', views.ProductDetail.as_view()),
    # path('products/<slug:brand_slug>/', views.BrandDetail.as_view()),
    path('brand-list/', views.get_brand_list),
    # path('products/details/<slug:slug>', views.ProductVariantDetail.as_view()),
    # path('products/get-image-url/<slug:slug>', views.get_image)

]
