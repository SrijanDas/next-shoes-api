from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Review
from product.models import ProductColorVariant, Product
from .serializers import ReviewSerializer, NewReviewSerializer


# Create your views here.
class ReviewView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = NewReviewSerializer(data=request.data)
            if serializer.is_valid():
                product_id = request.data['product']
                product = Product.objects.get(pk=product_id).color_variant.parent_product

                reviews = Review.objects.filter(user=request.user)
                already_reviewed = False
                if reviews.count():
                    for r in reviews:
                        if r.product.pk == product.pk:
                            already_reviewed = True
                            break
                else:
                    serializer.save(user=request.user, product=product)

                if already_reviewed:
                    serializer.save(user=request.user, product=product, show_on_client_side=False)
                else:
                    serializer.save(user=request.user, product=product)

                return Response(serializer.data)

        except Exception as e:
            print(e)

        return Response({})


@api_view(['GET'])
def get_reviews(request):
    try:
        color_variant_id = request.query_params.get('color_variant_id')
        color_variant = ProductColorVariant.objects.get(pk=color_variant_id)
        reviews = Review.objects.filter(product_id=color_variant.parent_product.id, show_on_client_side=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
