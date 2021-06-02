from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category, Seller
from .serializers import ProductSerializer, CategorySerializer, \
    CategoryListSerializer, SellerListSerializer, SellerSerializer

from django.db.models import Q


# Create your views here.


class LatestProductsList(APIView):
    def get(self, request):
        products = Product.objects.all()[:20]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class SellerDetail(APIView):
    def get_object(self, seller_slug):
        try:
            return Seller.objects.get(slug=seller_slug)
        except Exception as e:
            raise Http404

    def get(self, request, seller_slug):
        seller = self.get_object(seller_slug)
        serializer = SellerSerializer(seller)
        return Response(serializer.data, 200)


class SellerProducts(APIView):
    def get_object(self, seller_slug):
        try:
            return Product.objects.get(seller__slug=seller_slug)
        except Exception:
            raise Http404

    def get(self, request, seller_slug):
        products = self.get_object(seller_slug)
        # print("\n\nproducts----------")
        # print(seller_slug)
        # print(products)
        # serializer = ProductSerializer(products)
        return Response(f"{seller_slug}")


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
def get_category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['Get'])
def get_seller_list(request):
    sellers = Seller.objects.all()
    serializer = SellerListSerializer(sellers, many=True)
    return Response(serializer.data)
