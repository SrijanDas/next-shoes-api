from django.db.models import Q
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


# Create your views here.
class LatestProductsList(APIView):
    def get(self, request):
        products = ProductVariant.objects.filter(main_variant=True).order_by("date_added")[:10]
        serializer = ProductVariantSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    def get_object(self, product_slug):
        try:
            return ProductVariant.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, product_slug):
        product = self.get_object(product_slug)
        product_details = ProductVariantDetail.objects.get(pk=product.pk)
        print(product_details)
        serializer = ProductVariantSerializer(product)
        return Response(serializer.data)


class BrandDetail(APIView):
    def get_object(self, brand_slug):
        try:
            return Brand.objects.get(slug=brand_slug)
        except Brand.DoesNotExist:
            raise Http404

    def get(self, request, brand_slug):
        brand = self.get_object(brand_slug)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})


@api_view(['Get'])
def get_brand_list(request):
    categories = Brand.objects.all()
    serializer = BrandListSerializer(categories, many=True)
    return Response(serializer.data)


