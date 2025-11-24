from django.db import models
from .customer import Customer

class Store(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='store'
    )
    name = models.CharField(max_length=155)
    description = models.TextField()
    product = models.ManyToManyField("Product")