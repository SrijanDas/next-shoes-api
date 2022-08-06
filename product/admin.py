from django.contrib import admin
from .models import *
# Register your models here.


class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "date_added")
    prepopulated_fields = {"slug": ("name",)}


class ColorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class SizeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("size",)}


class ParentProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "date_added")
    prepopulated_fields = {"slug": ("name",)}


class ColorVariantAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("parent_product",)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "color_variant", "size", "price", "quantity", "date_added")
    prepopulated_fields = {"slug": ("color_variant", "size")}


admin.site.register(Brand, BrandAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(ParentProduct, ParentProductAdmin)
admin.site.register(ColorVariant, ColorVariantAdmin)
admin.site.register(Product, ProductAdmin)


