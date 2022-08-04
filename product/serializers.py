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
            "logo_url",
        )


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("name", )


class ColorVariantSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField("get_brand")
    # product_details = serializers.SerializerMethodField("get_details")
    color = serializers.SerializerMethodField("get_color")
    available_colors = serializers.SerializerMethodField("get_colors")
    starting_price = serializers.SerializerMethodField("get_price")
    name = serializers.SerializerMethodField("get_name")

    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "name",
            "image_url",
            "slug",
            "brand",
            "color",
            "available_colors",
            # "product_details",
            "starting_price",
        )

    # def get_details(self, color_variant):
    #     product_details_objs = ProductVariantDetail.objects.filter(product_variant_id=color_variant.id)
    #     return ProductVariantDetailSerializer(product_details_objs, many=True).data

    def get_color(self, product_variant):
        color = Color.objects.get(id=product_variant.color.pk)
        return color.slug

    def get_colors(self, product_variant):
        color_variants = ProductVariant.objects.filter(parent_product_id=product_variant.parent_product.id)
        colors = []
        for cv in color_variants:
            colors.append(cv.color.slug)
        return colors

    def get_brand(self, product_variant):
        parent_product = Product.objects.get(id=product_variant.parent_product.id)
        return BrandSerializer(parent_product.brand).data

    def get_price(self, product_variant):
        size_variants = ProductVariantDetail.objects.filter(product_variant_id=product_variant.id).order_by("price")
        if size_variants.count() > 0:
            return size_variants.first().price
        return -1

    def get_name(self, product_variant):
        parent_product = Product.objects.get(id=product_variant.parent_product.id)
        return parent_product.name


class SizeVariantSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField("get_size")
    image_url = serializers.SerializerMethodField("get_image_url")
    name = serializers.SerializerMethodField("get_product_name")
    color = serializers.SerializerMethodField("get_color")

    class Meta:
        model = ProductVariantDetail
        fields = (
            "id",
            "size",
            "price",
            "quantity",
            "image_url",
            "name",
            "color",
            "slug",
        )

    def get_color(self, size_variant):
        return size_variant.product_variant.color.name

    def get_size(self, size_variant):
        return size_variant.size.size

    def get_image_url(self, size_variant):
        return size_variant.product_variant.image_url

    def get_product_name(self, size_variant):
        return size_variant.product_variant.parent_product.name




