import datetime

from django.db import models
from django.utils.text import slugify

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    logo_url = models.CharField(max_length=500, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.slug}/"

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


# this is the main parent product
class ParentProduct(models.Model):
    brand = models.ForeignKey(Brand, related_name="products", on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
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


# stores different color variants for one single parent product
class ColorVariant(models.Model):
    parent_product = models.ForeignKey(ParentProduct, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=500)
    main_variant = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.parent_product.name} | Color={self.color.name}"

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(f"{self.parent_product.slug}-{self.color.name}")
        return super().save(*args, **kwargs)


# storing all the product images
class ProductImage(models.Model):
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=255)

    def __str__(self):
        return self.color_variant.__str__()


# stores different "sizes", "price", "quantity" for different color variants
class Product(models.Model):
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)

    # class Meta:
    #     verbose_name_plural = "product details"

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(f"{self.color_variant.slug}-{str(self.size.size)}")
        return super().save(*args, **kwargs)
