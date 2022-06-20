import datetime

from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File

from django.utils.text import slugify
# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    logo_url = models.CharField(max_length=500, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.slug}/"

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name.lower())
        return super().save(*args, **kwargs)


class Product(models.Model):
    brand = models.ForeignKey(Brand, related_name="products", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    # description = models.TextField(blank=True, null=True)
    # thumbnail = models.ImageField(
    #     upload_to='uploads/thumbnail/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name.lower())
        return super().save(*args, **kwargs)


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.lower())
        return super().save(*args, **kwargs)


class Size(models.Model):
    size = models.IntegerField(unique=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return str(self.size)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.size).lower())
        return super().save(*args, **kwargs)


# stores different color variants for one single parent product
class ProductVariant(models.Model):
    parent_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=500)
    main_variant = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.parent_product.name} | Color={self.color.name}"

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(f"{self.parent_product.name.lower()}-{self.color.name}")
        return super().save(*args, **kwargs)


# stores different "sizes", "price", available "quantity" for different color variants
class ProductVariantDetail(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100)

    # class Meta:
    #     verbose_name_plural = "product details"

    def __str__(self):
        return self.product_variant.slug

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(f"{self.product_variant.slug}-{str(self.size)}")
        return super().save(*args, **kwargs)

