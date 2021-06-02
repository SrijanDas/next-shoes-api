from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name', )
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.slug}/"

class Seller(models.Model):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    slug = models.SlugField()
    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/sellers/', blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='uploads/thumbnail/sellers/', blank=True, null=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return f"/{self.slug}/"

    def get_image(self):
        if self.image:
            return 'http://vkart.herokuapp.com' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://vkart.herokuapp.com' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'vkart.herokuapp.com' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='uploads/thumbnail/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://vkart.herokuapp.com' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://vkart.herokuapp.com' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'vkart.herokuapp.com' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
