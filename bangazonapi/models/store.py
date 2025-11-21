from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
    )
    name = models.CharField(max_length=155)
    description = models.TextField()
    product = models.ManyToManyField("Product")