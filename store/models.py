from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)

    is_discounted = models.BooleanField(default=False)
    discounted_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )

    def get_final_price(self):
        if self.is_discounted and self.discounted_price:
            return self.discounted_price
        return self.price

    def __str__(self):
        return self.name