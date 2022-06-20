from django.contrib import admin
from .models import *
# Register your models here.


class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "date_added")
    prepopulated_fields = {"slug": ("name",)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "date_added")
    prepopulated_fields = {"slug": ("name",)}


class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ("parent_product", "size", "price", "quantity", "date_added")
    prepopulated_fields = {"slug": ("parent_product", "size")}


class ColorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class SizeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("size",)}


class ProductVariantAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product",)}


admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariantDetail, ProductDetailsAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)

