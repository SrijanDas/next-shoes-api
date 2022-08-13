from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from .models import Review
from product.models import ColorVariant
from .serializers import ReviewSerializer


# Create your views here.

@api_view(['GET'])
def get_reviews(request):
    try:
        color_variant_id = request.query_params.get('color_variant_id')
        color_variant = ColorVariant.objects.get(pk=color_variant_id)
        reviews = Review.objects.filter(product=color_variant.parent_product)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
