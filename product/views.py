from django.db.models import Q
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *


# Create your views here.
class LatestProductsList(APIView):
    def get(self, request):
        color_variants = ColorVariant.objects.filter(main_variant=True).order_by("date_added")[:10]
        serializer = ProductCardSerializer(color_variants, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    def get_object(self, product_slug):
        try:
            return ColorVariant.objects.get(slug=product_slug)
        except Exception:
            raise Http404

    def get(self, request, product_slug):
        color_variant = self.get_object(product_slug)
        serializer = ProductPageSerializer(color_variant)
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


@api_view(['GET'])
def search(request):
    query = request.query_params.get('q', '')
    query = str(query).replace(' ', '-')
    if query:
        color_variants = ColorVariant.objects.filter(
            Q(slug__icontains=query)
            | Q(parent_product__brand__slug__icontains=query)
        )
        serializer = ProductCardSerializer(color_variants, many=True)
        return Response(serializer.data)

    return Response({"products": []})


@api_view(['Get'])
def get_brand_list(request):
    brands = Brand.objects.all()
    serializer = BrandListSerializer(brands, many=True)
    return Response(serializer.data)


class ProductVariantDetail(APIView):
    def get_object(self, slug):
        try:
            size_variant = Product.objects.get(slug=slug)
            return size_variant
        except Exception:
            raise Http404

    def get(self, request, slug):
        size_variant = self.get_object(slug)
        serializer = ProductSerializer(size_variant)
        return Response(serializer.data)


@api_view(['Get'])
def get_image(request, slug):
    try:
        color_variant = ColorVariant.objects.get(slug=slug)
        images = ProductImage.objects.filter(color_variant=color_variant)
        context = {
            "image_url": color_variant.image_url,
            "images": ImageSerializer(images, many=True).data
        }
        return Response(context)
        pass
    except Exception:
        raise Http404
