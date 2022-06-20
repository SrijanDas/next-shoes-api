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
    class Meta:
        model = ProductVariantDetail
        fields = (
            "size",
            "price",
            "quantity",
        )


class ProductVariantSerializer(serializers.ModelSerializer):
    parent_product = ProductSerializer(many=False)
    product_details = serializers.SerializerMethodField("get_details")
    color = serializers.SerializerMethodField("get_color")

    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "image_url",
            "slug",
            "parent_product",
            "color",
            "date_added",
            "product_details",
        )

    def get_details(self, product_variant):
        product_details_objs = ProductVariantDetail.objects.filter(product_variant_id=product_variant.id)
        return ProductVariantDetailSerializer(product_details_objs, many=True).data

    def get_color(self, product_variant):
        color = Color.objects.get(id=product_variant.color.pk)
        return color.name


