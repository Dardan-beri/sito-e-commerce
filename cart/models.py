from django.db import models
from django.conf import settings
from store.models import Product

# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    original_quantity_available = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'product')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.original_quantity_available = self.product.quantity_available
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity

    def get_total_discounted_price(self):
        if self.product.is_discounted and self.product.discounted_price:
            return self.product.discounted_price * self.quantity
        return self.get_total_price()