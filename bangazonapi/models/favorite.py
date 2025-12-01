from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .customer import Customer
from .productcategory import ProductCategory
from .orderproduct import OrderProduct
from .store import Store
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE


class Favorite(models.Model):

    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name="favorited"
    )
    seller = models.ForeignKey(
        Store, on_delete=models.DO_NOTHING, related_name="favorited"
    )
