from rest_framework import serializers

from .models import *


class BrandNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name", "logo_url", )


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandNameSerializer(many=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "brand",
        )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "get_absolute_url",
        )


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("name", )


class ProductVariantDetailSerializer(serializers.ModelSerializer):
    pass


class ProductVariantSerializer(serializers.ModelSerializer):
    color = ColorSerializer(many=False)
    parent_product = ProductSerializer(many=False)

    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "image_url",
            "slug",
            "parent_product",
            "color",
            "date_added"
        )
