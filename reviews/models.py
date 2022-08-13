from django.db import models
from accounts.models import Account as User
from product.models import ParentProduct as Product
# Create your models here.


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review = models.CharField(max_length=512)
    date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.product.slug)
