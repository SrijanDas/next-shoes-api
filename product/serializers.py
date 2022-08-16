from rest_framework import serializers

from .models import *
from reviews.models import Review


class BrandNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name", "logo_url",)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("name", "slug")


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image_url", "id")


class ParentProductSerializer(serializers.ModelSerializer):
    brand = BrandNameSerializer(many=False)

    class Meta:
        model = ParentProduct
        fields = (
            "id",
            "name",
            "brand",
        )


class ProductCardSerializer(serializers.ModelSerializer):
    """
    1. this serializer is for product cards
    2. it takes in color variant model
    """
    brand = serializers.SerializerMethodField("get_brand")
    color = serializers.SerializerMethodField("get_color")
    available_colors = serializers.SerializerMethodField("get_available_colors")
    starting_price = serializers.SerializerMethodField("get_price")
    name = serializers.SerializerMethodField("get_name")
    rating = serializers.SerializerMethodField("get_rating")
    parent_slug = serializers.SerializerMethodField("get_parent_slug")

    class Meta:
        model = ProductColorVariant
        fields = (
            "id",
            "name",
            "image_url",
            "slug",
            "parent_slug",
            "brand",
            "color",
            "available_colors",
            "starting_price",
            "date_added",
            "rating",
        )

    def get_parent_slug(self, color_variant):
        return color_variant.parent_product.slug

    def get_rating(self, color_variant):
        context = {
            'rating': 0,
            'review_count': 0
        }
        ratings = Review.objects.filter(product=color_variant.parent_product)
        if ratings.count() > 0:
            rating = sum([r.rating for r in ratings]) / ratings.count()
            context['rating'] = round(rating, 1)
            context['review_count'] = ratings.count()

        return context

    def get_color(self, color_variant):
        return color_variant.color.slug

    def get_available_colors(self, color_variant):
        color_variants = ProductColorVariant.objects.filter(parent_product_id=color_variant.parent_product.id)
        return [cv.color.slug for cv in color_variants]

    def get_brand(self, color_variant):
        return BrandSerializer(color_variant.parent_product.brand).data

    def get_price(self, color_variant):
        product = Product.objects.filter(color_variant_id=color_variant.id).order_by("price")
        if product.count() > 0:
            return product.first().price
        return -1

    def get_name(self, color_variant):
        return color_variant.parent_product.name


class ProductPageSerializer(serializers.ModelSerializer):
    """
    # this serializer is for products page
    # takes in color variant slug
    """
    brand = serializers.SerializerMethodField("get_brand")
    color = serializers.SerializerMethodField("get_color")
    available_colors = serializers.SerializerMethodField("get_available_colors")
    available_products = serializers.SerializerMethodField("get_available_products")
    starting_price = serializers.SerializerMethodField("get_price")
    name = serializers.SerializerMethodField("get_name")
    images = serializers.SerializerMethodField("get_images")
    rating = serializers.SerializerMethodField("get_rating")
    parent_slug = serializers.SerializerMethodField("get_parent_slug")

    class Meta:
        model = ProductColorVariant
        fields = (
            "id",
            "name",
            "image_url",
            "images",
            "slug",
            "parent_slug",
            "brand",
            "color",
            "available_colors",
            "available_products",
            "starting_price",
            "rating",
        )

    def get_parent_slug(self, color_variant):
        return color_variant.parent_product.slug

    def get_available_products(self, color_variant):
        available_products = {}
        products = Product.objects.filter(color_variant=color_variant)

        for product in products:
            available_products[product.size.size] = {
                    "id": product.pk,
                    "price": product.price,
                    "quantity": product.quantity
                }

        return available_products

    def get_rating(self, color_variant):
        context = {
            'rating': 0,
            'review_count': 0
        }
        ratings = Review.objects.filter(product=color_variant.parent_product)
        if ratings.count() > 0:
            rating = sum([r.rating for r in ratings]) / ratings.count()
            context['rating'] = round(rating, 1)
            context['review_count'] = ratings.count()

        return context

    def get_images(self, color_variant):
        images = ProductImage.objects.filter(color_variant=color_variant)
        return ImageSerializer(images, many=True).data

    def get_color(self, color_variant):
        color = Color.objects.get(id=color_variant.color.pk)
        return color.slug

    def get_available_colors(self, color_variant):
        color_variants = ProductColorVariant.objects.filter(parent_product_id=color_variant.parent_product.id)
        available_colors = []
        for cv in color_variants:
            available_colors.append(
                {
                    'color': cv.color.name,
                    'color_slug': cv.color.slug,
                    'slug': cv.slug,
                    'image_url': cv.image_url,
                }
            )
        return available_colors

    def get_brand(self, color_variant):
        parent_product = ParentProduct.objects.get(id=color_variant.parent_product.id)
        return BrandSerializer(parent_product.brand).data

    def get_price(self, color_variant):
        product = Product.objects.filter(color_variant_id=color_variant.id).order_by("price")
        if product.count() > 0:
            return product.first().price
        return -1

    def get_name(self, color_variant):
        parent_product = ParentProduct.objects.get(id=color_variant.parent_product.id)
        return parent_product.name


class ProductSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField("get_size")
    image_url = serializers.SerializerMethodField("get_image_url")
    name = serializers.SerializerMethodField("get_product_name")
    color = serializers.SerializerMethodField("get_color")

    class Meta:
        model = Product
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

    def get_color(self, product):
        return ColorSerializer(product.color_variant.color).data

    def get_size(self, size_variant):
        return size_variant.size.size

    def get_image_url(self, size_variant):
        return size_variant.color_variant.image_url

    def get_product_name(self, size_variant):
        return size_variant.color_variant.parent_product.name
