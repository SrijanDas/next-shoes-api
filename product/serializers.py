from rest_framework import serializers

from .models import Category, Product, Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = (
            "id",
            "slug",
            "first_name",
            "last_name",
            "age",
            "bio",
            "rating",
            "get_image",
            "get_thumbnail",
        )


class SellerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail",
            "seller"
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
        )


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SellerProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Seller
        fields = (
            "id",
            "slug",
            "products",
        )
