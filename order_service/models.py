from django.db import models
from django.conf import settings
from store.models import Product

# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')  # impedisce doppioni dello stesso prodotto

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x {self.quantity}"
